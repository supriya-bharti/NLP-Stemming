
import csv
from pathlib import Path

from preprocessing import preprocess_with_mapping, show_pipeline
from evaluation import evaluate
from lemmatization_evaluation import evaluate_lemmatizer


# ---------------- CONFIGURATION ----------------

STEM_TEST_WORDS = [
    "students", "learning", "natural", "language",
    "processing", "fascinating", "field", "artificial",
    "intelligence", "researchers", "developing", "algorithms",
    "understanding", "studying", "machine", "computational",
    "linguistics", "system", "processes", "different",
    "types", "textual", "information", "preprocessing",
    "important", "designed", "identify", "meaningful", "patterns"
]

LEMMA_TEST_WORDS = [
    ("cats", "n"), ("children", "n"), ("mice", "n"),
    ("feet", "n"), ("applications", "n"), ("researchers", "n"),
    ("classes", "n"), ("boxes", "n"), ("studies", "n"),
    ("types", "n"), ("running", "v"), ("studying", "v"),
    ("went", "v"), ("gone", "v"), ("making", "v"),
    ("taking", "v"), ("writing", "v"), ("coming", "v"),
    ("using", "v"), ("stopped", "v"), ("bought", "v"),
    ("eaten", "v"), ("analyzing", "v"), ("processing", "v"),
    ("becoming", "v"), ("better", "a"), ("worse", "a"),
    ("happier", "a"), ("simpler", "a"), ("fascinating", "v")
]


# ---------------- TEXT PROCESSING ----------------

def process_text():
    text = input("\nEnter a sentence: ").strip()

    if not text:
        print("Please enter some text.")
        return

    results = preprocess_with_mapping(text)

    print("\n" + "-" * 58)
    print(f"{'ORIGINAL WORD':20} {'STEM':15} {'LEMMA':15}")
    print("-" * 58)

    for original, stem, lemma in results:
        print(f"{original:20} {stem:15} {lemma:15}")

    choice = input("\nShow detailed preprocessing pipeline? (y/n): ").strip().lower()

    if choice == "y":
        show_pipeline(text)


# ---------------- STEMMING EVALUATION ----------------

def evaluate_stemmer():
    results, accuracy = evaluate(*STEM_TEST_WORDS)

    print("\nSTEMMER EVALUATION")
    print("-" * 58)
    print(f"Words tested: {len(STEM_TEST_WORDS)}")
    print(f"Agreement with NLTK: {accuracy:.2f}%")

    show_details = input("\nShow word-by-word comparison? (y/n): ").strip().lower()

    if show_details == "y":
        print(f"\n{'WORD':20} {'OUR STEM':20} {'NLTK STEM':20} {'RESULT'}")
        print("-" * 72)

        for word, our_stem, nltk_stem, status in results:
            print(f"{word:20} {our_stem:20} {nltk_stem:20} {status}")

    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    with open(output_dir / "stemming_results.csv", "w",
              newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Word", "Our Stemmer", "NLTK Stemmer", "Result"])
        writer.writerows(results)

    print("\nDetailed results saved to results/stemming_results.csv")


# ---------------- LEMMATIZATION EVALUATION ----------------

def evaluate_our_lemmatizer():
    results, accuracy = evaluate_lemmatizer(LEMMA_TEST_WORDS)

    print("\nLEMMATIZER EVALUATION")
    print("-" * 58)
    print(f"Words tested: {len(LEMMA_TEST_WORDS)}")
    print(f"Agreement with NLTK WordNet: {accuracy:.2f}%")

    show_details = input("\nShow word-by-word comparison? (y/n): ").strip().lower()

    if show_details == "y":
        print(f"\n{'WORD':16} {'POS':6} {'OUR LEMMA':18} {'WORDNET':18} {'RESULT'}")
        print("-" * 78)

        for word, pos, our_lemma, nltk_lemma, status in results:
            print(
                f"{word:16} {pos:6} {our_lemma:18} "
                f"{nltk_lemma:18} {status}"
            )


# ---------------- MAIN MENU ----------------

def main():
    while True:
        print("\n" + "=" * 48)
        print("   NLP STEMMING & LEMMATIZATION SYSTEM")
        print("=" * 48)
        print("1. Process text")
        print("2. Evaluate stemmer")
        print("3. Evaluate lemmatizer")
        print("4. Exit")
        print("-" * 48)

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            process_text()
        elif choice == "2":
            evaluate_stemmer()
        elif choice == "3":
            evaluate_our_lemmatizer()
        elif choice == "4":
            print("\nThank you for using the NLP system!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
