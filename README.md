# MyLLM - Hinglish Guide

Ye project ek chhota GPT-style language model banata hai jo:

1. Base text data par train hota hai
2. Q&A pairs par fine-tune hota hai
3. Preference data par RLHF-style alignment karta hai
4. Better sampling ke saath text generate karta hai
5. INT8 quantized version me compress ho sakta hai
6. REST API ke form me serve ho sakta hai
7. BLEU aur perplexity jaise metrics se evaluate ho sakta hai

Is README ka goal ye hai ki agar koi beginner bhi is project ko padhe to usse samajh aa jaye:

- project me kaunsi file kya karti hai
- kaunsa concept kahan use hua hai
- har training stage ka purpose kya hai
- model ko kaise chalana hai
- ANN, SwiGLU, BPE, GQA, PyTorch, RLHF, neural network jaise words ka matlab kya hai


## Project Flow

Is project ka learning flow 5 steps me divide hai:

1. Architecture fix
   SwiGLU, weight tying, GQA, dropout, RMSNorm, RoPE
2. Training fix
   AdamW, weight decay, gradient clipping, gradient accumulation, LR scheduler, mixed precision, data curriculum
3. Generation fix
   top-k, top-p, repetition penalty, KV cache, beam search, Mirostat
4. Fine-tuning
   50 Q&A pairs se direct jawab dena sikhana
5. RLHF-style alignment
   chosen vs rejected answers se behavior better karna
6. Quantization + API
   INT8 shareable model aur FastAPI serving


## File Structure

- `model.py`
  Ye model architecture define karta hai.
- `tokenizer.py`
  Ye text ko token ids me convert karta hai.
- `train.py`
  Base model training script hai.
- `generate.py`
  Trained model se text generate karta hai.
- `evaluate.py`
  Model ke BLEU score aur perplexity ko measure karta hai.
- `quantize.py`
  Trained model ko INT8 version me convert karta hai.
- `api.py`
  FastAPI based REST API expose karta hai.
- `SusaGPT_Architecture.md`
  SusaGPT ko GPT-2, LLaMA 3 aur GPT-4 ke context me explain karti hai.
- `SusaGPT_Skills.md`
  Batati hai ki SusaGPT samajhne ke baad kaunsi practical skills aati hain.
- `SusaGPT_Diagram_Guide.md`
  Diagrams ke through poore SusaGPT system ko visual tarike se samjhati hai.
- `MCP_Guide.md`
  MCP kya hota hai, kaise kaam karta hai aur kaise build hota hai ye samjhati hai.
- `AI_Agents_Guide.md`
  AI agents, tools, memory, planning aur multi-agent systems ko samjhati hai.
- `Agentic_AI_Guide.md`
  Agentic AI, generative AI relation, autonomy aur agentic workflows ko explain karti hai.
- `fine_tune.py`
  Q&A data par supervised fine-tuning karta hai.
- `rlhf.py`
  Simplified RLHF-style preference tuning karta hai.
- `config.py`
  Sare important configs ek jagah rakhta hai.
- `qa_pairs.json`
  50 Q&A pairs ka supervised fine-tuning data.
- `preference_pairs.json`
  RLHF-style chosen vs rejected examples.
- `data.txt`
  Base text corpus.
- `tokenizer.json`
  Saved tokenizer mapping.
- `SusaGPT.pt`
  Base trained model checkpoint.
- `SusaGPT-finetuned.pt`
  Q&A fine-tuned model checkpoint.
- `SusaGPT-rlhf.pt`
  Final aligned model checkpoint.
- `SusaGPT-int8.pt`
  Quantized INT8 inference checkpoint.
- `requirements.txt`
  Basic dependencies list.


## Kaise Run Karein

Pehle dependencies install karo:

```bash
pip install -r requirements.txt
```

Step 1: Base training

```bash
python train.py
```

Step 2: Q&A fine-tuning

```bash
python fine_tune.py
```

Step 3: RLHF-style alignment

```bash
python rlhf.py
```

Step 4: Generation / chat

```bash
python generate.py
```

Step 5: INT8 quantization

```bash
python quantize.py
```

Step 6: Evaluation metrics

```bash
python evaluate.py
```

Step 7: REST API run

```bash
uvicorn api:app --host 127.0.0.1 --port 8000 --reload
```

