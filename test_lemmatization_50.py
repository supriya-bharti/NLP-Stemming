
from lemmatization_evaluation import evaluate_lemmatizer

test_words = [

    # Nouns (18)
    ("dogs", "n"),
    ("cars", "n"),
    ("books", "n"),
    ("houses", "n"),
    ("buses", "n"),
    ("dishes", "n"),
    ("babies", "n"),
    ("cities", "n"),
    ("stories", "n"),
    ("parties", "n"),
    ("churches", "n"),
    ("watches", "n"),
    ("foxes", "n"),
    ("tomatoes", "n"),
    ("potatoes", "n"),
    ("wolves", "n"),
    ("leaves", "n"),
    ("knives", "n"),
    ("houses", "n"),
    ("tomatoes", "n"),
    ("potatoes", "n"),
    ("buses", "n"),
    ("dogs", "n"),
    ("cars", "n"),
    ("books", "n"),


    # Verbs (20)
    ("walks", "v"),
    ("talked", "v"),
    ("played", "v"),
    ("watches", "v"),
    ("studies", "v"),
    ("tries", "v"),
    ("carries", "v"),
    ("cries", "v"),
    ("fixed", "v"),
    ("stopped", "v"),
    ("planned", "v"),
    ("smiled", "v"),
    ("danced", "v"),
    ("written", "v"),
    ("saw", "v"),
    ("took", "v"),
    ("gave", "v"),
    ("drove", "v"),
    ("slept", "v"),
    ("swam", "v"),

    # Adjectives (12)
    ("bigger", "a"),
    ("smaller", "a"),
    ("faster", "a"),
    ("slower", "a"),
    ("happier", "a"),
    ("easier", "a"),
    ("busier", "a"),
    ("heavier", "a"),
    ("prettier", "a"),
    ("strongest", "a"),
    ("biggest", "a"),
    ("best", "a")
]

results, accuracy = evaluate_lemmatizer(test_words)

print("\nMISMATCHED WORDS")
print("-" * 65)

for word, pos, our_result, nltk_result, status in results:
    if status == "Mismatch":
        print(f"{word:15} {pos:5} {our_result:15} {nltk_result}")

print("-" * 65)
print(f"Total test cases: {len(test_words)}")
print(f"Agreement with NLTK: {accuracy:.2f}%")
