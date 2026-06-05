import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import time
import torch
import torch.nn as nn
import torch.nn.functional as F

from susagpt.src.config import (
    BASE_MODEL_PATH,
    FINETUNED_MODEL_PATH,
    GENERATION_CONFIG,
    QUANTIZED_MODEL_PATH,
    RLHF_MODEL_PATH,
    TOKENIZER_PATH,
)
from susagpt.src.model import SusaGPT
from susagpt.src.tokenizer import Tokenizer


# generate.py ab inference utilities ka central file hai.
# Yahin se:
# 1. best model resolve hota hai
# 2. quantized model load ho sakta hai
# 3. top-k / top-p / Mirostat sampling hoti hai
# 4. KV cache aur beam search dono chal sakte hain
#
# Important practical note:
# tokenizer aur model checkpoint ka vocab size match karna bahut zaruri hai.
# Agar tokenizer 2262 tokens ka hai aur checkpoint 768 tokens par trained hai,
# to encode ke baad kuch token ids model embedding range ke bahar chale jayenge.
# Us case me "index out of range" error aata hai.


def apply_dynamic_int8_quantization(model):
    # Dynamic INT8 quantization inference ke liye useful hoti hai.
    # Ye mostly Linear layers ko int8 me convert karti hai.
    #
    # Iska fayda:
    # - model chhota ho sakta hai
    # - CPU inference fast ho sakta hai
    # - sharing aur deployment easy ho sakta hai
    return torch.quantization.quantize_dynamic(
        model,
        {nn.Linear},
        dtype=torch.qint8,
    )


def list_candidate_model_paths(prefer_quantized=True):
    candidate_paths = []

    if prefer_quantized:
        candidate_paths.append(QUANTIZED_MODEL_PATH)

    candidate_paths.extend([RLHF_MODEL_PATH, FINETUNED_MODEL_PATH, BASE_MODEL_PATH])
    return candidate_paths


def resolve_model_path(prefer_quantized=True):
    candidate_paths = list_candidate_model_paths(prefer_quantized=prefer_quantized)

    for path in candidate_paths:
        if Path(path).exists():
            return path

    raise FileNotFoundError("Koi trained model file nahi mili.")


def load_checkpoint_metadata(checkpoint_path):
    # Metadata check lightweight safety step hai.
    # Isse full model banane se pehle ye verify kar sakte hain ki checkpoint
    # current tokenizer ke saath compatible hai ya nahi.
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    return {
        "vocab_size": checkpoint["vocab_size"],
        "quantized": checkpoint.get("quantized", False),
    }


def load_model_checkpoint(checkpoint_path):
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)

    model = SusaGPT(
        vocab_size=checkpoint["vocab_size"],
        embed_dim=checkpoint["embed_dim"],
        num_heads=checkpoint["num_heads"],
        num_kv_heads=checkpoint.get("num_kv_heads", checkpoint["num_heads"]),
        num_layers=checkpoint["num_layers"],
        max_len=checkpoint.get("max_len", 32),
        dropout=checkpoint.get("dropout", 0.1),
    )

    # Quantized checkpoint load karte waqt pehle same quantized structure banana padta hai.
    if checkpoint.get("quantized", False):
        model = apply_dynamic_int8_quantization(model)

    model.load_state_dict(checkpoint["model_state"])
    model.eval()
    return model


def resolve_compatible_model_path(tokenizer, prefer_quantized=True):
    # Auto-selection me sirf wahi checkpoint choose karte hain jo current tokenizer
    # ke vocab size ke saath match kare. Isse runtime embedding crash avoid hota hai.
    for candidate_path in list_candidate_model_paths(prefer_quantized=prefer_quantized):
        if not Path(candidate_path).exists():
            continue

        metadata = load_checkpoint_metadata(candidate_path)
        if metadata["vocab_size"] == tokenizer.vocab_size:
            return candidate_path

    raise FileNotFoundError(
        "Current tokenizer ke saath compatible model checkpoint nahi mila."
    )


