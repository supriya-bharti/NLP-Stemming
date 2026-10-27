
from lemmatizer import lemmatize
from nltk.stem import WordNetLemmatizer

nltk_lemmatizer = WordNetLemmatizer()

def evaluate_lemmatizer(test_words):
    results = []
    correct = 0

    for word, pos in test_words:
        our_result = lemmatize(word)

        nltk_result = nltk_lemmatizer.lemmatize(word, pos=pos)

        status = "Match" if our_result == nltk_result else "Mismatch"

        if status == "Match":
            correct += 1

        results.append((word, pos, our_result, nltk_result, status))

    accuracy = (correct / len(test_words)) * 100 if test_words else 0

    return results, accuracy


if __name__ == "__main__":
    
    test_words = [
    # Nouns
    ("cats", "n"),
    ("children", "n"),
    ("mice", "n"),
    ("feet", "n"),
    ("applications", "n"),
    ("researchers", "n"),
    ("classes", "n"),
    ("boxes", "n"),
    ("studies", "n"),
    ("types", "n"),

    # Verbs
    ("running", "v"),
    ("studying", "v"),
    ("went", "v"),
    ("gone", "v"),
    ("making", "v"),
    ("taking", "v"),
    ("writing", "v"),
    ("coming", "v"),
    ("using", "v"),
    ("stopped", "v"),
    ("bought", "v"),
    ("eaten", "v"),
    ("analyzing", "v"),
    ("processing", "v"),
    ("becoming", "v"),

    # Adjectives
    ("better", "a"),
    ("worse", "a"),
    ("happier", "a"),
    ("simpler", "a"),
    ("fascinating", "v"),
]


    results, accuracy = evaluate_lemmatizer(test_words)

    print("\nLemmatization Evaluation")
    print("-" * 75)
    print(f"{'Word':<15}{'POS':<8}{'Our Lemma':<18}{'NLTK Lemma':<18}{'Status'}")
    print("-" * 75)

    for word, pos, our_result, nltk_result, status in results:
        print(
            f"{word:<15}{pos:<8}{our_result:<18}"
            f"{nltk_result:<18}{status}"
        )

    print("-" * 75)
    print(f"Agreement with NLTK: {accuracy:.2f}%")
