import string
from tokenizer import tokenize
from stopwords import remove_stopwords
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from evaluation import evaluate
from lemmatization_evaluation import evaluate_lemmatizer
from stemmer import porter_stem
from lemmatizer import lemmatize
from preprocessing import preprocess_with_mapping, show_pipeline

app = FastAPI(title="NLP Stemming and Lemmatization API")

# Allow our React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextRequest(BaseModel):
    text: str
    operation: str = "both"
    show_steps: bool = False

class LemmatizationEvaluationRequest(BaseModel):
    text: str
    pos: str
    
def get_preprocessing_steps(text):
    steps = []

    steps.append({
        "name": "Original Text",
        "value": text
    })

    text = text.lower()
    steps.append({
        "name": "Lowercase",
        "value": text
    })

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )
    steps.append({
        "name": "Punctuation Removed",
        "value": text
    })

    tokens = tokenize(text)
    steps.append({
        "name": "Tokenization",
        "value": tokens
    })

    tokens = remove_stopwords(tokens)
    steps.append({
        "name": "Stopword Removal",
        "value": tokens
    })

    return steps

@app.post("/evaluate/stemming")
def evaluate_stemming(request: TextRequest):
    if not request.text.strip():
        return {"error": "Please enter some text."}

    words = request.text.lower().split()

    results, accuracy = evaluate(*words)

    output = []

    for word, my_stem, nltk_stem, status in results:
        output.append({
            "word": word,
            "custom_stem": my_stem,
            "nltk_stem": nltk_stem,
            "status": status
        })

    return {
        "total_words": len(words),
        "accuracy": round(accuracy, 2),
        "results": output
    }
@app.post("/evaluate/lemmatization")
def evaluate_lemmatization(request: LemmatizationEvaluationRequest):

    if not request.text.strip():
        return {"error": "Please enter some text."}

    if request.pos not in ["n", "v", "a"]:
        return {"error": "Invalid Part of Speech."}

    words = request.text.lower().split()

    test_words = [(word, request.pos) for word in words]

    results, accuracy = evaluate_lemmatizer(test_words)

    output = []

    for word, pos, our_result, nltk_result, status in results:
        output.append({
            "word": word,
            "pos": pos,
            "custom_lemma": our_result,
            "nltk_lemma": nltk_result,
            "status": status
        })

    return {
        "total_words": len(words),
        "accuracy": round(accuracy, 2),
        "results": output
    }
    
@app.get("/")
def home():
    return {"message": "NLP API is running!"}




def get_preprocessing_steps(text):
    steps = []

    steps.append({
        "name": "Original Text",
        "value": text
    })

    text = text.lower()
    steps.append({
        "name": "Lowercase",
        "value": text
    })

    text = text.translate(str.maketrans("", "", string.punctuation))
    steps.append({
        "name": "Punctuation Removed",
        "value": text
    })

    tokens = tokenize(text)
    steps.append({
        "name": "Tokenization",
        "value": tokens
    })

    tokens = remove_stopwords(tokens)
    steps.append({
        "name": "Stopword Removal",
        "value": tokens
    })

    return steps

@app.post("/process")
def process_text(request: TextRequest):
    if not request.text.strip():
        return {"error": "Please enter some text."}

    if request.operation not in ["stemming", "lemmatization", "both"]:
        return {"error": "Invalid operation selected."}

    # Use the existing preprocessing pipeline
    results = preprocess_with_mapping(request.text)

    output = []

    for original, stem, lemma in results:
        item = {"word": original}

        if request.operation in ["stemming", "both"]:
            item["stem"] = stem

        if request.operation in ["lemmatization", "both"]:
            item["lemma"] = lemma

        output.append(item)
    steps = get_preprocessing_steps(request.text) if request.show_steps else []
    return {
        "original_text": request.text,
        "operation": request.operation,
        "results": output,
        "preprocessing_steps": steps,
    }
