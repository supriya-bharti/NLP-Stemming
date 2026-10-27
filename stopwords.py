
STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "am",
    "to", "of", "in", "on", "for", "and", "or", "but",
    "with", "this", "that", "it", "i", "my", "you",
    "he", "she", "they", "we"
}


def remove_stopwords(tokens):
    return [
        word for word in tokens
        if word not in STOPWORDS
    ]


if __name__ == "__main__":
    tokens = ["i", "love", "natural", "language", "processing"]
    print(remove_stopwords(tokens))
