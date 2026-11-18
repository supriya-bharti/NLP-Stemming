
import string
from stemmer import porter_stem
from tokenizer import tokenize
from stopwords import remove_stopwords
from lemmatizer import lemmatize
from pos_tagger import detect_pos_with_context

def preprocess(text):

    # 1. Convert to lowercase
    text = text.lower()

    # 2. Remove punctuation
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # 3. Tokenize
    tokens = tokenize(text)

    # 4. Remove stopwords
    tokens = remove_stopwords(tokens)

    # 5. Apply Porter Stemmer
    stemmed_tokens = [
        porter_stem(word)
        for word in tokens
    ]

    return stemmed_tokens



def preprocess_with_mapping(text):
    text = text.lower()

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)

    # Detect POS automatically
    tagged_words = detect_pos_with_context(tokens)

    result = []

    for word, pos in tagged_words:
        stemmed = porter_stem(word)

        # Keep other words unchanged
        if pos == "other":
            lemmatized = word
        else:
            lemmatized = lemmatize(word, pos)

        result.append((word, stemmed, lemmatized, pos))

    return result



def show_pipeline(text):

    import string

    print("\nOriginal Text:")
    print(text)

    # Lowercase
    text = text.lower()
    print("\n1. Lowercase:")
    print(text)

    # Remove punctuation
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )
    print("\n2. Punctuation Removed:")
    print(text)

    # Tokenization
    tokens = tokenize(text)
    print("\n3. Tokenization:")
    print(tokens)

    # Stopword removal
    tokens = remove_stopwords(tokens)
    print("\n4. Stopword Removal:")
    print(tokens)

    # Stemming
    stemmed = [
        porter_stem(word)
        for word in tokens
    ]

    print("\n5. Porter Stemming:")
    print(stemmed)

    return stemmed