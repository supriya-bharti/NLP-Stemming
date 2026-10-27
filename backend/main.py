
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


@app.get("/")
def home():
    return {"message": "NLP API is running!"}


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

    return {
        "original_text": request.text,
        "operation": request.operation,
        "results": output,
    }
