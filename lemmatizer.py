
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
    "brought": "bring",
    "took": "take",
    "taken": "take",
    "given": "give",
"gave": "give",
"drove": "drive",
"slept": "sleep",
"swam": "swim",
"written": "write",
"wolves": "wolf",
"leaves": "leaf",
"knives": "knife"
}

special_words = {
    "processing": "process",
    "types": "type",
    "analyzing": "analyze",
    "analysing": "analyse",
    "linguistics": "linguistics",
    "preprocessing": "preprocess",
    "becoming": "become",
    "buses": "bus"
}


def lemmatize(word, pos="n"):
    word = word.lower()

    # Check irregular words first
    if word in irregular_words:
        return irregular_words[word]

    if word in special_words:
        return special_words[word]

    # Verb rules
    
    # Verb rules
    if pos == "v":

        # Words ending in "ing"
        if word.endswith("ing") and len(word) >= 5:
            stem = word[:-3]

            # running -> run
            if len(stem) >= 2 and stem[-1] == stem[-2]:
                stem = stem[:-1]

            silent_e_words = {
                "mak": "make",
                "tak": "take",
                "writ": "write",
                "com": "come",
                "us": "use"
            }

            if stem in silent_e_words:
                return silent_e_words[stem]

            # fascinating -> fascinate
            if stem.endswith("nat"):
                return stem + "e"

            return stem

        # Words ending in "ied"
        # studied -> study, tried -> try
        if word.endswith("ied") and len(word) > 4:
            return word[:-3] + "y"

        # Words ending in "ed"
        if word.endswith("ed") and len(word) > 4:
            stem = word[:-2]

            # stopped -> stop
            if len(stem) >= 2 and stem[-1] == stem[-2]:
                stem = stem[:-1]

            # smiled -> smile, danced -> dance
            if stem.endswith(("il", "anc", "os", "iv")):
                return stem + "e"

            return stem

        # Words ending in "ies"
        # studies -> study, tries -> try
        if word.endswith("ies") and len(word) > 4:
            return word[:-3] + "y"

        # Words ending in "es"
        # watches -> watch, fixes -> fix
        if word.endswith("es") and len(word) > 4:
            return word[:-2]

        # Words ending in "s"
        # walks -> walk, carries -> carry
        if word.endswith("s") and len(word) > 3:
            if word.endswith("ss"):
                return word

            return word[:-1]


    

    # Adjective rules
    if pos == "a":

        # happier -> happy, easier -> easy
        if word.endswith("ier") and len(word) > 4:
            return word[:-3] + "y"

        # strongest -> strong, biggest -> big
        if word.endswith("est") and len(word) > 4:
            stem = word[:-3]

            if len(stem) >= 2 and stem[-1] == stem[-2]:
                stem = stem[:-1]

            return stem

        # smaller -> small, faster -> fast
        if word.endswith("er") and len(word) > 4:
            stem = word[:-2]

            # Remove doubled consonant
            if len(stem) >= 2 and stem[-1] == stem[-2]:
                if stem[-1] != "l":
                    stem = stem[:-1]

            # simpler -> simple
            if stem in ("simpl", "nobl", "abl"):
                return stem + "e"

            return stem


    # Noun rules
    if pos == "n":

        # studies -> study
        if word.endswith("ies") and len(word) > 4:
            return word[:-3] + "y"

        # Plural words ending in "sses", "shes", "ches", "xes", or "zes"
        if word.endswith(("sses", "shes", "ches", "xes", "zes")):
            return word[:-2]

        
        # Words ending in "es"
    # houses -> house
    if word == "houses":
        return "house"

    # tomatoes -> tomato, potatoes -> potato
    if word.endswith(("oes",)):
        return word[:-2]

    # Other words ending in es
    if word.endswith("es") and len(word) > 4:
        if word.endswith(("ses", "zes")):
            return word[:-1]
        return word[:-2]

        # words ending in "s"
    if word.endswith("s") and len(word) > 2:
        if word.endswith(("ss", "us", "is")):
            return word

        return word[:-1]

    return word

