import nltk
from nltk.corpus import words, wordnet as wn
from core.qdrant_client import insert_word
from core.embeddings import get_vector
from tqdm import tqdm

nltk.download('words')
nltk.download('wordnet')
nltk.download('omw-1.4')

word_list = words.words()

print(f"Total words to insert: {len(word_list)}")

for w in tqdm(word_list, desc="Indexing words into Qdrant"):
    synsets = wn.synsets(w)

    # Collect simple metadata from WordNet if available
    if synsets:
        meaning = synsets[0].definition()
        synonyms = [lemma.name() for lemma in synsets[0].lemmas()]
        antonyms = [
            ant.name() for lemma in synsets[0].lemmas() for ant in lemma.antonyms()
        ]
        examples = synsets[0].examples()
    else:
        meaning, synonyms, antonyms, examples = "", [], [], []

    vector = get_vector(w)

    payload = {
        "word": w,
        "meaning": meaning,
        "synonyms": synonyms,
        "antonyms": antonyms,
        "examples": examples
    }

    insert_word(vector, payload)

print("All words have been inserted into Qdrant!")