def validate_tokenizer_model_compatibility(tokenizer, checkpoint_path):
    metadata = load_checkpoint_metadata(checkpoint_path)

    if metadata["vocab_size"] != tokenizer.vocab_size:
        raise ValueError(
            "Tokenizer aur model checkpoint ka vocab size match nahi kar raha. "
            f"Tokenizer vocab={tokenizer.vocab_size}, "
            f"checkpoint vocab={metadata['vocab_size']}. "
            "Current setup me base model use karo ya matching tokenizer/checkpoint pair load karo."
        )


def load_everything(model_path=None, tokenizer_path=TOKENIZER_PATH, prefer_quantized=True, return_path=False):
    tokenizer = Tokenizer()
    tokenizer.load(str(tokenizer_path))

    if model_path is None:
        model_path = resolve_compatible_model_path(
            tokenizer=tokenizer,
            prefer_quantized=prefer_quantized,
        )
    else:
        validate_tokenizer_model_compatibility(tokenizer, model_path)

    model = load_model_checkpoint(model_path)

    print(f"SusaGPT loaded from -> {model_path}")

    if return_path:
        return model, tokenizer, model_path
    return model, tokenizer


def filter_logits_with_top_k_top_p(logits, top_k=0, top_p=1.0):
    if top_k > 0:
        top_k = min(top_k, logits.size(-1))
        threshold = torch.topk(logits, top_k).values[..., -1, None]
        logits = logits.masked_fill(logits < threshold, float("-inf"))

    if 0.0 < top_p < 1.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        sorted_probs = F.softmax(sorted_logits, dim=-1)
        cumulative_probs = torch.cumsum(sorted_probs, dim=-1)

        sorted_mask = cumulative_probs > top_p
        sorted_mask[..., 1:] = sorted_mask[..., :-1].clone()
        sorted_mask[..., 0] = False

        removal_mask = torch.zeros_like(logits, dtype=torch.bool)
        removal_mask.scatter_(dim=-1, index=sorted_indices, src=sorted_mask)
        logits = logits.masked_fill(removal_mask, float("-inf"))

    return logits


def apply_repetition_penalty(logits, generated_tokens, penalty):
    if penalty <= 1.0 or not generated_tokens:
        return logits

    adjusted_logits = logits.clone()
    for token_id in set(generated_tokens):
        if adjusted_logits[token_id] > 0:
            adjusted_logits[token_id] = adjusted_logits[token_id] / penalty
        else:
            adjusted_logits[token_id] = adjusted_logits[token_id] * penalty
    return adjusted_logits


def sample_with_mirostat(logits, generated_tokens, repetition_penalty, tau, eta, mirostat_state):
    # Mirostat ka goal output surprise ko ek target band me rakhna hota hai.
    # Ye static top-k/top-p ki jagah dynamic control deta hai.
    #
    # Yahan simplified Mirostat v2 style logic use ho raha hai:
    # - current mu ke basis par allowed token set banega
    # - sampled token ki surprise dekhkar mu update hoga
    adjusted_logits = apply_repetition_penalty(logits, generated_tokens, repetition_penalty)
    probs = F.softmax(adjusted_logits, dim=-1)

    sorted_probs, sorted_indices = torch.sort(probs, descending=True)
    surprisals = -torch.log2(sorted_probs.clamp_min(1e-9))

    threshold_mask = surprisals <= mirostat_state["mu"]
    if not threshold_mask.any():
        threshold_mask[0] = True

    kept_probs = sorted_probs[threshold_mask]
    kept_indices = sorted_indices[threshold_mask]
    kept_probs = kept_probs / kept_probs.sum()

    sampled_pos = torch.multinomial(kept_probs, num_samples=1).item()
    next_token = kept_indices[sampled_pos].item()

    observed_prob = probs[next_token].clamp_min(1e-9)
    observed_surprise = -torch.log2(observed_prob).item()

    # mu update se next step ki randomness adapt hoti hai.
    mirostat_state["mu"] = max(
        1.0,
        mirostat_state["mu"] - eta * (observed_surprise - tau),
    )
    return next_token


def get_cache_length(kv_cache):
    if not kv_cache:
        return 0
    return kv_cache[0][0].size(2)


