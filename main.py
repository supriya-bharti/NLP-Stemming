import csv
from stemmer import porter_stem 
from nltk.stem import PorterStemmer
from preprocessing import preprocess
from preprocessing import preprocess_with_mapping
from preprocessing import show_pipeline
from evaluation import evaluate
from stemmer import porter_stem, step1b, step4
from stemmer import step4_suffixes

nltk_stemmer = PorterStemmer()

# import string

with open("dataset/sample.txt", "r") as file:
    text = file.read()

results = preprocess_with_mapping(text)

print(f"{'Original':20} {'Stemmed':20}")
print("-" * 40)

for original, stemmed in results:
    print(f"{original:20} {stemmed:20}")

test_words = [
    "students",
    "learning",
    "natural",
    "language",
    "processing",
    "fascinating",
    "field",
    "artificial",
    "intelligence",
    "researchers",
    "developing",
    "algorithms",
    "understanding",
    "studying",
    "machine",
    "computational",
    "linguistics",
    "system",
    "processes",
    "different",
    "types",
    "textual",
    "information",
    "preprocessing",
    "important",
    "algorithms",
    "designed",
    "identify",
    "meaningful",
    "patterns"
]

results, accuracy = evaluate(test_words)

with open("results/stemming_results.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Word",
        "Our Stemmer",
        "NLTK Stemmer",
        "Result"
    ])

    for word, my_stem, nltk_stem, status in results:

        writer.writerow([
            word,
            my_stem,
            nltk_stem,
            status
        ])



print(f"{'Word':20} {'Our Stemmer':20} {'NLTK':20} {'Result'}")
print("-" * 75)

for word, my_stem, nltk_stem, status in results:
    print(
        f"{word:20} "
        f"{my_stem:20} "
        f"{nltk_stem:20} "
        f"{status}"
    )

print("\nAccuracy:", accuracy, "%")



print("\n" + "=" * 60)
print("INTERACTIVE STEMMING")
print("=" * 60)

text = input("\nEnter a sentence: ")

result = preprocess_with_mapping(text)

print("\nOriginal → Stemmed")
print("-" * 40)

for original, stemmed in result:
    print(f"{original:20} → {stemmed}")


show_pipeline(text)





