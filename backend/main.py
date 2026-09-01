from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Product Review API is running"
    }


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


classifier = pipeline(
    "zero-shot-classification",
    model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
)


class Review(BaseModel):
    review: str


@app.post("/check-review")
def check_review(data: Review):

    text = data.review

    if not text or not text.strip():
        return {
            "show": False,
            "message": "Empty review"
        }

    result = classifier(
        text,
        candidate_labels=[
            "positive review",
            "negative review"
        ]
    )

    sentiment = result["labels"][0]


    # Positive review
    if sentiment == "positive review":

        return {
            "show": True,
            "review": text,
            "message": "Positive review approved"
        }


    # Negative review ko file mein store karo
    with open(
        "negative_reviews.txt",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(text + "\n")


    return {
        "show": False,
        "message": "Negative review rejected and stored"
    }