def generate_with_sampling_stream(
    model,
    generated,
    max_new_tokens,
    temperature,
    top_k,
    top_p,
    repetition_penalty,
    use_kv_cache,
    sampling_mode,
    mirostat_tau,
    mirostat_eta,
):
    kv_cache = None
    mirostat_state = {"mu": 2.0 * mirostat_tau}

    with torch.no_grad():
        if not generated:
            return

        x = torch.tensor([generated[-model.max_len :]], dtype=torch.long)
        if use_kv_cache:
            logits, kv_cache = model(x, use_cache=True, start_pos=0)
        else:
            logits = model(x)

        for _ in range(max_new_tokens):
            next_token_logits = logits[0, -1, :] / temperature

            if sampling_mode == "mirostat":
                next_token = sample_with_mirostat(
                    logits=next_token_logits,
                    generated_tokens=generated,
                    repetition_penalty=repetition_penalty,
                    tau=mirostat_tau,
                    eta=mirostat_eta,
                    mirostat_state=mirostat_state,
                )
            else:
                next_token_logits = apply_repetition_penalty(
                    next_token_logits,
                    generated_tokens=generated,
                    penalty=repetition_penalty,
                )
                filtered_logits = filter_logits_with_top_k_top_p(
                    next_token_logits,
                    top_k=top_k,
                    top_p=top_p,
                )
                probs = F.softmax(filtered_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1).item()

            generated.append(next_token)
            yield next_token

            if not use_kv_cache:
                context = generated[-model.max_len :]
                x = torch.tensor([context], dtype=torch.long)
                logits = model(x)
                continue

            cache_length = get_cache_length(kv_cache)
            if cache_length >= model.max_len:
                context = generated[-model.max_len :]
                x = torch.tensor([context], dtype=torch.long)
                logits, kv_cache = model(x, use_cache=True, start_pos=0)
            else:
                x = torch.tensor([[next_token]], dtype=torch.long)
                logits, kv_cache = model(
                    x,
                    kv_cache=kv_cache,
                    use_cache=True,
                    start_pos=cache_length,
                )


def generate_with_sampling(
    model,
    generated,
    max_new_tokens,
    temperature,
    top_k,
    top_p,
    repetition_penalty,
    use_kv_cache,
    sampling_mode,
    mirostat_tau,
    mirostat_eta,
):
    for _ in generate_with_sampling_stream(
        model=model,
        generated=generated,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        use_kv_cache=use_kv_cache,
        sampling_mode=sampling_mode,
        mirostat_tau=mirostat_tau,
        mirostat_eta=mirostat_eta,
    ):
        pass
    return generated


def beam_search_generate(
    model,
    generated,
    max_new_tokens,
    beam_width,
    temperature,
    repetition_penalty,
):
    beams = [(generated[:], 0.0)]

    with torch.no_grad():
        for _ in range(max_new_tokens):
            candidates = []

            for beam_tokens, beam_score in beams:
                context = beam_tokens[-model.max_len :]
                x = torch.tensor([context], dtype=torch.long)
                logits = model(x)
                next_token_logits = logits[0, -1, :] / temperature
                next_token_logits = apply_repetition_penalty(
                    next_token_logits,
                    generated_tokens=beam_tokens,
                    penalty=repetition_penalty,
                )

                log_probs = F.log_softmax(next_token_logits, dim=-1)
                top_values, top_indices = torch.topk(log_probs, beam_width)

                for value, index in zip(top_values.tolist(), top_indices.tolist()):
                    candidates.append((beam_tokens + [index], beam_score + value))

            beams = sorted(
                candidates,
                key=lambda item: item[1] / max(1, len(item[0])),
                reverse=True,
            )[:beam_width]

    return beams[0][0]