API docs:

- `http://127.0.0.1:8000/docs`


## Concepts Explained

### 1. PyTorch kya hai

PyTorch ek deep learning framework hai.
Is project me ye model banane, tensors handle karne, training chalane aur gradients calculate karne ke liye use hua hai.

Simple language me:
PyTorch wo toolkit hai jisse neural network code likha jata hai.


### 2. Tensor kya hota hai

Tensor ek multi-dimensional number container hota hai.
Ye list se zyada powerful hota hai aur GPU par bhi chal sakta hai.

Examples:

- scalar = ek number
- vector = numbers ki line
- matrix = numbers ka table
- tensor = usse bhi general form


### 3. Neural Network kya hota hai

Neural network ek aisa model hota hai jo data se patterns seekhta hai.
Ye human brain se inspired hota hai, lekin exact brain copy nahi hota.

Ye layers ka use karke input ko process karta hai aur output predict karta hai.


### 4. ANN kya hota hai

ANN ka full form hai Artificial Neural Network.

Ye neural network ka basic family name hai.
Is project ka model bhi ANN family me hi aata hai, lekin specifically ye transformer-style language model hai.


### 5. Tokenizer kya karta hai

Tokenizer text ko numbers me convert karta hai.

Example:

`"hello world"` -> `[12, 97]`

Model words directly nahi samajhta.
Isliye text ko token ids me convert karna padta hai.

Tokenizer reverse conversion bhi karta hai:

`[12, 97]` -> `"hello world"`

Is project me ab simple word-level tokenizer nahi, balki byte-level BPE tokenizer use hota hai.


### 6. Vocabulary kya hoti hai

Vocabulary ya vocab matlab total unique tokens ki list.

Example:
Agar corpus me words hain:

`ai, software, crm, healthcare`

to in sabko ids milengi.

Ye total count hi `vocab_size` hota hai.


### 7. BPE kya hota hai

BPE ka full form hai Byte Pair Encoding.

Ye tokenizer pehle text ko bytes me todta hai, phir common byte pairs ko merge karke useful subword tokens banata hai.

Iska fayda:

- rare words bhi tokenize ho jaate hain
- `<UNK>` token ki problem khatam ho jaati hai
- Hindi, Urdu, English mixed text handle ho sakta hai
- long words chhote meaningful pieces me toot sakte hain


### 8. Byte-level BPE kya hota hai

Byte-level BPE me raw UTF-8 bytes se start karte hain.
Har Unicode script bytes me represent ho sakti hai.

Isliye:

- Hindi
- Urdu
- English
- symbols

sab tokenize ho sakte hain bina unknown token ke.


### 9. Embedding kya hota hai

Embedding ek learnable vector representation hoti hai.

Word id ko model ek vector me convert karta hai:

`25 -> [0.12, -0.77, 0.41, ...]`

Isse model words ke beech relations seekh pata hai.


### 10. Positional Encoding kya hota hai

Transformer ko naturally word order ka idea nahi hota.
Positional encoding usse batata hai kaunsa token kis position par hai.

Isliye:

- `ai for healthcare`
- `healthcare for ai`

dono alag samjhe ja sakte hain.


### 11. Attention kya hota hai

Attention ka matlab:
model decide kare kaunsa word kis dusre word par kitna focus kare.

Example:
Sentence me agar word hai `it`,
to model pichle words dekhkar samajhne ki koshish karega ke `it` kis cheez ko refer kar raha hai.


### 12. Multi-Head Attention kya hota hai

Single attention me model ek hi nazariye se context dekhta hai.
Multi-head attention me multiple heads same sentence ko alag-alag angle se dekhte hain.

Iska fayda:

- ek head grammar par focus kar sakta hai
- ek head entity relations par
- ek head nearby context par
- ek head long-range context par

Is project me base idea multi-head attention ka hi hai, lekin optimized form me GQA use hua hai.


### 13. GQA kya hota hai

GQA ka full form hai Grouped Query Attention.

Isme Query heads zyada ho sakte hain, lekin Key aur Value heads kam hote hain.
Phir K aur V ko groups ke form me multiple Q heads ke saath share kiya jata hai.

Iska fayda:

- memory usage kam hoti hai
- KV cache halka hota hai
- generation faster aur efficient ho sakti hai


