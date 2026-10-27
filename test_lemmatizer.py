
from lemmatizer import lemmatize

expected_lemmas = {
    "making": "make",
    "taking": "take",
    "writing": "write",
    "coming": "come",
    "using": "use",
    "applications": "application",
    "researchers": "researcher",
    "fascinating": "fascinate",
    "cats": "cat",
    "studies": "study",
    "wishes": "wish",
    "teeth": "tooth",
    "children": "child",
    "mice": "mouse",
    "feet": "foot",
    "geese": "goose",
    "happier": "happy",
    "simpler": "simple",
    "running": "run",
    "studying": "study",
    "stopped": "stop",
    "classes": "class",
    "wishes": "wish",
    "watches": "watch",
    "boxes": "box"
}

passed = 0

for word, expected in expected_lemmas.items():
    actual = lemmatize(word)

    if actual == expected:
        status = "PASS"
        passed += 1
    else:
        status = "FAIL"

    print(f"{word:15} Expected: {expected:10} Actual: {actual:10} {status}")

total = len(expected_lemmas)
accuracy = (passed / total) * 100

print(f"\nPassed: {passed}/{total}")
print(f"Agreement with expected lemmas: {accuracy:.2f}%")
