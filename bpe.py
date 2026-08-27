
# a simple byte pair encoding tokenizer merges can be adjusted using merge_limit variable 
# final vocab size will be merge_limit + 256
# tokens are utf-8 encoded


def pair_counts(ids):
    pair_counts = {}
    for i in range(len(ids) - 1):
        pair = (ids[i], ids[i+1])
        pair_counts[pair] = pair_counts.get(pair, 0) + 1
    return pair_counts


def merge_pair(ids, pair, new_id):
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


def encode(text, merges):
    ids = list(text.encode("utf-8"))

    while len(ids) >= 2:
        counts = pair_counts(ids)
        pair_to_merge = min(counts, key=lambda p: merges.get(p, float("inf")))

        if pair_to_merge not in merges:
            break

        ids = merge_pair(ids, pair_to_merge, merges[pair_to_merge])

    return ids


with open("training_data.txt", "r", encoding="utf-8") as file:
    text = file.read()


ids = list(text.encode('utf-8'))

merge_map = {}
merge_limit = 50
next_id = 256

for i in range(merge_limit):
    counts = pair_counts(ids)
    if not counts:
        break
    max_pair = max(counts, key = counts.get)
    ids = merge_pair(ids, max_pair, next_id)
    merge_map[max_pair] = next_id
    next_id += 1


print(encode(text, merge_map))
#print(merge_map)