### 14. SwiGLU kya hota hai

SwiGLU ka matlab roughly Swish plus GLU style gating.

Ye feed-forward network ka upgraded version hota hai jahan ek branch gate banati hai aur doosri branch content.
Phir dono multiply hote hain.

Iska fayda:

- information flow zyada controlled hota hai
- modern LLMs me commonly use hota hai
- kabhi-kabhi GELU se better practical behavior mil sakta hai


### 15. Weight Tying kya hota hai

Weight tying ka matlab:
input embedding aur output projection same weights share karein.

Iska fayda:

- parameters bach sakte hain
- input aur output word space aligned hoti hai
- kabhi-kabhi language modeling quality improve hoti hai


### 16. Dropout kya hota hai

Dropout ek regularization technique hai.
Training ke time kuch neurons temporary ignore kiye jaate hain.

Iska fayda:

- model exact ratta kam marta hai
- generalization improve hoti hai
- overfitting ka chance kam hota hai


### 17. RMSNorm kya hota hai

RMSNorm normalization ka ek lightweight version hai.
Ye input ka scale stable rakhta hai, lekin LayerNorm ki tarah full mean subtraction nahi karta.

Iska fayda:

- computation simple hoti hai
- transformer me kaafi achha kaam karta hai
- modern LLMs me kaafi jagah use hota hai


### 18. RoPE kya hota hai

RoPE ka full form Rotary Positional Embedding hai.

Ye position information ko Q aur K vectors me rotate karke inject karta hai.
Simple sinusoidal position add karne ki jagah ye attention ke andar hi position ko use karta hai.

Iska fayda:

- relative positions better samajh aati hain
- long-range context handling improve ho sakti hai
- modern transformer designs me bahut common hai


### 19. Loss kya hota hai

Loss batata hai model kitna galat hai.

Agar loss high hai:
model ki prediction weak hai

Agar loss low hai:
model sahi direction me seekh raha hai

Is project me `CrossEntropyLoss` use hui hai,
kyunki next-token prediction classification jaisa problem hota hai.


### 20. Optimizer kya hota hai

Optimizer model ke parameters update karta hai.
Yahan `AdamW` use hua hai.

Simple words me:
loss dekhkar optimizer decide karta hai weights ko kaise badla jaye.

`AdamW` me `weight decay` bhi hota hai.
Weight decay ek regularization method hai jo weights ko bahut uncontrolled grow hone se rokta hai.
Ye overfitting control karne me help karta hai.


### 21. Gradient kya hota hai

Gradient batata hai kis parameter ko kis direction me aur kitna badalna chahiye.

Backpropagation ke baad gradients milte hain.
Optimizer un gradients ka use karke weights update karta hai.


### 22. Gradient Clipping kya hota hai

Kabhi-kabhi gradients bahut bade ho jate hain.
Isse training unstable ho sakti hai.

Gradient clipping un gradients ko limit kar deta hai.

Is project me ye stable training ke liye add kiya gaya hai.


### 23. LR Scheduler kya hota hai

LR ka matlab learning rate.

Learning rate batata hai model har step me kitna bada update kare.

LR scheduler training ke different phases me learning rate change karta hai.
Is project me warmup + cosine decay approach use hui hai.

Iska fayda:

- starting smooth hoti hai
- middle me achhi learning hoti hai
- end me fine adjustment milta hai


### 24. Gradient Accumulation kya hota hai

Gradient accumulation ka matlab:
hum multiple chhote batches ka gradient collect karte hain aur kuch steps baad optimizer update karte hain.

Iska fayda:

- effective batch size bada lagta hai
- kam memory me training possible hoti hai
- training kabhi-kabhi zyada stable ho jaati hai


### 25. Mixed Precision kya hota hai

Mixed precision ka matlab kuch operations lower precision me chalana, jaise `float16`.

Iska fayda:

- GPU memory kam lag sakti hai
- training faster ho sakti hai
- bade batches ya longer runs possible ho sakte hain

Is project me mixed precision safe tarike se `autocast` aur `GradScaler` ke saath use ki gayi hai.


### 26. Data Curriculum kya hota hai

Curriculum learning ka matlab:
model ko pehle easier examples aur baad me harder examples dikhana.

Is project me text chunks ko easy-to-hard order me sort kiya jata hai.

