import streamlit as st
import requests
import pandas as pd
import altair as alt

API_URL = "http://localhost:8000"

def predict_sentiment(reviews):
    response = requests.post(f"{API_URL}/predictions", json={"reviews": reviews})
    return response.json()

st.header("Sentiment Analysis")
st.write("This app uses Natural Language Processing (NLP) to analyze the sentiment of the product reviews given")

# Initialize an empty list to store reviews
reviews = []

# This loop is replaced with a condition to take reviews one at a time
review = st.text_input("Please enter the review below", key="unique_review_input")

submit_button_html = """
<div style="display: flex; justify-content: center; margin-top: 10px;">
    <button style="
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        cursor: pointer;
        box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    ">Submit</button>
</div>
"""

# When the "Submit" button is clicked, append the review and reset the input field
if review:
    reviews.append(review)
    st.success(f"Review added: {review}")

if st.markdown(submit_button_html, unsafe_allow_html=True):
    if reviews:
        st.write("All reviews submitted, now you can predict sentiment.")
    else:
        st.error("Please enter at least one review")

predict_button_html = """
<div style="display: flex; justify-content: center; margin-top: 10px;">
    <button style="
        background-color: #2196F3;
        color: white;
        font-size: 16px;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        cursor: pointer;
        box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    ">Predict Sentiment</button>
</div>
"""

# Predict sentiment when the "Predict Sentiment" button is pressed
if st.markdown(predict_button_html, unsafe_allow_html=True):
    if reviews:
        sentiment = predict_sentiment(reviews)
        st.session_state['sentiment'] = sentiment
        # Display the sentiment analysis results
        for result in st.session_state['sentiment']:
            st.subheader(f"Review: {result['review']}")
            # Determine the color based on the sentiment
            if result["sentiment"] == "positive":
                sentiment_color = "green"
            elif result["sentiment"] == "negative":
                sentiment_color = "red"
            else:
                sentiment_color = "darkblue"

            # Display the sentiment with the appropriate color
            st.markdown(f'<p style="font-size: 18px; color: {sentiment_color}; font-weight: bold;">Sentiment: {result["sentiment"]}</p>',
                         unsafe_allow_html=True)

            # Create a DataFrame for confidence scores
            confidence_data = pd.DataFrame({
                "Sentiment": ["Negative", "Positive", "Neutral"],
                "Confidence": [
                    result["negative_confidence"], 
                    result["positive_confidence"], 
                    result["neutral_confidence"]
                ],
                "Color": ["red", "green", "blue"]  # Assign colors to sentiments
            })

            # Create a bar chart using Altair
            chart = alt.Chart(confidence_data).mark_bar().encode(
                x=alt.X("Sentiment", title="Sentiment"),
                y=alt.Y("Confidence", title="Confidence Score"),
                color=alt.Color("Sentiment", scale=alt.Scale(domain=["Negative", "Positive", "Neutral"], 
                                                             range=["red", "green", "blue"])),
                tooltip=["Sentiment", "Confidence"]
            ).properties(
                width=500,
                height=300
            )

            # Display the chart
            st.altair_chart(chart, use_container_width=True)
    else:
        st.error("Please enter at least one review before predicting sentiment.")
