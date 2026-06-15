# 🏛️ SusaGPT — Production Ready Tiny LLM

SusaGPT ek custom **Tiny Language Model** hai jo **SusaLabs** ke official dataset (Company info, AI services, custom software, CRM systems, and healthcare platforms) par trained hai. Yeh model fully self-contained, CPU-optimized aur edge-deployment ready hai.

---

## 📂 Production Folder Structure

Humne project ko ek clean industrial standard structure mein organize kiya hai:

```
susagpt/
├── data/
│   ├── data.txt                # SusaLabs pretraining corpus (573 lines)
│   ├── qa_pairs.json           # Fine-tuning QA pairs
│   └── preference_pairs.json   # RLHF preference pairs
├── src/                        # Core Model & Tokenizer implementation
│   ├── __init__.py
│   ├── config.py               # Hyperparameters and paths
│   ├── model.py                # PyTorch Transformer Architecture (RoPE, GQA, SwiGLU)
│   ├── tokenizer.py            # Custom Byte-level BPE Tokenizer
│   ├── generate.py             # Inference engine (Mirostat, Top-k, Top-p, KV cache)
│   └── api.py                  # FastAPI REST Server
├── scripts/                    # Runnable scripts for training/deployment
│   ├── train.py                # Pretraining entrypoint (Curriculum Learning)
│   ├── fine_tune.py            # Supervised Fine-Tuning (SFT)
│   ├── rlhf.py                 # RLHF-style alignment (Preference tuning)
│   ├── quantize.py             # PyTorch Dynamic INT8 Quantization
│   └── export_onnx.py          # ONNX graph export & ONNX INT8 Quantization
├── cli.py                      # Production CLI (Single Q, Interactive, Benchmark)
├── requirements.txt            # Python dependencies
└── README.md                   # Yeh documentation file
```

---

## 🛠️ Advanced Techniques & Real-World Model Mapping

Humne SusaGPT mein woh saare modern architecture patterns aur optimization techniques use kiye hain jo LLaMA, Gemma, aur GPT-4 jaise modern open/closed source models mein use hote hain.

Niche table mein in techniques, unka real-world mapping, and exact code files with line numbers ki details hain:

