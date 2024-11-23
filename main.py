from fastapi import FastAPI
from models import ProductReviews
from classification import classify_sentiment

app = FastAPI()

@app.post("/predictions")
def predict_sentiment(product_reviews: ProductReviews):
    report=[]
    response = classify_sentiment(product_reviews)
    for classification in response:
       report.append({"review": classification.input, "sentiment": classification.prediction, 
                      "score": classification.confidence, "negative_confidence": classification.labels["negative"].confidence,
                       "positive_confidence": classification.labels["positive"].confidence, 
                       "neutral_confidence": classification.labels["neutral"].confidence})    
    return report