Easy ka heuristic:

- chhote chunks
- kam punctuation
- kam multilingual complexity

Iska fayda:

- model initial phase me jaldi stable hota hai
- learning smoother ho sakti hai
- complex patterns later phase me better absorb hote hain


### 27. Stable Training kya hota hai

Stable training ka matlab:

- loss explode na kare
- gradients control me rahein
- learning rate sensible ho
- overfitting kam ho

Is project me stability ke liye:

- AdamW
- weight decay
- gradient clipping
- gradient accumulation
- LR scheduler
- mixed precision
- curriculum learning
- validation split
- early stopping

use hua hai.


### 28. Top-K Sampling kya hota hai

Generation ke time model bohot saare next-token options deta hai.
Top-K me sirf top K most likely tokens ko consider kiya jata hai.

Isse output random bhi rehta hai aur bahut wild bhi nahi hota.


### 29. Top-P Sampling kya hota hai

Top-P ko nucleus sampling bhi bolte hain.

Isme tokens ko descending probability order me rakhte hain aur utne hi tokens rakhte hain
jinki cumulative probability `p` tak pahunch jaye.

Iska fayda:

- fixed K ki jagah adaptive selection hota hai
- output natural lagta hai


### 30. Repetition Penalty kya hota hai

Generation ke time model kabhi-kabhi same words ko repeat karta rehta hai.
Repetition penalty already used tokens ke logits ko thoda punish karti hai.

Iska fayda:

- output me same word baar-baar aane ka chance kam hota hai
- response thoda zyada varied lagta hai


### 31. Mirostat kya hota hai

Mirostat ek adaptive sampling method hai.
Ye output ki randomness ko ek target surprise level ke around maintain karne ki koshish karta hai.

Simple words me:
Top-k aur top-p static rules hain.
Mirostat dynamic rule hai jo har next token ke baad apna behavior adjust karta hai.

Iska fayda:

- output overly boring bhi nahi hota
- output overly random bhi nahi hota
- long generation me quality kabhi-kabhi zyada stable lag sakti hai


### 32. KV Cache kya hota hai

KV cache ka matlab key-value cache.

Attention generation ke time har naya token aane par purana context dubara compute karta hai.
KV cache purane key aur value tensors store kar leta hai.

Iska fayda:

- generation fast hoti hai
- har token par poora prompt dubara run nahi karna padta
- especially long generation me speed improvement milta hai


### 33. Beam Search kya hota hai

Beam search ek decoding method hai jo ek hi next token sample karne ki jagah multiple candidate sequences track karta hai.

Iska fayda:

- output zyada deterministic ho sakta hai
- best-scoring sentence choose ki ja sakti hai
- Q&A ya formal response me kabhi-kabhi useful hota hai


### 34. INT8 Quantization kya hota hai

INT8 quantization ka matlab model ke kuch weights ko 32-bit float ki jagah 8-bit integer format me store karna.

Is project me dynamic INT8 quantization use hoti hai, mainly `Linear` layers par.

Iska fayda:

- model chhota ho jata hai
- CPU par inference faster ho sakta hai
- model share karna easy hota hai

Important:
Ye mostly inference optimization hai, training optimization nahi.


### 35. FastAPI kya hota hai

FastAPI Python ka ek modern web framework hai jo APIs banane ke liye use hota hai.

Iska fayda:

- code simple hota hai
- automatic docs milti hain
- JSON request/response support milta hai
- portfolio aur real-world demo ke liye bahut useful hai


### 36. REST API kya hota hai

REST API ek tarika hai jisme aap HTTP requests ke through model se baat karte ho.

Example:

- `POST /generate`
- `GET /health`
- `GET /model-info`

Iska fayda:

- website app backend ya mobile app se connect kar sakte ho
- local model ko service ki tarah expose kar sakte ho


### 37. BLEU score kya hota hai

BLEU ek text-overlap metric hai jo dekhta hai generated answer aur reference answer me kitna n-gram match ho raha hai.

Simple words me:

- BLEU high ho to wording overlap zyada hai
- BLEU low ho to generated answer reference se kaafi different hai

Important:
BLEU meaning ka perfect judge nahi hota.
Kabhi answer sahi ho sakta hai lekin wording different hone ki wajah se BLEU low aa sakta hai.


### 38. Perplexity kya hota hai