def generate_stream(
    model,
    tokenizer,
    prompt,
    max_new_tokens=None,
    temperature=None,
    top_k=None,
    top_p=None,
    repetition_penalty=None,
    use_kv_cache=None,
    use_beam_search=False,
    beam_width=None,
    sampling_mode=None,
    mirostat_tau=None,
    mirostat_eta=None,
):
    max_new_tokens = max_new_tokens or GENERATION_CONFIG["max_new_words"]
    temperature = temperature or GENERATION_CONFIG["temperature"]
    top_k = GENERATION_CONFIG["top_k"] if top_k is None else top_k
    top_p = GENERATION_CONFIG["top_p"] if top_p is None else top_p
    repetition_penalty = (
        GENERATION_CONFIG["repetition_penalty"]
        if repetition_penalty is None
        else repetition_penalty
    )
    use_kv_cache = (
        GENERATION_CONFIG["use_kv_cache"] if use_kv_cache is None else use_kv_cache
    )
    beam_width = GENERATION_CONFIG["beam_width"] if beam_width is None else beam_width
    sampling_mode = sampling_mode or GENERATION_CONFIG["sampling_mode"]
    mirostat_tau = (
        GENERATION_CONFIG["mirostat_tau"] if mirostat_tau is None else mirostat_tau
    )
    mirostat_eta = (
        GENERATION_CONFIG["mirostat_eta"] if mirostat_eta is None else mirostat_eta
    )

    generated = tokenizer.encode(prompt)
    prompt_len = len(generated)

    if use_beam_search:
        full_tokens = beam_search_generate(
            model=model,
            generated=generated,
            max_new_tokens=max_new_tokens,
            beam_width=beam_width,
            temperature=temperature,
            repetition_penalty=repetition_penalty,
        )
        new_tokens = full_tokens[prompt_len:]
        yield tokenizer.decode(new_tokens)
    else:
        # Clone to avoid mutating prompt tokens outside the function
        gen_tokens = list(generated)
        decoded_len = len(tokenizer.decode(gen_tokens))
        for token_id in generate_with_sampling_stream(
            model=model,
            generated=gen_tokens,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            use_kv_cache=use_kv_cache,
            sampling_mode=sampling_mode,
            mirostat_tau=mirostat_tau,
            mirostat_eta=mirostat_eta,
        ):
            full_decoded = tokenizer.decode(gen_tokens)
            chunk = full_decoded[decoded_len:]
            decoded_len = len(full_decoded)
            yield chunk


def generate(
    model,
    tokenizer,
    prompt,
    max_new_tokens=None,
    temperature=None,
    top_k=None,
    top_p=None,
    repetition_penalty=None,
    use_kv_cache=None,
    use_beam_search=False,
    beam_width=None,
    sampling_mode=None,
    mirostat_tau=None,
    mirostat_eta=None,
):
    chunks = list(generate_stream(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        use_kv_cache=use_kv_cache,
        use_beam_search=use_beam_search,
        beam_width=beam_width,
        sampling_mode=sampling_mode,
        mirostat_tau=mirostat_tau,
        mirostat_eta=mirostat_eta,
    ))
    return "".join(chunks)


def chat(model, tokenizer):
    print("\n" + "=" * 60)
    print("SusaGPT interactive chat")
    print("quit likho band karne ke liye")
    print("beam: likhoge to beam search mode chalega")
    print("miro: likhoge to Mirostat mode chalega")
    print("Default run me base SusaGPT.pt use ho raha hai")
    print("=" * 60 + "\n")

    while True:
        # Agar script non-interactive environment me run ho rahi ho
        # to input() EOF de sakta hai. Us case me clean exit karna better hai.
        try:
            prompt = input("Tum : ").strip()
        except EOFError:
            print("\nInput stream band hai. Chat mode close kiya ja raha hai.")
            break

        if prompt.lower() in ["quit", "exit", "band karo"]:
            print("\nSusaGPT band ho raha hai. Alvida!")
            break

        if not prompt:
            print("Kuch likho!\n")
            continue

        use_beam_search = prompt.lower().startswith("beam:")
        use_mirostat = prompt.lower().startswith("miro:")

        clean_prompt = prompt
        if use_beam_search:
            clean_prompt = prompt[5:].strip()
        elif use_mirostat:
            clean_prompt = prompt[5:].strip()

        output = generate(
            model=model,
            tokenizer=tokenizer,
            prompt=clean_prompt,
            use_beam_search=use_beam_search,
            sampling_mode="mirostat" if use_mirostat else "topk_topp",
        )
        print(f"SusaGPT : {output}\n")


