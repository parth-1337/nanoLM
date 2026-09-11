class Tokenizer:
    def __init__(self):
        with open("input.txt", "r", encoding="utf-8") as file:
                self.train_text = file.read()
        self.merge_map = {}
        self.merge_limit = 500
        self.next_id = 256
        #self.ids = list(text.encode('utf-8'))

    def build_vocab(self):
        vocab = {idx: bytes([idx]) for idx in range(256)}   # base case: single bytes
        for pair, new_id in self.merge_map.items():
            vocab[new_id] = vocab[pair[0]] + vocab[pair[1]]  # concatenate bytes of the merged pair
        self.vocab = vocab
    
    def decode(self, ids):
        bytes_out = b"".join(self.vocab[idx] for idx in ids)
        return bytes_out.decode("utf-8", errors="replace")
    
    def pair_counts(self,ids):
        pair_counts = {}
        for i in range(len(ids) - 1):
            pair = (ids[i], ids[i+1])
            pair_counts[pair] = pair_counts.get(pair, 0) + 1
        return pair_counts

    def merge_pair(self, ids, pair, new_id):
        new_ids = []
        i = 0
        while i < len(ids):
            if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
                new_ids.append(new_id)
                i += 2
            else:
                new_ids.append(ids[i])
                i += 1
        return new_ids

    def train(self):
        ids = list(self.train_text.encode('utf-8'))
        for i in range(self.merge_limit):
            counts = self.pair_counts(ids)
            if not counts:
                break
            max_pair = max(counts, key = counts.get)
            ids = self.merge_pair(ids, max_pair, self.next_id)
            self.merge_map[max_pair] = self.next_id
            self.next_id += 1
        self.build_vocab()

    def encode(self, text):
        ids = list(text.encode("utf-8"))
        while len(ids) >= 2:
            counts = self.pair_counts(ids)
            pair_to_merge = min(counts, key=lambda p: self.merge_map.get(p, float("inf")))
            if pair_to_merge not in self.merge_map:
                break
            ids = self.merge_pair(ids, pair_to_merge, self.merge_map[pair_to_merge])
        return ids

obj = Tokenizer()
obj.train()
x = obj.encode("thou")
print(x)

