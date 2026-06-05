import sentencepiece as spm

# Train the tokenizer
spm.SentencePieceTrainer.train(
    input="data.txt",
    model_prefix="my_tokenizer",
    vocab_size=30,  # Reduced from 100 because data.txt is very small, or use hard_vocab_limit=False
    model_type="unigram"   # ya "bpe"
)

# Load and test the trained tokenizer
sp: spm.SentencePieceProcessor = spm.SentencePieceProcessor()
sp.load("my_tokenizer.model")
# for i in range(50):
#     print(i, "->", sp.id_to_piece(i))
text = "my name is sameer"

tokens = sp.encode_as_pieces(text)
ids = sp.encode_as_ids(text)

print("Tokens:")
print(tokens)

print("\nIDs:")
print(ids)

decoded = sp.decode_ids(ids)

print("\nDecoded:")
print(decoded)

# from tokenizers import ByteLevelBPETokenizer

# # Initialize
# tokenizer = ByteLevelBPETokenizer()

# # Train on some data
# tokenizer.train(files=["data.txt"], vocab_size=5000, min_frequency=2)
# vocab = tokenizer.get_vocab()
# # Encode
# output = tokenizer.encode("First, you know Caius Marcius is chief enemy to the people.")
# print(output.tokens)
# print(output.ids)
# decode = tokenizer.decode(output.ids)
# print(decode)
# print("vocab ",tokenizer.get_vocab_size())
# print("tokens ",len(output.tokens))
# Output: ['Hello', 'Ġworld', '!'] (Ġ represents a space)

# In production, use pre-trained tokenizers from HuggingFace

#Text
#↓
#Tokenizer (BPE)
#↓
#Tokens

# ["I","love","AI"]

# ↓
# Token IDs

# [5,12,89]

# ↓
# Embedding Layer

# [
#  [0.25,0.81,...],
#  [0.51,-0.22,...],
#  [0.11,0.62,...]
# ]

# ↓
# Transformer

# (Self Attention)

# ↓
# Linear Layer

# ↓
# Softmax

# ↓
# Next Token Prediction