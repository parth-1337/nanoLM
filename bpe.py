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
# test text 1000 words
text = """The quick brown fox jumps over the lazy dog. This classic pangram contains every letter of the English alphabet, making it a perfect starting point for testing fonts, keyboards, and of course, tokenizers. When building a natural language processing system, the first step is often to convert raw text into a sequence of integers. This process is called tokenization. To train a good tokenizer, whether it uses Byte-Pair Encoding (BPE), WordPiece, or Unigram models, you need a diverse dataset. You want words of varying lengths, common suffixes like -ing, -ed, and -tion, as well as a good mix of punctuation marks, numbers, and perhaps even some special characters or symbols. In the early days of computing, text was simply ASCII. Each character was exactly one byte. The letter 'A' was 65, 'B' was 66, and so on. But as software became global, we needed to support thousands of characters from hundreds of languages, leading to the creation of Unicode and UTF-8. UTF-8 is a variable-width character encoding capable of encoding all 1,112,064 valid character code points in Unicode using one to four one-byte code units. It is backward compatible with ASCII, which is why it has become the dominant encoding for the World Wide Web. As of 2026, UTF-8 is used by over 98% of all websites.

But character-level tokenization is often inefficient for machine learning models. If a model has to predict text character by character, the sequence lengths become extremely long. A single sentence of 100 words might be 500 characters, meaning the model has to process 500 steps. On the other hand, word-level tokenization has its own problems. The vocabulary size becomes massive. There are hundreds of thousands of words in the English language alone, and when you account for typos, slang, and different word forms (like run, running, ran), the dictionary explodes in size. If a model encounters a word it has never seen before, it is forced to use an <UNK> (unknown) token, losing all the semantic meaning of that word.

This is where subword tokenization bridges the gap. Algorithms like BPE start with a vocabulary of individual characters and iteratively merge the most frequently occurring pairs of tokens. For example, if 'e' and 'r' frequently appear together, they are merged into 'er'. Then, if 'er' and 's' frequently appear together, they become 'ers'. Over many iterations, the vocabulary grows to contain common whole words, like 'the', 'and', or 'computer', while rare words remain split into smaller subword units. If the tokenizer encounters the word 'unbelievably', it might split it into 'un', 'believ', and 'ably'. This ensures that the model can handle any text, even misspelled words or made-up terms, without ever resorting to an unknown token.

Let's add some numbers and diverse symbols to ensure your vocabulary is robust! We can include integers like 10, 42, 100, 2024, 2025, and 2026. Let's add some decimals like 3.14159, 2.718, or 0.99. What about punctuation? We need commas, periods, exclamation points! We should ask questions too? Hyphens-are-useful, and so are (parentheses), [brackets], and {braces}. Some code-like syntax might appear: functionName(var1, var2) { return var1 + var2; }. We should also include capitalization. UPPERCASE words, lowercase words, and Title Case Words all look different to a basic tokenizer unless it converts everything to lowercase first. Case-sensitive tokenizers are standard for modern large language models because the capitalization of a word often carries important context. For instance, 'apple' might refer to the fruit, while 'Apple' usually refers to the technology company.

The beauty of language is its endless variety. In the forest of syntax, verbs act as the engines of sentences, driving the action forward, while adjectives and adverbs paint the scenes with color and precision. Nouns stand as the solid pillars, the objects and concepts we discuss. Prepositions establish relationships in time and space, telling us if something is under the bridge, above the clouds, or happening before the dawn. Conjunctions link these pieces together, allowing for complex, compound thoughts that elevate human communication above mere grunts and gestures. As you train your tokenizer on this text, watch how it breaks down the morphology of words. It will learn the roots, prefixes, and suffixes. It will map the statistical structure of English, finding the hidden mathematical patterns in our everyday speech. The resulting vocabulary will be a compressed representation of the language itself, optimized for a neural network to consume, process, and eventually, understand.

As we look to the future, the complexity of models will only increase. We are moving beyond text to multimodal systems that tokenize images, audio, and video alongside text. An image can be broken down into patches, much like a sentence is broken down into subwords. An audio waveform can be sliced into frames and quantized into discrete audio tokens. By treating everything as a sequence of tokens, artificial intelligence can learn the underlying relationships between different modalities, mapping the word 'dog' to the visual representation of a dog and the audio waveform of a bark. But everything starts here, with simple text, a sequence of bytes, and an algorithm trying to find the most efficient way to compress the beautiful complexity of human language into a finite vocabulary of integers.

Consider the vast oceans and the stars in the night sky. When astronomers gaze through telescopes, they collect petabytes of data. This data, too, must be processed, filtered, and analyzed. Much like how a tokenizer sifts through letters to find meaningful words, algorithms sift through background radiation to find the faint signals of distant galaxies, pulsars, and black holes. The universe is a grand puzzle, and our attempts to understand it require breaking it down into manageable, fundamental pieces. In physics, these pieces are quarks and leptons. In chemistry, they are atoms and molecules. In biology, they are cells and DNA sequences. And in natural language processing, they are tokens.

To build a robust system, you must test edge cases. What happens when the user inputs repeated characters like 'looooong' or 'hahahaha'? What about strings of numbers: 9876543210? Does the tokenizer split them by digit, or try to keep them as a single block? What if there are multiple spaces    between   words? Handling whitespace correctly is crucial. Some tokenizers use a special symbol, like a meta-character (e.g., ' ') to represent a space, ensuring that the original text can be perfectly reconstructed from the tokens. This is known as lossless tokenization. If your tokenizer strips out extra spaces or drops punctuation, it becomes lossy, meaning the decoded output will not exactly match the original input. For tasks like code generation or precise formatting, lossless tokenization is an absolute requirement.

As you copy and paste this text into your Python script, Jupyter notebook, or Rust application, imagine the tiny mathematical operations happening under the hood. Thousands of loops, hash map lookups, and frequency counts are being executed in milliseconds. You are teaching a machine the very first step of reading. It doesn't know what the words mean yet, but it is learning their shapes. It is learning that 'token' and 'ization' often go together, that 'train' can be followed by 'ing', and that punctuation usually attaches to the end of a word rather than the beginning. This fundamental step sets the stage for the attention mechanisms and transformer blocks that will follow. So here is your data, a thousand words of structured thought, ready to be digested, compressed, and transformed by your code."""

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

print(merge_map)