| Technique | Kis Model Mein Use Hota Hai | File Path | Code Line (Line Range) | Explanation |
| :--- | :--- | :--- | :--- | :--- |
| **Rotary Position Embeddings (RoPE)** | LLaMA 1/2/3, Mistral, Gemma, Qwen | [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py) | **Line 27–40** (`RotaryEmbedding`) & **Line 49–54** (`apply_rotary_pos_emb`) | Absolute position embeddings (like Sinusoidal) ke bajaye relative distance sequence positions compute karne ke liye query/key pairs rotate karta hai. |
| **Grouped Query Attention (GQA)** | LLaMA 2 (70B), LLaMA 3, Mistral | [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py) | **Line 66–153** (`SelfAttention` class init & forward) | Query heads ko split karta hai and Key/Value heads ko compress karta hai (KV repeat). Isse memory bandwidth aur cache requirements reduce hoti hain. |
| **SwiGLU Activation Function** | LLaMA, PaLM, Gemma | [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py) | **Line 156–174** (`SwiGLUFeedForward`) | Standard ReLU ya GELU ke badle Swish (SiLU) gate activation function use karta hai jo linear projections ko multiply karke representational capacity badhata hai. |
| **RMSNorm** | LLaMA, Gemma, Mistral | [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py) | **Line 14–24** (`RMSNorm`) | LayerNorm se faster normalizing technique jo bina mean calculation ke direct root-mean-square coordinate variance scale par normalize karti hai. |
| **LoRA (Low-Rank Adaptation)** | LLaMA 1/2/3, Gemma, GPT-4 (PEFT) | [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py), [`susagpt/scripts/fine_tune.py`](file:///c:/Projects/MyLLM/susagpt/scripts/fine_tune.py), [`susagpt/scripts/rlhf.py`](file:///c:/Projects/MyLLM/susagpt/scripts/rlhf.py) | **model.py: Line 263-350**, **fine_tune.py: Line 275-285**, **rlhf.py: Line 105-110** | Base model parameters freeze karke attention (W_q, W_v) aur FFN (w1, w3) layers ke parallel low-rank (r=8) trainable matrices ($A$ aur $B$) use karta hai, jisse training parameters 90%+ reduce hote hain. Training ke baad weights merge ho jate hain zero inference latency ke liye. |
| **Byte-level BPE Tokenization** | GPT-2, GPT-3/4, LLaMA, Gemma | [`susagpt/src/tokenizer.py`](file:///c:/Projects/MyLLM/susagpt/src/tokenizer.py) | **Line 38–256** (`Tokenizer` class, `build_vocab`, `encode`, `decode`) | Character ya word level ke bajaye byte sequences par split karke merges training karta hai. Isse unknown tokens (`<UNK>`) handle nahi karne padte aur multilingual/code format support milta hai. |
| **Curriculum Learning** | GPT-4, LLaMA 3 | [`susagpt/scripts/train.py`](file:///c:/Projects/MyLLM/susagpt/scripts/train.py) | **Line 72–106** (`split_into_curriculum_chunks` & `build_curriculum_text`) | Dataset mein simple and short sentences ko pehle, aur complex/punctuated sentences ko baad mein sort karke train karta hai, taaki model stable learn kare. |
| **RLHF-style Preference Tuning** | InstructGPT, ChatGPT, LLaMA 2/3-Chat | [`susagpt/scripts/rlhf.py`](file:///c:/Projects/MyLLM/susagpt/scripts/rlhf.py) | **Line 50–74** (`average_answer_logprob`) & **Line 134–138** (Pairwise loss sigmoid optimization) | chosen (pasandida) answer ki probability badhata hai aur rejected answer ki weightage kam karta hai using logits sigmoid gap loss. |
| **INT8 Dynamic Quantization** | LLaMA.cpp, PyTorch Mobile Deployments | [`susagpt/src/generate.py`](file:///c:/Projects/MyLLM/susagpt/src/generate.py) | **Line 33–45** (`apply_dynamic_int8_quantization`) | Float32 weight tensors ko 8-bit integers mein convert karke CPU model footprints size ko 4x small aur fast compute-intensive banata hai. |
| **Mirostat Sampling** | LLaMA.cpp (local/edge devices engine) | [`susagpt/src/generate.py`](file:///c:/Projects/MyLLM/susagpt/src/generate.py) | **Line 185–218** (`sample_with_mirostat`) | Next-token selection ke variance / surprise rate ko target parameter "tau" ke around dynamic control deta hai taaki loop repetitions ya generic generation avoid ho sake. |
| **ONNX Runtime Graph Export** | TensorRT, WebNN WebGPU Deployment, edge servers | [`susagpt/scripts/export_onnx.py`](file:///c:/Projects/MyLLM/susagpt/scripts/export_onnx.py) | **Line 56–78** (`export_onnx`) & **Line 80–100** (`quantize_onnx`) | PyTorch weights dependencies hatakar universal computation model output format export karta hai jo dynamic batch axis aur quantized engine optimization support karta hai. |

---

## 📚 Complete LLM Learning Mapping (llm_learning Catalog)

SusaGPT, [`docs/llm_learning/`](file:///c:/Projects/MyLLM/docs/llm_learning) roadmap ke saare theoretical aur design concepts ko practically implement karne ke liye ek playground hai. Niche har module ka real-world GPT connection aur SusaGPT me iska direct implementation files aur line numbers ke sath detail me mapped hai:

### 1. [00_Foundations_and_Roadmap](file:///c:/Projects/MyLLM/docs/llm_learning/00_Foundations_and_Roadmap)
* **Real-World GPT Context**: Real-world GPT models ko maintain karne ke liye production-ready modular folder structure aur parameters configurations ko isolate karna critical hota hai taaki codebase readable aur scalable rahe.
* **SusaGPT Implementation**:
  * **Production Directory Layout**: Data processing (`susagpt/data`), core components (`susagpt/src`), and pipeline run scripts (`susagpt/scripts`) alag-alag directories me organize kiye gaye hain.
  * **Hyperparameters Config Isolation**: Model architectures (vocab size, layer count, embed dims) aur optimizer configs (learning rate, weight decay) isolated hain [`susagpt/src/config.py`](file:///c:/Projects/MyLLM/susagpt/src/config.py) me **Lines 1–48** par.

### 2. [01_Mathematics_for_AI_and_LLMs](file:///c:/Projects/MyLLM/docs/llm_learning/01_Mathematics_for_AI_and_LLMs)
* **Real-World GPT Context**: GPT models me weights updates stabilize karne ke liye mathematical optimizers, learning rate scheduling (warmups & decay), aur exploding gradients control karna mandatory hota hai.
* **SusaGPT Implementation**:
  * **AdamW Optimizer**: Weights update ke time weight decay implement karta hai taaki overfitting reduce ho sake. Used in [`susagpt/scripts/train.py`](file:///c:/Projects/MyLLM/susagpt/scripts/train.py#L159-L163), [`susagpt/scripts/fine_tune.py`](file:///c:/Projects/MyLLM/susagpt/scripts/fine_tune.py#L142-L146), and [`susagpt/scripts/rlhf.py`](file:///c:/Projects/MyLLM/susagpt/scripts/rlhf.py#L114-L118) me.
  * **Cosine Annealing with Warmup**: Start steps me learning rate control and stabilize karta hai. Implemented inside `build_scheduler` inside [`susagpt/scripts/train.py`](file:///c:/Projects/MyLLM/susagpt/scripts/train.py#L113-L124).
  * **Gradient Clipping**: Large loss values ke gradients ko threshold clamp dekar loss divergence control karta hai. Implemented using `clip_grad_norm_` inside [`susagpt/scripts/train.py`](file:///c:/Projects/MyLLM/susagpt/scripts/train.py#L229-L231), [`susagpt/scripts/fine_tune.py`](file:///c:/Projects/MyLLM/susagpt/scripts/fine_tune.py#L204-L206), and [`susagpt/scripts/rlhf.py`](file:///c:/Projects/MyLLM/susagpt/scripts/rlhf.py#L150-L152).

### 3. [02_Python_and_Software_Engineering](file:///c:/Projects/MyLLM/docs/llm_learning/02_Python_and_Software_Engineering)
* **Real-World GPT Context**: Core models ko client applications me serve karne ke liye high-performance async APIs design kiye jate hain, aur pipelines execution speeds (latency, tokens-per-second) benchmark results generate karte hain.
* **SusaGPT Implementation**:
  * **FastAPI Server Endpoint**: Async API integration web requests serve karne ke liye inside [`susagpt/src/api.py`](file:///c:/Projects/MyLLM/susagpt/src/api.py) on **Lines 1–85**.
  * **Benchmarking Pipeline**: Execution loops latency profile aur tokens-per-second performance metrics output checks inside [`susagpt/cli.py`](file:///c:/Projects/MyLLM/susagpt/cli.py#L168-L230), jo `benchmark_results.json` write karta hai.

### 4. [03_Machine_Learning_Foundations](file:///c:/Projects/MyLLM/docs/llm_learning/03_Machine_Learning_Foundations)
* **Real-World GPT Context**: Language model prediction metrics assess karne ke liye prediction target outputs loss functions evaluate karne padte hain, aur training runtime monitor karke overfitting prevent karni hoti hai.
* **SusaGPT Implementation**:
  * **Cross-Entropy Loss**: Next token predictions divergence loss check karne ke liye output calculation inside [`susagpt/scripts/train.py`](file:///c:/Projects/MyLLM/susagpt/scripts/train.py#L164) and [`susagpt/scripts/fine_tune.py`](file:///c:/Projects/MyLLM/susagpt/scripts/fine_tune.py#L147).
  * **Validation Early Stopping**: Training status flags evaluation (jaise `overfit⚠`, `stable✓`, `watch` logs) monitoring and patience bounds checks inside [`susagpt/scripts/train.py`](file:///c:/Projects/MyLLM/susagpt/scripts/train.py#L268-L279,L285-L293) and [`susagpt/scripts/fine_tune.py`](file:///c:/Projects/MyLLM/susagpt/scripts/fine_tune.py#L244-L252).

### 5. [04_Deep_Learning_Foundations](file:///c:/Projects/MyLLM/docs/llm_learning/04_Deep_Learning_Foundations)
* **Real-World GPT Context**: Multi-Layer Perceptrons (MLP) representations coordinate spaces mapping handle karte hain, aur dropout layer layers ke random drop connections create karke neural networks co-adaptation block karti hai.
* **SusaGPT Implementation**:
  * **MLP Block**: Projection dimension spaces map setup in `SwiGLUFeedForward` class in [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py#L156-L174).
  * **Dropout Layers**: Attention maps weight drops and output dropout inside `SelfAttention` on **Lines 91–92** and `SusaGPT` forward projection on **Line 224** inside [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py).

### 6. [05_NLP_Fundamentals_and_Tokenization](file:///c:/Projects/MyLLM/docs/llm_learning/05_NLP_Fundamentals_and_Tokenization)
* **Real-World GPT Context**: Sub-word tokenizer text ko representation indexes integer format maps me split karta hai taaki vocabulary bounds set rahein, aur Embeddings unhe numerical parameter space me convert karti hain.
* **SusaGPT Implementation**:
  * **Byte-level BPE Tokenizer**: Unicode character bytes merge merges logic sequence build and vocabulary construct karne ke liye inside [`susagpt/src/tokenizer.py`](file:///c:/Projects/MyLLM/susagpt/src/tokenizer.py) via `Tokenizer` on **Lines 38–256**.
  * **Token Embeddings Layer**: Character mappings high-dimension dimensions projections mapping inside `EmbeddingLayer` inside [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py#L57-L63).

### 7. [06_Transformer_Architecture_From_Scratch](file:///c:/Projects/MyLLM/docs/llm_learning/06_Transformer_Architecture_From_Scratch)
* **Real-World GPT Context**: Modern decoders architectures (LLaMA family) core mathematical block components check karti hain: RMSNorm layers normalize fast calculation steps, RoPE encodes distances parameters, and GQA optimizes inference.
* **SusaGPT Implementation**:
  * **RMSNorm**: Faster normalization logic without mean division operations on **Lines 14–24** of [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py).
  * **Rotary Position Embeddings (RoPE)**: positional coordinate values queries-keys rotate layers mapping in `RotaryEmbedding` class on **Lines 27–40** and `apply_rotary_pos_emb` function on **Lines 49–54** of [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py).
  * **Grouped Query Attention (GQA)**: KV head dimension repeats and query heads attention scoring matrices inside `SelfAttention` class on **Lines 66–153** of [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py).
  * **SwiGLU Activation Function**: Multiplies gate activated branch maps FFN projections inside `SwiGLUFeedForward` class on **Lines 156–174** of [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py).
  * **Causal Masking**: Future token predictions block outputs set to `-inf` on **Lines 137–142** of [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py).

### 8. [07_Modern_LLMs_and_Scaling_Laws](file:///c:/Projects/MyLLM/docs/llm_learning/07_Modern_LLMs_and_Scaling_Laws)
* **Real-World GPT Context**: Hardware memory constraints check karke dimensions parameters allocation optimize karne ke liye design ratios control kiye jate hain.
* **SusaGPT Implementation**:
  * **Parameter Budget Optimization**: Vocabulary tokens target limit, hidden embedding steps, block sequence layer depths optimize settings inside [`susagpt/src/config.py`](file:///c:/Projects/MyLLM/susagpt/src/config.py#L38-L47).

### 9. [08_LLM_Training_and_Data_Engineering](file:///c:/Projects/MyLLM/docs/llm_learning/08_LLM_Training_and_Data_Engineering)
* **Real-World GPT Context**: Autoregressive next-token training targets pretraining loops run setup maps data prepare, aur initial model cycles start simple data chunks sorting steps se stable learn karte hain.
* **SusaGPT Implementation**:
  * **Dataset Loader**: `TextDataset` offsets inputs/targets next token tensors sequence generation inside [`susagpt/scripts/train.py`](file:///c:/Projects/MyLLM/susagpt/scripts/train.py#L59-L73).
  * **Curriculum Learning Chunks**: text length metrics score sequence analysis aur complexity parameters sort mapping inside [`susagpt/scripts/train.py`](file:///c:/Projects/MyLLM/susagpt/scripts/train.py#L76-L110).

### 10. [09_Fine_Tuning_and_Alignment](file:///c:/Projects/MyLLM/docs/llm_learning/09_Fine_Tuning_and_Alignment)
* **Real-World GPT Context**: Base model fine-tuning outputs check instruct responses build karta hai, aur preference mapping selected choices probability sigmoid gaps maximize alignment setups detaye hain.
* **SusaGPT Implementation**:
  * **LoRA PEFT implementation**: base linear layers lock checks, custom parameter projections adapters update parameters logic (`LoRAParameterizedLinear`, `inject_lora`, and weights merging `merge_and_unload_lora`) inside [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py#L266-L352).
  * **SFT instruction tuning**: Q&A training loop loading datasets directly formatting responses via `QADataset` inside [`susagpt/scripts/fine_tune.py`](file:///c:/Projects/MyLLM/susagpt/scripts/fine_tune.py#L84-L118).
  * **RLHF Preference Sigmoid Gaps Tuning**: chosen vs rejected logprob reward gap sigmoid loss backpropagation inside [`susagpt/scripts/rlhf.py`](file:///c:/Projects/MyLLM/susagpt/scripts/rlhf.py#L127-L160).

### 11. [10_RAG_and_Vector_Databases](file:///c:/Projects/MyLLM/docs/llm_learning/10_RAG_and_Vector_Databases)
* **Real-World GPT Context**: Real-time context information prompt integration through keyword queries, vectors indexing, and database lookups checks hallucination reduction detaye hain.
* **SusaGPT Implementation**:
  * **Keyword/TF-IDF Context matching**: Overlap scoring calculations inputs check to pick relevant document lines on **Lines 672–707** of [`susagpt/src/generate.py`](file:///c:/Projects/MyLLM/susagpt/src/generate.py).

### 12. [11_Inference_and_Optimization](file:///c:/Projects/MyLLM/docs/llm_learning/11_Inference_and_Optimization)
* **Real-World GPT Context**: Model output fast decode generation loops key-value cache buffer optimize keye jate hain, sampling outputs temperatures scale adjustments target filter parameters apply checks karte hain, aur deployment steps memory size compression dynamic quantization operations support format detaya hai.
* **SusaGPT Implementation**:
  * **Key-Value (KV) Cache**: Query updates calculations reduction logic self-attention models inside [`susagpt/src/model.py`](file:///c:/Projects/MyLLM/susagpt/src/model.py#L120-L126) and generate runs on **Lines 242–303** of [`susagpt/src/generate.py`](file:///c:/Projects/MyLLM/susagpt/src/generate.py).
  * **Autoregressive sampling settings**: logits top-k/top-p filters, repetition penalty adjustments, Mirostat v2 adaptive surprise mu checks inside [`susagpt/src/generate.py`](file:///c:/Projects/MyLLM/susagpt/src/generate.py#L153-L220).
  * **Beam Search**: candidate paths logs probabilities scoring updates evaluation inside [`susagpt/src/generate.py`](file:///c:/Projects/MyLLM/susagpt/src/generate.py#L335-L372).
  * **Model Weights Quantization**: PyTorch Dynamic INT8 conversions of Linear operators inside [`susagpt/src/generate.py`](file:///c:/Projects/MyLLM/susagpt/src/generate.py#L36-L48) and [`susagpt/scripts/quantize.py`](file:///c:/Projects/MyLLM/susagpt/scripts/quantize.py#L35-L55).

### 13. [12_MLOps_LLMOps_and_Infrastructure](file:///c:/Projects/MyLLM/docs/llm_learning/12_MLOps_LLMOps_and_Infrastructure)
* **Real-World GPT Context**: Cross-platform deployment me PyTorch models dependencies universal runtime formats (jaise ONNX dynamic graphs) compilation pipelines output optimize detaye hain.
* **SusaGPT Implementation**:
  * **ONNX universal format graph export & quantization**: computation model exports aur ONNX quantization operations inside [`susagpt/scripts/export_onnx.py`](file:///c:/Projects/MyLLM/susagpt/scripts/export_onnx.py#L56-L100).

### 14. [13_Production_Systems_and_Agents](file:///c:/Projects/MyLLM/docs/llm_learning/13_Production_Systems_and_Agents)
* **Real-World GPT Context**: AI Agent configurations input query analysis routing, dialog patterns recognition, local databases check, and API fallbacks handle structures check framework design keye jate hain.
* **SusaGPT Implementation**:
  * **Conversational Agent router fallback loop**: greetings mapping check, local contexts evaluation, Ollama servers request forwarding fallback, Cloud APIs endpoints routing loops inside [`susagpt/src/generate.py`](file:///c:/Projects/MyLLM/susagpt/src/generate.py#L610-L879).

### 15. [14_Model_Evaluation_and_Benchmarking](file:///c:/Projects/MyLLM/docs/llm_learning/14_Model_Evaluation_and_Benchmarking)
* **Real-World GPT Context**: model prediction quality check aur latency statistics benchmark reports log verify checks compile jate hain.
* **SusaGPT Implementation**:
  * **Automated Benchmarks runner**: CLI evaluation on standard prompt lists testing profiling stats logging inside [`susagpt/cli.py`](file:///c:/Projects/MyLLM/susagpt/cli.py#L168-L230).

### 16. [15_AI_Security_and_Safety](file:///c:/Projects/MyLLM/docs/llm_learning/15_AI_Security_and_Safety)
* **Real-World GPT Context**: predictable defaults context safe fallback maps secure bounds execution boundaries setups verify logic apply calculations karte hain.
* **SusaGPT Implementation**:
  * **Graceful fallback exception maps routing**: connection checks wrapper inside [`susagpt/src/generate.py`](file:///c:/Projects/MyLLM/susagpt/src/generate.py) crash controls optimize settings.

### 17. [16_Open_Source_Ecosystem_and_Local_LLMs](file:///c:/Projects/MyLLM/docs/llm_learning/16_Open_Source_Ecosystem_and_Local_LLMs)
* **Real-World GPT Context**: Local environments local models integration interfaces (Ollama hosting setups) local requests serve checks design format setups detaye hain.
* **SusaGPT Implementation**:
  * **Ollama local request client API**: localhost requests micro-services connection setups for `qwen3.5:0.8b` fallback models inside [`susagpt/src/generate.py`](file:///c:/Projects/MyLLM/susagpt/src/generate.py#L717-L745).

### 18. [17_Multimodal_LLMs](file:///c:/Projects/MyLLM/docs/llm_learning/17_Multimodal_LLMs)
* **Real-World GPT Context**: Multimodal features integration coordinates sequence spaces mapping coordinate values layers projections parameters setups understand maps check pipelines define karta hai.
* **SusaGPT Implementation**:
  * **Structural blueprint mappings**: Token configurations embeddings, linear projection scaling layers, cross-attention networks architecture foundations mapping.

### 19. [18_Case_Studies_and_Hands_On_Projects](file:///c:/Projects/MyLLM/docs/llm_learning/18_Case_Studies_and_Hands_On_Projects)
* **Real-World GPT Context**: conceptual designs practical implementations code formats convert systems deployment workflows demonstrate details.
* **SusaGPT Implementation**:
  * **Production mini-LLM implementation repository**: GQA, RoPE, LoRA PEFT, RLHF alignment features merged pipeline codebase architecture sandbox.

### 20. [19_Interview_Preparation](file:///c:/Projects/MyLLM/docs/llm_learning/19_Interview_Preparation)
* **Real-World GPT Context**: engineering system designs, layer norm operations advantages calculation, parameters math scale analysis technical checks verify patterns maps target checks define jate hain.
* **SusaGPT Implementation**:
  * **Interview Design Sandboxing**: Working implementation reference portfolio verify questions calculations direct in code layers.

---


## 🚀 How to Run the Pipeline (Commands)

Aap in commands ko step-by-step terminal mein run karke model complete train aur deployment verify kar sakte hain:

### 1. Requirements Install Karein
```bash
pip install -r susagpt/requirements.txt
```

### 2. Base Model Training (Pretraining)
```bash
python susagpt/scripts/train.py
```
*Yeh SusaLabs core corpus `susagpt/data/data.txt` par curriculum pretraining shuru karega.*

### 3. Supervised Fine-Tuning (SFT)
```bash
python susagpt/scripts/fine_tune.py
```
*Yeh checkpoint load karke model ko QA pairs `susagpt/data/qa_pairs.json` ke corresponding direct response sikhayega.*

### 4. RLHF Alignment (Preference Tuning)
```bash
python susagpt/scripts/rlhf.py
```
*Yeh chosen vs rejected preference pair behavior sikhakar answer quality enhance karega.*

### 5. CPU Weight Quantization (PyTorch INT8)
```bash
python susagpt/scripts/quantize.py
```
*Trained model ko dynamic 8-bit integers compress target format `SusaGPT-int8.pt` mein save karega.*

### 6. ONNX Export aur Quantization (Mobile/Edge Deployment)
```bash
python susagpt/scripts/export_onnx.py
```
*Yeh full precision ONNX model (`SusaGPT.onnx`) aur quantized dynamic INT8 model (`SusaGPT_quantized.onnx`) generate karega.*

---

## 🤖 Production CLI Interface Usage

Humne ek advanced production-grade CLI built kiya hai jisse aap models benchmark aur test kar sakte hain:

### A. Ask a Single Question
```bash
python susagpt/cli.py --question "what does susalabs do"
```

### B. Interactive Chat Mode (type 'quit' to exit)
```bash
python susagpt/cli.py --interactive
```

### C. Run the Production 10-Question Benchmark
```bash
python susagpt/cli.py --benchmark
```
*Yeh benchmark model ko 10 different company queries par check karke execution timestamps analyze karega aur `benchmark_results.json` output file save karega.*

### D. Force Use Base Model (For comparing SFT/RLHF upgrades)
```bash
python susagpt/cli.py --question "what services does susalabs offer" --base
```
