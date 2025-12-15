import streamlit as st
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

st.set_page_config(
    page_title="Customer Feedback",
    page_icon="★",
    layout="centered"
)


load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-2.5-flash')
DATA_FILE = "submissions.csv"

def get_ai_response(rating, review_text):
    """
    This function generates a personalized response using AI
    Had to tweak this prompt multiple times to get natural-sounding responses
    """
    # Using RTCROS prompting framework
    prompt = f"""Role: You are a professional customer service manager at a restaurant who genuinely cares about customer feedback.

Task: Write a personalized response to the following customer review.

Context: 
- Customer Rating: {rating} out of 5 stars
- Customer Review: "{review_text}"
- This response will be shown immediately to the customer after they submit feedback
- Keep it brief (2-3 sentences only)

Reasoning:
- If rating is 4-5 stars: Show genuine appreciation and encourage them to return
- If rating is 3 stars: Thank them honestly and acknowledge room for improvement
- If rating is 1-2 stars: Apologize sincerely without making excuses, show commitment to fixing issues

Output: Write ONLY the response message in plain text. No labels, no JSON, no extra formatting.

Stopping Condition: Stop after generating one response message."""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        # Backup responses if API fails 
        if rating >= 4:
            return f"Thank you so much for your {rating}-star review! We're thrilled you enjoyed your experience and hope to see you again soon."
        elif rating == 3:
            return "Thank you for your feedback. We appreciate your input and are always working to improve."
        else:
            return f"We sincerely apologize for your experience. Your feedback helps us improve, and we'd love the opportunity to make things right."

def save_submission(rating, review, ai_response):
    """
    Saves the submission to CSV
    Simple append logic - check if file exists first
    """
    new_data = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'rating': rating,
        'review': review,
        'ai_response': ai_response
    }
    
   
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    else:
        df = pd.DataFrame([new_data])
    
    df.to_csv(DATA_FILE, index=False)

# Main UI 
st.title("Share Your Experience With Us")
st.write("Your honest feedback helps us serve you better. It only takes a minute!")

st.write("")
st.write("")

st.subheader("Step 1: Rate Your Experience")
st.write("**Drag the slider below to select your rating** (1 = Poor, 5 = Excellent)")

st.markdown("""
<style>
    .stSlider {
        padding: 20px 0px;
        background-color: #f0f2f6;
        border-radius: 10px;
        margin: 10px 0px;
    }
</style>
""", unsafe_allow_html=True)


rating = st.select_slider(
    label="Slide to rate",
    options=[1, 2, 3, 4, 5],
    value=3,  # Start in middle so users notice they need to change it
    format_func=lambda x: "★" * x + " " + "☆" * (5-x),
    help="Drag the slider left or right to change your rating",
    label_visibility="collapsed"
)

rating_labels = {
    1: "Very Poor",
    2: "Poor", 
    3: "Average",
    4: "Good",
    5: "Excellent"
}

st.markdown(f"<h2 style='text-align: center; color: #ff6b6b;'>{'★' * rating}{'☆' * (5-rating)} - {rating_labels[rating]}</h2>", unsafe_allow_html=True)

st.write("")
st.write("")

# Review section
st.subheader("Step 2: Tell Us More")
st.write("What made your experience " + rating_labels[rating].lower() + "?")

review = st.text_area(
    label="Your detailed review",
    placeholder="Tell us about the food quality, service, ambiance, cleanliness, or anything else...",
    height=150,
    label_visibility="collapsed"
)



st.write("")
st.write("")

# Submit section
st.subheader("Step 3: Submit Your Feedback")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    submit_button = st.button("Submit My Feedback", type="primary", use_container_width=True)



# Handle the submission
if submit_button:
    if review.strip() and len(review.strip()) >= 10:
        with st.spinner("Processing your feedback..."):
            ai_response = get_ai_response(rating, review)
            
            
            save_submission(rating, review, ai_response)
        
        st.success("Thank you! Your feedback has been submitted.")
        
        
        st.info(f"**Our Response to You:**\n\n{ai_response}")
        
        #Balloons
        if rating >= 4:
            st.balloons()
            
    elif not review.strip():
        st.warning("Please write a review before submitting.")
    else:
        st.warning("Please write at least 10 characters to help us understand your experience better.")


st.write("")
st.write("")
st.markdown("---")
st.caption("Thank you for taking the time to share your feedback with us.")