Perplexity batata hai next token predict karne me model kitna confused hai.

Simple rule:

- lower perplexity = model zyada confident aur better predictor
- higher perplexity = model zyada confused

Language model evaluation me perplexity bahut common metric hai,
especially jab hum dekhna chahte hain ki model raw text ko kitna achha model kar raha hai.


### 39. Fine-tuning kya hota hai

Fine-tuning ka matlab base model ko ek specific kaam ke liye aur train karna.

Yahan:
base language model ko 50 Q&A pairs par fine-tune kiya gaya hai
taaki wo direct question-answer pattern seekhe.


### 40. Q&A Fine-tuning ka kya fayda

Base model general text continuation me acha ho sakta hai,
lekin direct jawab dene me weak ho sakta hai.

Q&A fine-tuning ke baad model:

- prompt ko sawal ke roop me dekhna seekhta hai
- concise answer format me respond karna seekhta hai
- repetitive text continuation se thoda nikalta hai


### 41. RLHF kya hota hai

RLHF ka full form hai Reinforcement Learning from Human Feedback.

Industry me RLHF pipeline generally kuch is tarah hoti hai:

1. base model
2. supervised fine-tuning
3. human preference data
4. reward model
5. PPO ya kisi RL algorithm se optimization


### 42. Is project me RLHF kaunsa use hua hai

Is project me full industrial PPO RLHF nahi hai.
Yahan ek simplified RLHF-style preference tuning stage hai.

Hum chosen vs rejected answers use karke model ko sikhate hain:

- kaunsi response better hai
- kaunsi response vague ya wrong hai

Ye learning purpose ke liye practical aur samajhne layak version hai.


### 43. Preference Data kya hota hai

Preference data me ek prompt ke liye do answers hote hain:

- chosen = better answer
- rejected = weak answer

Model ko train kiya jata hai ki chosen answer ko zyada score de.


## Har Script Kya Karti Hai

### `train.py`

Ye script:

- `data.txt` padhti hai
- byte-level BPE tokenizer build karti hai
- data curriculum apply karti hai
- base model train karti hai
- AdamW + weight decay use karti hai
- gradient clipping use karti hai
- gradient accumulation use karti hai
- LR scheduler chalati hai
- mixed precision support rakhti hai
- best checkpoint save karti hai


### `fine_tune.py`

Ye script:

- base model load karti hai
- `qa_pairs.json` padhti hai
- supervised Q&A fine-tuning karti hai
- model ko direct answers ki taraf shift karti hai


### `rlhf.py`

Ye script:

- fine-tuned model se start karti hai
- `preference_pairs.json` padhti hai
- chosen vs rejected response scoring use karti hai
- behavior alignment improve karti hai


### `generate.py`

Ye script:

- best available model load karti hai
- RLHF model mile to usse prefer karti hai
- top-k aur top-p ke saath generation karti hai
- Mirostat mode bhi support karti hai
- repetition penalty use karti hai
- KV cache se fast generation karti hai
- beam search mode bhi support karti hai
- interactive chat mode chalati hai


### `evaluate.py`

Ye script:

- best available model load karti hai
- `data.txt` ke holdout tokens par perplexity nikalti hai
- `qa_pairs.json` par BLEU score nikalti hai
- sample predictions print karti hai
- evaluation ko numbers ke through samajhne me help karti hai


### `quantize.py`

Ye script:

- best trained model load karti hai
- dynamic INT8 quantization apply karti hai
- compact checkpoint save karti hai
- original aur quantized size compare karti hai


### `api.py`

Ye script:

- FastAPI server banati hai
- `/health` endpoint deti hai
- `/model-info` endpoint deti hai
- `/generate` endpoint deti hai
- quantized ya non-quantized model serve kar sakti hai


## Kaunsi `.md` File Se Kya Sikh Sakte Ho

Ye section specially docs ke liye hai.
Yani agar aap code ke saath-saath explanation files bhi padhna chahte ho,
to yahan se samajh jaoge kis markdown file me kya milega.


### `SusaGPT_Architecture.md`

Is file me aap seekh sakte ho:

- SusaGPT architecture-wise kahan stand karta hai
- GPT-2, LLaMA 3 aur GPT-4 se iska difference kya hai
- modern architecture blocks ka importance kya hai
- scale aur architecture me kya farq hota hai
- honest technical comparison kaise likha jata hai


