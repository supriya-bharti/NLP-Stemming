
def is_consonant(word, i):

    if word[i] in "aeiou":
        return False

    if word[i] == "y":
        if i == 0:
            return True
        return not is_consonant(word, i - 1)

    return True

def is_vowel_at(word, index):
    return not is_consonant(word, index)




def measure(word):

    m = 0
    i = 0

    while i < len(word):

        # Skip consonants
        while i < len(word) and is_consonant(word, i):
            i += 1

        # Skip vowels
        while i < len(word) and not is_consonant(word, i):
            i += 1

        # We completed a VC sequence
        if i < len(word):
            m += 1

    return m

def contains_vowel(word):
    for i in range(len(word)):
        if not is_consonant(word, i):
            return True

    return False


def step1a(word):

    if word.endswith("sses"):
        word = word[:-2]

    elif word.endswith("ies"):
        word = word[:-2]

    elif word.endswith("ss"):
        word = word

    elif word.endswith("s"):
        word = word[:-1]

    return word

def step1b(word):

    # Rule 1: eed -> ee
    if word.endswith("eed"):
        stem = word[:-3]

        if measure(stem) > 0:
            word = stem + "ee"

    # Rule 2: ed
    elif word.endswith("ed"):
        stem = word[:-2]

        if contains_vowel(stem):
            word = stem

            # Post-processing
            if word.endswith(("at", "bl", "iz")):
                word += "e"

            elif word.endswith(("bb", "dd", "ff", "gg",
                                "mm", "nn", "pp", "rr",
                                "tt", "cc")):
                word = word[:-1]

            elif measure(word) == 1 and cvc(word):
                word += "e"

    # Rule 3: ing
    elif word.endswith("ing"):
        stem = word[:-3]

        if contains_vowel(stem):
            word = stem

            # Post-processing
            if word.endswith(("at", "bl", "iz")):
                word += "e"

            elif word.endswith(("bb", "dd", "ff", "gg",
                                "mm", "nn", "pp", "rr",
                                "tt", "cc")):
                word = word[:-1]

            elif measure(word) == 1 and cvc(word):
                word += "e"

    return word

def step1c(word):

    if word.endswith("y"):

        stem = word[:-1]

        if contains_vowel(stem):
            word = stem + "i"

    return word


step2_rules = {
    "ational": "ate",
    "tional": "tion",
    "enci": "ence",
    "anci": "ance",
    "izer": "ize",
    "bli": "ble",
    "alli": "al",
    "entli": "ent",
    "eli": "e",
    "ousli": "ous",
    "ization": "ize",
    "ation": "ate",
    "ator": "ate",
    "alism": "al",
    "iveness": "ive",
    "fulness": "ful",
    "ousness": "ous",
    "aliti": "al",
    "iviti": "ive",
    "biliti": "ble",
    "logi": "log"
}

def step2(word):

    for suffix, replacement in step2_rules.items():

        if word.endswith(suffix):

            stem = word[:-len(suffix)]

            if measure(stem) > 0:
                word = stem + replacement

            break

    return word

step3_rules = {
    "icate": "ic",
    "ative": "",
    "alize": "al",
    "iciti": "ic",
    "ical": "ic",
    "ful": "",
    "ness": ""
}

def step3(word):

    for suffix, replacement in step3_rules.items():

        if word.endswith(suffix):

            stem = word[:-len(suffix)]

            if measure(stem) > 0:
                word = stem + replacement

            break

    return word

step4_suffixes = [
    "al",
    "ance",
    "ence",
    "er",
    "ic",
    "able",
    "ible",
    "ant",
    "ement",
    "ment",
    "ent",
    "ion",
    "ou",
    "ism",
    "ate",
    "iti",
    "ous",
    "ive",
    "ize"
]


def step4(word):

    for suffix in step4_suffixes:

        if word.endswith(suffix):

            stem = word[:-len(suffix)]

            if measure(stem) > 1:

                # Special rule for "ion"
                if suffix == "ion":

                    if stem.endswith("s") or stem.endswith("t"):
                        word = stem

                else:
                    word = stem

            break

    return word

def cvc(word):

    if len(word) < 3:
        return False

    i = len(word) - 1

    if (
        is_consonant(word, i)
        and not is_consonant(word, i - 1)
        and is_consonant(word, i - 2)
    ):

        if word[i] not in "wxy":
            return True

    return False

def step5a(word):

    if word.endswith("e"):

        stem = word[:-1]
        m = measure(stem)

        if m > 1:
            word = stem

        elif m == 1 and not cvc(stem):
            word = stem

    return word

def step5b(word):

    if word.endswith("ll"):

        stem = word[:-1]

        if measure(stem) > 1:
            word = stem

    return word

def step5(word):

    word = step5a(word)

    word = step5b(word)

    return word

def porter_stem(word):

    word = step1a(word)

    word = step1b(word)

    word = step1c(word)
    word = step2(word)
    word = step3(word)
    word = step4(word)
    word = step5(word)
    return word