def filter_context_length(context, prompt):
    import re
    clean_prompt = prompt.lower().strip()
    detail_keywords = [
        "explain", "detail", "why", "describe", "elaborate", "tell me about", 
        "long", "full", "write a paragraph", "sab", "samjhao", "vistar", "detail me"
    ]
    wants_detail = any(kw in clean_prompt for kw in detail_keywords)
    
    if wants_detail:
        return context
        
    # Split using lookbehinds for standard sentence end punctuation
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', context) if s.strip()]
    if sentences:
        if len(sentences) > 1:
            return sentences[0] + " " + sentences[1]
        return sentences[0]
    return context


def web_search_ddg(query):
    import urllib.request
    import urllib.parse
    import re
    import html as html_unescape
    
    url = "https://html.duckduckgo.com/html/"
    data = urllib.parse.urlencode({'q': query}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    try:
        with urllib.request.urlopen(req, timeout=3.0) as response:
            html_text = response.read().decode('utf-8')
            
            # Extract zero-click abstract (instant answer)
            abstract = None
            if 'id="zero_click_abstract"' in html_text:
                try:
                    part = html_text.split('id="zero_click_abstract"', 1)[1]
                    part = part.split('>', 1)[1]
                    content = part.split('</div>', 1)[0]
                    content = re.sub(r'<[^>]+>', '', content)
                    content = " ".join(content.split())
                    if content:
                        abstract = content
                except Exception:
                    pass
            
            # Extract organic snippets
            snippets = []
            parts = html_text.split('class="result__snippet"')
            for part in parts[1:4]:
                try:
                    if '>' in part:
                        content = part.split('>', 1)[1]
                        if '</a>' in content:
                            snippet = content.split('</a>', 1)[0]
                            snippet = re.sub(r'<[^>]+>', '', snippet)
                            snippet = " ".join(snippet.split())
                            if snippet:
                                snippets.append(snippet)
                except Exception:
                    pass
            
            if abstract:
                abstract = html_unescape.unescape(abstract).replace('\r', '')
                if snippets:
                    snippets = [html_unescape.unescape(s).replace('\r', '') for s in snippets]
                    return f"{abstract} | Search snippets: " + " ".join(snippets)
                return abstract
            if snippets:
                snippets = [html_unescape.unescape(s).replace('\r', '') for s in snippets]
                return " ".join(snippets)
            return ""
    except Exception:
        return ""


def generate_hybrid_stream(
    prompt,
    model,
    tokenizer,
    max_new_tokens=None,
    temperature=None,
    top_k=None,
    top_p=None,
    repetition_penalty=None,
    use_kv_cache=None,
    use_beam_search=False,
    beam_width=None,
    sampling_mode=None,
    mirostat_tau=None,
    mirostat_eta=None,
):
    # 0. Conversational Intent Handler (Greetings & General FAQs)
    clean_prompt = prompt.lower().strip().replace("?", "").replace(".", "").replace("!", "")
    
    # 0.1 Date & Time Direct Local Handlers
    import datetime
    is_date_query = any(kw in clean_prompt for kw in ["date", "tarikh", "taarikh", "din"]) and any(kw in clean_prompt for kw in ["today", "aaj", "current", "ab", "now"])
    is_time_query = any(kw in clean_prompt for kw in ["time", "samay", "waqt", "ghadi"]) and any(kw in clean_prompt for kw in ["current", "today", "aaj", "ab", "now", "kya"])
    
    if is_date_query or clean_prompt in ["today", "date", "tarikh", "aaj ki date"]:
        now = datetime.datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        ans = f"Today's date is {date_str}."
        for char in ans:
            yield char
            time.sleep(0.005)
        return
        
    if is_time_query or clean_prompt in ["time", "samay", "waqt", "what is the time"]:
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        ans = f"The current time is {time_str}."
        for char in ans:
            yield char
            time.sleep(0.005)
        return
    
    greetings_map = {
        ("hi", "hello", "hey", "hola", "namaste", "salam", "helo"): 
            "Hello! Main SusaGPT hoon—SusaLabs ka custom AI assistant. SusaLabs ke services aur technology ke baare me aap kya jaanna chahte hain?",
        ("how are you", "kaise ho", "kaise hain aap", "how r u", "how are u"): 
            "Main ekdam badhiya hoon! Aap bataiye, aap kaise hain aur aaj SusaLabs ke baare me kya jaanna chahte hain?",
        ("who are you", "tum kaun ho", "aap kaun hain", "identify yourself", "what is your name", "who r u"): 
            "Main SusaGPT hoon, jise SusaLabs ne custom software, CRM, aur biotech solutions ke baare me chat karne ke liye build kiya hai.",
        ("thank you", "thanks", "dhanyawad", "shukriya", "thankyou"): 
            "You're welcome! Agar SusaLabs ke products ya services ke baare me koi aur sawal hai, toh zaroor bataiye.",
        ("bye", "goodbye", "alvida", "chalta hoon"): 
            "Alvida! SusaLabs se connect karne ke liye dhanyawad. Have a great day!"
    }
    
    prompt_words = clean_prompt.split()
    for keys, reply in greetings_map.items():
        if clean_prompt in keys or (len(prompt_words) <= 3 and any(word in keys for word in prompt_words)):
            for char in reply:
                yield char
                time.sleep(0.005)
            return

    # 1. Retrieve local context first using TF-IDF/Overlap RAG
    import re
    from susagpt.src.config import DATA_PATH
    
    context = ""
    is_web = False
    if DATA_PATH.exists():
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            
            stopwords = {"is", "are", "was", "were", "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by", "of", "does", "what", "how", "why", "who", "which", "where", "when", "s"}
            prompt_words = set(w for w in re.findall(r'\w+', prompt.lower()) if len(w) > 3 and w not in stopwords)
            if prompt_words:
                best_line = ""
                best_score = 0
                for line in lines:
                    line_words = set(w for w in re.findall(r'\w+', line.lower()) if len(w) > 3 and w not in stopwords)
                    if not line_words:
                        continue
                    intersection = prompt_words.intersection(line_words)
                    score = len(intersection) / len(prompt_words)
                    if score > best_score:
                        best_score = score
                        best_line = line
                if best_score > 0.50:
                    context = best_line
                else:
                    is_web = True
            else:
                is_web = True
        except Exception:
            is_web = True
    else:
        is_web = True

    # 2. Handle web search if local context is not found
    web_info = ""
    if is_web:
        yield "🔍 Web searching...\n\n"
        web_info = web_search_ddg(prompt)

    # 3. Try routing to local Ollama if available
    import urllib.request
    import json
    import os
    
    try:
        url = "http://localhost:11434/api/generate"
        if is_web and web_info:
            ollama_prompt = f"Web Search Results: {web_info}\nQuestion: {prompt}\nAnswer the question concisely in Hinglish based on the search results."
        else:
            ollama_prompt = f"Context: {context or 'No context available.'}\nQuestion: {prompt}\nAnswer the question concisely in Hinglish based on the context."
            
        data = {
            "model": "qwen3.5:0.8b",
            "prompt": ollama_prompt,
            "stream": True
        }
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode("utf-8"), 
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=1.5) as response:
            for line in response:
                if line:
                    res = json.loads(line.decode("utf-8"))
                    chunk = res.get("response", "")
                    if chunk:
                        yield chunk
            return
    except Exception:
        pass

    # Check Cloud Gemini API
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            if is_web and web_info:
                gemini_prompt = f"You are SusaGPT, a helpful AI assistant for SusaLabs.\nWeb Search Results: {web_info}\nQuestion: {prompt}\nAnswer the question concisely in Hinglish based on the search results."
            else:
                gemini_prompt = f"You are SusaGPT, a helpful AI assistant for SusaLabs.\nContext: {context or 'No context.'}\nQuestion: {prompt}\nAnswer the question concisely in Hinglish based on the context."
                
            data = {
                "contents": [{
                    "parts": [{
                        "text": gemini_prompt
                    }]
                }]
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=3.0) as response:
                res = json.loads(response.read().decode("utf-8"))
                candidates = res.get("candidates", [])
                if candidates:
                    ans = candidates[0]["content"]["parts"][0]["text"].strip()
                    if ans:
                        for word in ans.split(" "):
                            yield word + " "
                            time.sleep(0.02)
                        return
        except Exception:
            pass

    # Check Cloud OpenAI API
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            if is_web and web_info:
                system_msg = f"You are SusaGPT, a helpful AI assistant. Answer the user's question using these web search results:\n{web_info}"
            else:
                system_msg = f"You are SusaGPT, a helpful AI assistant for SusaLabs. Answer questions based on this context:\n{context}"
                
            data = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 100,
                "stream": True
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {openai_key}"
                }
            )
            with urllib.request.urlopen(req, timeout=3.0) as response:
                for line in response:
                    line_str = line.decode("utf-8").strip()
                    if line_str.startswith("data: "):
                        data_str = line_str[6:]
                        if data_str == "[DONE]":
                            break
                        res = json.loads(data_str)
                        chunk = res.get("choices", [{}])[0].get("delta", {}).get("content", "")
                        if chunk:
                            yield chunk
                return
        except Exception:
            pass

    # 4. Fallback to Local RAG Heuristics or Web snippet output
    if is_web and web_info:
        lines_to_yield = ["[Web Source]\n"]
        if " | Search snippets: " in web_info:
            parts = web_info.split(" | Search snippets: ")
            abstract = parts[0].strip()
            snippets_text = parts[1].strip()
            
            if abstract:
                lines_to_yield.append(f"• {abstract}\n")
            
            # Simple sentence splitting for snippets
            sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', snippets_text) if s.strip()]
            for s in sentences:
                if not s.endswith("."):
                    s += "."
                lines_to_yield.append(f"• {s}\n")
        else:
            sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', web_info) if s.strip()]
            for s in sentences:
                if not s.endswith("."):
                    s += "."
                lines_to_yield.append(f"• {s}\n")
                
        full_ans = "".join(lines_to_yield)
        for char in full_ans:
            yield char
            time.sleep(0.005)
        return
        
    if context:
        short_context = filter_context_length(context, prompt)
        ans = f"[Local RAG Context] {short_context}"
        for word in ans.split(" "):
            yield word + " "
            time.sleep(0.02)
        return

    # 5. Standalone autoregressive generator fallback
    yield from generate_stream(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        use_kv_cache=use_kv_cache,
        use_beam_search=use_beam_search,
        beam_width=beam_width,
        sampling_mode=sampling_mode,
        mirostat_tau=mirostat_tau,
        mirostat_eta=mirostat_eta,
    )


