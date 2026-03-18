import json
import re

from .config import DATA_PATH, TOKENIZER_CONFIG, TOKENIZER_PATH


# Ye tokenizer ab simple word-level tokenizer nahi hai.
# Ab hum byte-level BPE (Byte Pair Encoding) use kar rahe hain.
#
# Iska fayda:
# 1. <UNK> token ki zarurat nahi padti
# 2. Hindi / Urdu / English mixed text bhi tokenize ho sakta hai
# 3. Rare words ko chhote useful pieces me tod sakte hain
#
# Byte-level ka matlab:
# text ko UTF-8 bytes me todte hain
# isliye almost koi bhi Unicode text represent ho sakta hai.
#
# Practical note:
# abhi data kam hai, isliye current tokenizer setup ko hi rakhna sensible hai.
# Chhote dataset par tokenizer ko bahut aggressively complex banane se fayda
# hamesha nahi milta. Is file me jo BPE flow hai, wo future growth ke liye ready hai.
#
# BPE ko kab use karna chahiye:
# 1. jab text multilingual ho
# 2. jab rare words bahut aate hon
# 3. jab word-level tokenizer me <UNK> problem aa rahi ho
# 4. jab future me data size badhne wala ho
#
# BPE ko practically kaise use kar sakte ho:
# 1. raw text do -> tokenizer.build_vocab(text)
# 2. trained tokenizer save karo -> tokenizer.save(...)
# 3. text ko ids me badlo -> tokenizer.encode(...)
# 4. ids ko wapas text me badlo -> tokenizer.decode(...)
# 5. training aur generation dono me same saved tokenizer load karo