### `SusaGPT_Skills.md`

Is file me aap seekh sakte ho:

- is project ko samajhne ke baad kaunsi skills milti hain
- tokenizer, transformer, training, fine-tuning, RLHF aur deployment se kya learning nikalti hai
- kaunse roles ke liye ye project useful ho sakta hai
- beginner se intermediate AI engineer mindset kaise develop hota hai


### `SusaGPT_Diagram_Guide.md`

Is file me aap seekh sakte ho:

- diagrams ki help se SusaGPT ka poora visual flow
- tokenizer se generation tak end-to-end system kaise kaam karta hai
- attention, GQA, RoPE, RMSNorm, SwiGLU jaise blocks visually kaise samjhe ja sakte hain
- training, fine-tuning, RLHF, evaluation aur API ko visual tarike se kaise samjha jata hai


### `MCP_Guide.md`

Is file me aap seekh sakte ho:

- MCP yani Model Context Protocol kya hota hai
- host, client aur server architecture kaise kaam karti hai
- tools, resources aur prompts ka role kya hota hai
- MCP server kaise build hota hai
- MCP ke liye kaunsi skills aur learning resources useful hain


### `AI_Agents_Guide.md`

Is file me aap seekh sakte ho:

- AI agent kya hota hai
- chatbot aur AI agent me difference kya hota hai
- tools, memory, planning aur execution loop ka role kya hota hai
- multi-agent ya multi-AI-agent systems kya hote hain
- agent build karne ke liye kaunse frameworks aur concepts useful hain


### `Agentic_AI_Guide.md`

Is file me aap seekh sakte ho:

- agentic AI kya hota hai
- generative AI aur agentic AI me relation aur difference kya hai
- autonomy, planning, reflection aur feedback loop ka role kya hota hai
- agentic systems ki architecture kaise sochi jati hai
- student ko agentic AI seekhne ke liye kya path follow karna chahiye


## Kya Sikhne Ko Milega

Is project se aap ye cheezein practically samajh sakte ho:

- tokenizer kya hota hai
- BPE tokenizer ka basic flow kya hota hai
- transformer model ka basic flow kya hota hai
- embeddings aur positional encoding ka role
- attention, multi-head attention aur GQA ka kaam
- SwiGLU, dropout, RMSNorm aur RoPE ka effect
- weight tying ka use
- stable training ke liye AdamW, weight decay, gradient clipping, gradient accumulation, LR scheduler aur curriculum
- mixed precision ka practical use
- Mirostat sampling ka purpose
- BLEU score aur perplexity ka role
- INT8 quantization ka inference benefit
- FastAPI aur REST API ka practical role
- supervised fine-tuning ka purpose
- preference-based RLHF-style tuning ka idea
- top-k, top-p, repetition penalty, KV cache aur beam search ka impact
- checkpoint save/load flow
- MCP ka basic architecture
- AI agents aur multi-agent systems ka core idea
- agentic AI aur generative AI ke beech ka difference


## Important Notes

- Tokenizer byte-level BPE hai, word-level tokenizer nahi.
- Old `tokenizer.json` ko naye code ke saath regenerate karna zaruri hai.
- Purane model checkpoints ko ideally dubara train karna chahiye, kyunki tokenizer aur architecture dono change ho chuke hain.
- Quantized model mainly CPU inference ke liye useful hai.
- FastAPI run karne ke liye `fastapi` aur `uvicorn` installed hone chahiye.
- RLHF implementation simplified hai, full production PPO pipeline nahi.
- Q&A aur preference data learning/demo purpose ke liye curated hai.
- Ye project educational understanding ke liye strong hai, production-ready full stack nahi.


## Recommended Order

Best understanding ke liye files ko is order me padho:

1. `tokenizer.py`
2. `model.py`
3. `config.py`
4. `train.py`
5. `fine_tune.py`
6. `rlhf.py`
7. `generate.py`
8. `evaluate.py`
9. `SusaGPT_Architecture.md`
10. `SusaGPT_Diagram_Guide.md`
11. `SusaGPT_Skills.md`
12. `MCP_Guide.md`
13. `AI_Agents_Guide.md`
14. `Agentic_AI_Guide.md`


## Credit

sameer malik
