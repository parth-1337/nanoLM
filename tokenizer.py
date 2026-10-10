import json
import struct
# trained merges saved in json for now can cahnge it to pickle which will support tuples

# for rerun just remove the train method and just do gpt.load(merges.json)
# and then test using encode

class Tokenizer:
    def __init__(self):
        with open("input.txt", "r", encoding="utf-8") as file:
                self.train_text = file.read()
                #print(self.train_text[2])
        self.merge_map = {}
        self.merge_limit = 500
        self.next_id = 256

    def save(self, path="merges.json"):
        data = {
            "merge_map": {f"{k[0]},{k[1]}": v for k, v in self.merge_map.items()},
            "next_id": self.next_id
        }
        with open(path, "w") as f:
            json.dump(data, f)

    def load(self, path="tokenizer.json"):
        with open(path, "r") as f:
            data = json.load(f)
        self.merge_map = {tuple(map(int, k.split(","))): v for k, v in data["merge_map"].items()}
        self.next_id = data["next_id"]
        self.build_vocab()

    def build_vocab(self):
        vocab = {idx: bytes([idx]) for idx in range(256)}
        for pair, new_id in self.merge_map.items():
            vocab[new_id] = vocab[pair[0]] + vocab[pair[1]]
        self.vocab = vocab

    def decode(self, ids):
        bytes_out = b"".join(self.vocab[idx] for idx in ids)
        return bytes_out.decode("utf-8", errors="replace")

    def pair_counts(self,ids):
        pair_counts = {}
        for i in range(len(ids) - 1):
            pair = (ids[i], ids[i+1])
            pair_counts[pair] = pair_counts.get(pair, 0) + 1
            #print(pair_counts)

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

gpt = Tokenizer()
#gpt.train()
#gpt.save("merges.json")
gpt.load("merges.json")
test = "an what "
x = gpt.encode(test)
print(list(test.encode("utf-8")))
#print(gpt.vocab)
#print(gpt.merge_map)
print(x)
print(gpt.decode([266, 456]))

print(len(gpt.merge_map))
print(len(gpt.vocab))

# vocab -> bytes
# pack header vocab len + merge_map len
#
with open("tok.bin", "wb") as f:
    f.write(struct.pack('<ii', len(gpt.vocab), len(gpt.merge_map)))
    for i in range(len(gpt.vocab)):
        f.write(struct.pack('<i', len(gpt.vocab[i])))
        f.write(gpt.vocab[i])
    for (a, b) in gpt.merge_map.keys():
        f.write(struct.pack('<ii', a, b))
