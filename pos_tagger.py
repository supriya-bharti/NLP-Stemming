from tokenizer import tokenize
import string

# Common nouns
nouns = {
    "student", "students", "teacher", "teachers",
    "book", "books", "computer", "computers",
    "language", "languages", "word", "words",
    "project", "projects", "algorithm", "algorithms",
    "name", "city", "car", "roof","school", "house", "table", "story", "child", "dog", "cat",
    "topic", "application", "researcher","nlp", "ai", "ml", "data", "model", "system", "program", "code","bank", "river", "mountain", "ocean", "forest", "desert", "island", "continent", "planet", "universe"
}
interjections = {
    "hi", "hello", "hey", "wow", "oops",
    "ouch", "hurrah", " bravo", "alas", "hurray", "yikes", "oopsie", "whoa", "yippee"
}

proper_nouns = {
    "supriya", "bharti", "john", "mary", "london", "paris",
    "new york", "mumbai", "delhi", "tokyo", "sydney", "berlin", "moscow", "beijing", "cairo", "rio de janeiro", "cape town", "sao paulo", "toronto", "vancouver"
}
# Common verbs
verbs = {
    "is", "am", "are", "was", "were",
    "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "go", "goes", "went",
    "run", "runs", "eat", "eats", "study", "studies",
    "learn", "learns", "write", "writes",
    "play", "plays", "work", "works","fell", "went", "saw", "ran", "broke",
    "wrote", "spoke", "took", "gave", "came",
    "ate", "slept", "swam", "drove"
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
    "topics", "applications", "researchers",
    "children"
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

    original_word = word
    word = word.lower()

    # Interjections
    if word in interjections:
        return "interjection"

    # Known proper nouns
    if word in proper_nouns:
        return "proper_noun"

    # Words that belong to other categories
    if word in other_words:
        return "other"

    # Irregular verbs
    irregular_verbs = {
        "fell", "went", "saw", "ran", "broke",
        "wrote", "spoke", "took", "gave", "came",
        "ate", "slept", "swam", "drove"
    }

    if word in irregular_verbs:
        return "v"

    # Adverbs
    if word in adverbs or word in {"down", "up", "away"}:
        return "r"

    if word.endswith("ly"):
        return "r"

    # Known verbs
    if word in verbs:
        return "v"

    # Known adjectives
    if word in adjectives:
        return "a"

    # Known nouns
    if word in plural_nouns or word in nouns:
        return "n"

    # Adjective suffixes
    if word.endswith(("ous", "ful", "less", "able", "ible",
                      "ive", "al", "ic")):

        if word.endswith("ic") and word in {
            "topic", "music", "traffic", "logic"
        }:
            return "n"

        return "a"

    # Verb suffixes
    if word.endswith(("ing", "ed", "ize", "ise")):
        return "v"

    # Noun suffixes
    if word.endswith(("tion", "ment", "ness", "ity", "er", "or", "ism")):
        return "n"

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
                if pos not in ("r", "a", "n", "other"):
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

    # Do not convert the complete sentence to lowercase
    words = tokenize(sentence)

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