def generate_hybrid(
    prompt,
    model,
    tokenizer,
    max_new_tokens=None,
    temperature=None,
    top_k=None,
    top_p=None,
    repetition_penalty=None,
    use_kv_cache=None,
    use_beam_search=False,
    beam_width=None,
    sampling_mode=None,
    mirostat_tau=None,
    mirostat_eta=None,
):
    chunks = list(generate_hybrid_stream(
        prompt=prompt,
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        use_kv_cache=use_kv_cache,
        use_beam_search=use_beam_search,
        beam_width=beam_width,
        sampling_mode=sampling_mode,
        mirostat_tau=mirostat_tau,
        mirostat_eta=mirostat_eta,
    ))
    return "".join(chunks)


def main():
    # Default CLI run me base model force kar rahe hain.
    # Reason:
    # current tokenizer artifacts/models/SusaGPT.pt ke saath match kar raha hai.
    # Fine-tuned / RLHF checkpoints old vocab size par bane hue hon to mismatch aa sakta hai.
    #
    # Agar future me matching tokenizer ke saath fine-tuned ya RLHF checkpoint banana ho,
    # tab load_everything me model_path change karke us checkpoint ko use kiya ja sakta hai.
    model, tokenizer = load_everything(
        model_path=BASE_MODEL_PATH,
        prefer_quantized=False,
    )

    print("\n--- Auto Tests ---")
    test_prompts = [
        "susalabs is",
        "artificial intelligence",
        "healthcare solutions",
        "हिंदी اردو ai mix",
    ]

    for prompt in test_prompts:
        result = generate(model=model, tokenizer=tokenizer, prompt=prompt)
        print(f">> {result}\n")

    chat(model, tokenizer)


if __name__ == "__main__":
    main()
