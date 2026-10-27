from stemmer import porter_stem
from nltk.stem import PorterStemmer


nltk_stemmer = PorterStemmer()


def evaluate(*words):

    total = 0
    matches = 0

    results = []

    for word in words:

        my_stem = porter_stem(word)
        nltk_stem = nltk_stemmer.stem(word)

        if my_stem == nltk_stem:
            matches += 1
            status = "Match"
        else:
            status = "Mismatch"

        total += 1

        results.append(
            (word, my_stem, nltk_stem, status)
        )

    accuracy = (matches / total) * 100 if total > 0 else 0

    return results, accuracy