
import csv
from preprocessing import preprocess_with_mapping

print("=" * 65)
print("       NLP TEXT NORMALIZATION")
print("=" * 65)

text = input("\nEnter a sentence: ")

results = preprocess_with_mapping(text)

print("\nOriginal Word       Stem          Lemma")
print("-" * 50)

for original, stemmed, lemma in results:
    print(f"{original:20} {stemmed:13} {lemma}")

with open("normalization_results.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Original Word",
        "Stem",
        "Lemma"
    ])

    writer.writerows(results)

print("\nResults saved to normalization_results.csv")