class Tokenizer:
    def __init__(self, target_vocab_size=512):
        # BPE me base vocabulary 256 byte values se start hoti hai.
        # Iske upar hum merges add karke larger tokens banate hain.
        self.target_vocab_size = target_vocab_size
        self.pad_token = "<PAD>"
        self.pad_token_id = 0

        self.token_to_id = {self.pad_token: self.pad_token_id}
        self.id_to_token = {self.pad_token_id: self.pad_token}

        # 256 raw bytes ko vocabulary me add kar rahe hain.
        for byte_value in range(256):
            token_id = byte_value + 1
            token_bytes = bytes([byte_value])
            self.token_to_id[token_bytes] = token_id
            self.id_to_token[token_id] = token_bytes

        # merges list me BPE training se nikle merge rules aate hain.
        # Har item hoga: (left_token_bytes, right_token_bytes, merged_token_bytes)
        self.merges = []
        self.vocab_size = len(self.id_to_token)

    def _split_text_into_pieces(self, text):
        # BPE training ke liye text ko whitespace-preserving chunks me todna useful hota hai.
        # Regex spaces ko bhi preserve karta hai, taaki decode karte waqt original text shape bani rahe.
        return re.findall(r"\S+|\s+", text)

    def _count_pairs(self, sequences):
        # Har adjacent token pair kitni baar aaya, ye count karte hain.
        # BPE ka next merge isi frequency info par depend karta hai.
        pair_counts = {}
        for sequence in sequences:
            for index in range(len(sequence) - 1):
                pair = (sequence[index], sequence[index + 1])
                pair_counts[pair] = pair_counts.get(pair, 0) + 1
        return pair_counts

    def _merge_pair_in_sequence(self, sequence, pair, merged_token_id):
        # Ye function ek single sequence me chosen pair ko naya merged token bana deta hai.
        # Example:
        # [10, 11, 10, 11] aur pair (10,11) ho to result [merged, merged] ban sakta hai.
        merged_sequence = []
        index = 0

        while index < len(sequence):
            if (
                index < len(sequence) - 1
                and sequence[index] == pair[0]
                and sequence[index + 1] == pair[1]
            ):
                merged_sequence.append(merged_token_id)
                index += 2
            else:
                merged_sequence.append(sequence[index])
                index += 1

        return merged_sequence

    def _merge_pair_in_all_sequences(self, sequences, pair, merged_token_id):
        # Jo pair best nikla hai, use corpus ki sab sequences me apply karte hain.
        # Isi step se vocabulary dheere-dheere smarter banti jati hai.
        return [
            self._merge_pair_in_sequence(sequence, pair, merged_token_id)
            for sequence in sequences
        ]

    def build_vocab(self, text):
        # Ye tokenizer training step hai.
        # Yahin BPE decide karta hai kaunse byte-pairs ko merge karke naye tokens banana hain.
        #
        # Kam data ke case me:
        # - vocabulary ko unnecessary huge nahi banana chahiye
        # - useful repeated pairs par focus rakhna better hota hai
        # Byte-level BPE me lowercase force nahi karte.
        # Unicode scripts jaise Hindi/Urdu me exact text preserve karna zaruri hota hai.
        pieces = self._split_text_into_pieces(text)
        sequences = [
            [byte_value + 1 for byte_value in piece.encode("utf-8")] for piece in pieces
        ]

        # Target vocab size tak most frequent byte-pairs merge karte rahenge.
        while len(self.id_to_token) < self.target_vocab_size:
            pair_counts = self._count_pairs(sequences)
            if not pair_counts:
                break

            # Sabse frequent pair choose karte hain.
            # BPE ka assumption ye hai ki repeated patterns ko ek token banana useful hota hai.
            best_pair, best_count = max(pair_counts.items(), key=lambda item: item[1])

            # Agar pair bahut hi rare ho gaya to merge continue karne ka fayda kam hota hai.
            if best_count < 2:
                break

            left_id, right_id = best_pair
            left_bytes = self.id_to_token[left_id]
            right_bytes = self.id_to_token[right_id]
            merged_bytes = left_bytes + right_bytes

            if merged_bytes in self.token_to_id:
                break

            merged_token_id = len(self.id_to_token)
            self.token_to_id[merged_bytes] = merged_token_id
            self.id_to_token[merged_token_id] = merged_bytes
            self.merges.append((left_bytes, right_bytes, merged_bytes))

            # Ab chosen pair ko sab sequences me replace kar dete hain,
            # taaki next iteration nayi tokenization state se continue ho.
            sequences = self._merge_pair_in_all_sequences(
                sequences, best_pair, merged_token_id
            )

        self.vocab_size = len(self.id_to_token)
        print(f"BPE tokenizer ready! Total tokens: {self.vocab_size}")

    def encode(self, text):
        # Encode me text ko bytes me todkar merge rules apply karte hain.
        # Isliye koi unknown token nahi hota, kyunki har text bytes me toot sakta hai.
        #
        # Training ke baad actual real-world use isi function ka hota hai.
        # Model ko direct text nahi, isi function ke output token ids diye jate hain.
        pieces = self._split_text_into_pieces(text)
        encoded_ids = []

        for piece in pieces:
            sequence = [byte_value + 1 for byte_value in piece.encode("utf-8")]

            # Build_vocab ke time jo merges sikhe the, unhe same order me apply karna zaruri hai.
            # Tabhi inference ke time tokenization training ke saath match karegi.
            for left_bytes, right_bytes, merged_bytes in self.merges:
                left_id = self.token_to_id[left_bytes]
                right_id = self.token_to_id[right_bytes]
                merged_id = self.token_to_id[merged_bytes]
                sequence = self._merge_pair_in_sequence(
                    sequence, (left_id, right_id), merged_id
                )

            encoded_ids.extend(sequence)

        return encoded_ids

    def decode(self, ids):
        # Decode me token bytes ko join karke wapas utf-8 text banate hain.
        # errors="replace" safety ke liye hai, lekin ideally bytes valid honge.
        #
        # Decode mostly generation ke baad use hota hai:
        # model token ids deta hai -> hum decode karke readable text nikalte hain.
        output_bytes = bytearray()

        for token_id in ids:
            if token_id == self.pad_token_id:
                continue

            token_value = self.id_to_token.get(token_id, b"")
            if isinstance(token_value, bytes):
                output_bytes.extend(token_value)

        return output_bytes.decode("utf-8", errors="replace")

    def save(self, path):
        # bytes ko JSON me directly save nahi kar sakte,
        # isliye unhe hex string me store kar rahe hain.
        #
        # Save isliye important hai kyunki:
        # training aur inference dono me exact same tokenizer use hona chahiye.
        data = {
            "target_vocab_size": self.target_vocab_size,
            "pad_token": self.pad_token,
            "pad_token_id": self.pad_token_id,
            "vocab_size": self.vocab_size,
            "tokens": {
                str(token_id): (
                    token_value if isinstance(token_value, str) else token_value.hex()
                )
                for token_id, token_value in self.id_to_token.items()
            },
            "merges": [
                [left.hex(), right.hex(), merged.hex()]
                for left, right, merged in self.merges
            ],
        }

        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
        print(f"Tokenizer saved: {path}")

    def load(self, path):
        # Load ka matlab trained tokenizer ko wapas memory me lana.
        # Ye step generation, fine-tuning aur evaluation sab jagah required hota hai.
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.target_vocab_size = data["target_vocab_size"]
        self.pad_token = data["pad_token"]
        self.pad_token_id = data["pad_token_id"]
        self.vocab_size = data["vocab_size"]

        self.id_to_token = {}
        self.token_to_id = {}

        for token_id_str, token_value in data["tokens"].items():
            token_id = int(token_id_str)
            if token_id == self.pad_token_id:
                self.id_to_token[token_id] = token_value
                self.token_to_id[token_value] = token_id
            else:
                token_bytes = bytes.fromhex(token_value)
                self.id_to_token[token_id] = token_bytes
                self.token_to_id[token_bytes] = token_id

        self.merges = [
            (bytes.fromhex(left), bytes.fromhex(right), bytes.fromhex(merged))
            for left, right, merged in data["merges"]
        ]
        print(f"BPE tokenizer loaded! Tokens: {self.vocab_size}")


if __name__ == "__main__":
    # Ye demo block sirf samjhane ke liye hai.
    # Real project flow me train.py tokenizer ko build/save karta hai,
    # aur बाकी scripts saved tokenizer ko load karti hain.
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        text = file.read()

    tokenizer = Tokenizer(target_vocab_size=TOKENIZER_CONFIG["target_vocab_size"])
    tokenizer.build_vocab(text)

    sample = "SusaLabs AI aur اردو हिंदी mix text"
    encoded = tokenizer.encode(sample)
    decoded = tokenizer.decode(encoded)

    print(f"\nOriginal : {sample}")
    print(f"Encoded  : {encoded[:30]}")
    print(f"Decoded  : {decoded}")

    tokenizer.save(str(TOKENIZER_PATH))
