from evaluation import evaluate

test_words = [
    "caresses",
    "ponies",
    "ties",
    "cats",
    "boys",
    "happy",
    "relational",
    "conditional",
    "rational",
    "digitizer",
    "triplicate",
    "formative",
    "formalize",
    "electriciti",
    "hopeful",
    "goodness",
    "running",
    "jumped",
    "studying",
    "are",
    "make",
    "hope",
    "trouble",
    "private",
    "agreed",
    "disabled",
    "possibly",
    "generous",
    "adjustment",
    "replacement"
]

results, accuracy = evaluate(*test_words)

print("\nSTEMMING EVALUATION")
print("-" * 60)

for word, my_stem, nltk_stem, status in results:
    print(f"{word:15} {my_stem:15} {nltk_stem:15} {status}")

print("-" * 60)
print(f"Total words: {len(test_words)}")
print(f"Accuracy: {accuracy:.2f}%")