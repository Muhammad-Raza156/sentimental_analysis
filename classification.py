import cohere
import streamlit as st
from cohere import ClassifyExample
from models import ProductReviews
from dotenv import load_dotenv
import os

load_dotenv()
# get api key from .env
cohere_api_key = st.secrets["COHERE_API_KEY"]

# COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(cohere_api_key)

def classify_sentiment(product_reviews: ProductReviews):
    examples=[ClassifyExample(text="The order came 5 days early", label="positive"), 
            ClassifyExample(text="The item exceeded my expectations", label="positive"), 
            ClassifyExample(text="I ordered more for my friends", label="positive"), 
            ClassifyExample(text="I would buy this again", label="positive"), 
            ClassifyExample(text="I would recommend this to others", label="positive"), 
            ClassifyExample(text="The package was damaged", label="negative"), 
            ClassifyExample(text="The order is 5 days late", label="negative"), 
            ClassifyExample(text="The order was incorrect", label="negative"), 
            ClassifyExample(text="I want to return my item", label="negative"), 
            ClassifyExample(text="The item's material feels low quality", label="negative"), 
            ClassifyExample(text="The item was nothing special", label="neutral"), 
            ClassifyExample(text="I would not buy this again but it wasn't a waste of money", label="neutral"), 
            ClassifyExample(text="The item was neither amazing or terrible", label="neutral"), 
            ClassifyExample(text="The item was okay", label="neutral"), 
            ClassifyExample(text="I have no emotions towards this item", label="neutral")]
    
    response = co.classify(
        model="embed-english-v2.0",
        inputs=product_reviews.reviews,
        examples=examples)

    return response.classifications
