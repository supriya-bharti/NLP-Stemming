# lemmatizer.py

irregular_words = {
    "children": "child",
    "mice": "mouse",
    "men": "man",
    "women": "woman",
    "feet": "foot",
    "teeth": "tooth",
    "geese": "goose",
    "better": "good",
    "worse": "bad",
    "went": "go",
    "gone": "go",
    "ate": "eat",
    "eaten": "eat",
    "bought": "buy",
    "brought": "bring"
}

special_words = {
    "processing": "process",
    "types": "type",
    "analyzing": "analyze",
    "analysing": "analyse",
    "linguistics": "linguistics",
    "preprocessing": "preprocess",
    "becoming": "become"
}

def lemmatize(word):

    # Check irregular words first
    if word in irregular_words:
        return irregular_words[word]


    if word in special_words:
        return special_words[word]
    
    # Comparative adjectives
    if word.endswith("ier") and len(word) > 4:
        return word[:-3] + "y"

    if word.endswith("er") and len(word) > 4:
        stem = word[:-2]

        # simpler → simple, not simpl
        if stem.endswith("l"):
            return stem + "e"

        # bigger → big
        if len(stem) >= 2 and stem[-1] == stem[-2]:
            stem = stem[:-1]

        return stem

    # Words ending in "ies"
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"

    
    # Words ending in "ing"
    if word.endswith("ing") and len(word) >= 5:
        stem = word[:-3]

        # running → run
        if len(stem) >= 2 and stem[-1] == stem[-2]:
            stem = stem[:-1]

        # Restore final "e" for selected words
        silent_e_words = {
            "mak": "make",
            "tak": "take",
            "writ": "write",
            "com": "come",
            "us": "use"
        }

        if stem in silent_e_words:
            return silent_e_words[stem]

        # fascinating → fascinate
        if stem.endswith("nat"):
            return stem + "e"

        return stem


    # Words ending in "ed"
    if word.endswith("ed") and len(word) > 4:
        stem = word[:-2]

        # stopped → stop
        if len(stem) >= 2 and stem[-1] == stem[-2]:
            stem = stem[:-1]

        return stem

    
    # Plural words ending in "ses", "shes", "ches", "xes", or "zes"
    if word.endswith(("sses", "shes", "ches", "xes", "zes")):
        return word[:-2]

    # Other words ending in "es"
    if word.endswith("es") and len(word) > 4:
        return word[:-2]


    # Plural words ending in "s"
    if word.endswith("s") and len(word) > 3:
        if word.endswith(("ss", "us", "is")):
            return word

        return word[:-1]

    return word