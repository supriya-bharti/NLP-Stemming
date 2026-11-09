from tokenizer import tokenize
import string

# Common nouns
nouns = {
    "student", "students", "teacher", "teachers",
    "book", "books", "computer", "computers",
    "language", "languages", "word", "words",
    "project", "projects", "algorithm", "algorithms",
    "name", "city", "car", "house", "table"
}

# Common verbs
verbs = {
    "is", "am", "are", "was", "were",
    "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "go", "goes", "went",
    "run", "runs", "eat", "eats", "study", "studies",
    "learn", "learns", "write", "writes",
    "play", "plays", "work", "works"
}

# Common adjectives
adjectives = {
    "good", "bad", "beautiful", "happy",
    "sad", "big", "small", "fast", "slow",
    "intelligent", "difficult", "easy",
    "interesting", "important", "new", "old"
}

# Common adverbs
adverbs = {
    "quickly", "slowly", "happily", "sadly",
    "carefully", "easily", "very", "always",
    "never", "often", "sometimes", "here", "there"
}

other_words = {
    # Articles and determiners
    "a", "an", "the", "this", "that",
    "these", "those", "some", "any",

    # Pronouns
    "i", "you", "he", "she", "it",
    "we", "they", "me", "him", "her",
    "us", "them", "my", "your", "his",
    "our", "their",

    # Prepositions
    "in", "on", "at", "by", "for",
    "from", "to", "with", "of", "about",

    # Conjunctions
    "and", "but", "or", "because", "although"
}

plural_nouns = {
    "students", "teachers", "books", "computers",
    "languages", "words", "projects", "algorithms",
    "cars", "dogs", "tables", "chairs",
    "topics", "applications", "researchers"
}

ing_nouns = {
    "programming",
    "processing",
    "learning",
    "reading",
    "writing",
    "painting",
    "shopping"
}

def detect_pos(word):

    word = word.lower()
    
    if word in other_words:
        return "other"

    if word in plural_nouns:
        return "n"

    if word in nouns:
        return "n"

    if word in verbs:
        return "v"

    if word in adjectives:
        return "a"

    if word in adverbs:
        return "r"

    # Adverb detection
    if word.endswith("ly"):
        return "r"

    if word.endswith(("ous", "ful", "less", "able", "ible", "ive", "al", "ic")):
        if word.endswith("ic") and word in {"topic", "music", "traffic", "logic"}:
            return "n"
        return "a"

    # Verb detection
    if word.endswith(("ing", "ed", "ize", "ise")):
        return "v"

    # Noun detection
    if word.endswith(("tion", "ment", "ness", "ity", "er", "or", "ism")):
        return "n"

    # Default
    return "n"

def detect_pos_with_context(words):

    results = []

    for i, word in enumerate(words):

        pos = detect_pos(word)
        
        # An -ing noun can follow another -ing verb
        if i > 0 and words[i - 1].lower().endswith("ing"):
            if word.lower() in ing_nouns:
                pos = "n"
        
        # A word after a noun or pronoun may be a verb
        if i > 0 and results:
            previous_pos = results[-1][1]

            if previous_pos == "n" and word.lower().endswith(("s", "ed", "ing")):

                if word.lower() not in plural_nouns and word.lower() not in ing_nouns:
                    pos = "v"
                
            # A word after a pronoun is often a verb
            if previous_pos == "other" and results[-1][0].lower() in [
                "i", "you", "he", "she", "it", "we", "they"
            ]:
                if pos != "other":
                    pos = "v"

        # Articles are not nouns
        if word.lower() in ["a", "an", "the"]:
            pos = "other"

        # Word after an article
        elif i > 0 and words[i - 1].lower() in ["a", "an", "the"]:

            # Keep adjective if the word is an adjective
            if pos == "a":
                pos = "a"
            else:
                pos = "n"

        results.append((word, pos))

    return results

def tag_sentence(sentence):

    words = tokenize(sentence.lower())

    words = [
        word.strip(string.punctuation)
        for word in words
        if word.strip(string.punctuation)
    ]

    results = detect_pos_with_context(words)

    return results

from lemmatizer import lemmatize


def auto_lemmatize(sentence):

    tagged_words = tag_sentence(sentence)

    results = []

    for word, pos in tagged_words:

        if pos == "other":
            lemma = word
        else:
            lemma = lemmatize(word, pos)

        results.append({
            "word": word,
            "pos": pos,
            "lemma": lemma
        })

    return results


sentence = "The children are playing happily with beautiful dogs."

results = auto_lemmatize(sentence)

for item in results:
    print(item)