import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv
import time


st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="★",
    layout="wide"
)
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-2.5-flash')
DATA_FILE = "submissions.csv"

def generate_summary_and_action(review_text, rating):
    """
    This generates business insights from customer reviews
    Using structured prompting to get consistent outputs
    """
    #RTCROS Prompt
    prompt = f"""Role: You are a senior restaurant operations analyst who specializes in analyzing customer feedback and providing actionable business recommendations.

Task: Analyze the following customer review and generate two things:
1. A concise summary of what the customer experienced
2. A specific action recommendation for restaurant management

Context:
- Customer Rating: {rating} out of 5 stars
- Customer Review Text: "{review_text}"
- This analysis will be used by management to prioritize improvements
- Focus on concrete, actionable insights rather than generic advice

Reasoning:
- Extract the key positive or negative aspects mentioned
- Identify specific operational areas (food quality, service speed, cleanliness, staff behavior, etc.)
- Consider the severity based on the star rating
- Recommend specific actions that can be taken within the next week

Output Format:
SUMMARY: [Write one clear sentence summarizing the review]
ACTION: [Write one specific, actionable recommendation for management]

Stopping Condition: Stop after generating exactly one summary sentence and one action recommendation."""

    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        
        #Parse the response 
        if "SUMMARY:" in content and "ACTION:" in content:
            summary_part = content.split("ACTION:")[0].replace("SUMMARY:", "").strip()
            action_part = content.split("ACTION:")[1].strip()
            return summary_part, action_part
        else:
            # Fallback if format doesn't match
            lines = [line.strip() for line in content.split("\n") if line.strip()]
            summary_part = lines[0] if lines else f"Customer left {rating} star review"
            action_part = lines[1] if len(lines) > 1 else "Review this feedback and follow up"
            return summary_part, action_part
            
    except Exception as e:
        # Basic fallback if something breaks
        return f"Customer gave {rating} stars", "Manually review this feedback"

#header
st.title("Admin Dashboard - Customer Feedback Analytics")
st.write("Real-time view of all customer submissions with AI-powered insights")

if not os.path.exists(DATA_FILE):
    st.warning("No customer feedback data found yet.")
    st.info("The User Dashboard needs to be deployed and customers need to submit feedback first.")
    st.stop()


df = pd.read_csv(DATA_FILE)

# Add columns for AI insights if they don't exist
# This handles the case when new submissions come in
if 'ai_summary' not in df.columns:
    df['ai_summary'] = ""
if 'recommended_action' not in df.columns:
    df['recommended_action'] = ""

# Process any new submissions that don't have AI analysis yet
pending_analysis = df[(df['ai_summary'] == "") | (df['ai_summary'].isna())]

if len(pending_analysis) > 0:
    progress_text = f"Analyzing {len(pending_analysis)} new submission(s)..."
    with st.spinner(progress_text):
        for idx in pending_analysis.index:
            summary, action = generate_summary_and_action(
                df.loc[idx, 'review'],
                df.loc[idx, 'rating']
            )
            df.loc[idx, 'ai_summary'] = summary
            df.loc[idx, 'recommended_action'] = action
            time.sleep(0.3)  # Small delay to avoid hitting rate limits
        
        df.to_csv(DATA_FILE, index=False)
        st.success("Analysis complete!")
        time.sleep(1)
        st.rerun()

#metrics
st.markdown("## Key Performance Indicators")
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    total_reviews = len(df)
    st.metric("Total Reviews Received", total_reviews)

with metric_col2:
    avg_rating = df['rating'].mean()
    st.metric("Average Customer Rating", f"{avg_rating:.1f} ★")

with metric_col3:
    excellent_count = len(df[df['rating'] == 5])
    st.metric("5-Star Reviews", excellent_count)

with metric_col4:
    needs_attention = len(df[df['rating'] <= 2])
    st.metric("Low Ratings (Needs Attention)", needs_attention)

st.markdown("---")

st.markdown("## Rating Distribution Analysis")

#chart
rating_counts = df['rating'].value_counts().sort_index()
chart_data = pd.DataFrame({
    'Rating': [f"{i} ★" for i in range(1, 6)],
    'Number of Reviews': [rating_counts.get(i, 0) for i in range(1, 6)]
})

st.bar_chart(chart_data.set_index('Rating'))

st.markdown("---")

st.markdown("## All Customer Submissions")

# Filter controls
filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    selected_ratings = st.multiselect(
        "Filter by Star Rating",
        options=[1, 2, 3, 4, 5],
        default=[1, 2, 3, 4, 5],
        format_func=lambda x: f"{x} ★"
    )

with filter_col2:
    sort_option = st.selectbox(
        "Sort Order",
        options=["Most Recent First", "Oldest First", "Highest Rated First", "Lowest Rated First"]
    )

# Apply filters
filtered_data = df[df['rating'].isin(selected_ratings)].copy()

#sorting
if sort_option == "Most Recent First":
    filtered_data = filtered_data.sort_values('timestamp', ascending=False)
elif sort_option == "Oldest First":
    filtered_data = filtered_data.sort_values('timestamp', ascending=True)
elif sort_option == "Highest Rated First":
    filtered_data = filtered_data.sort_values('rating', ascending=False)
else:
    filtered_data = filtered_data.sort_values('rating', ascending=True)

#display table
table_data = filtered_data[['timestamp', 'rating', 'review', 'ai_summary', 'recommended_action']].copy()
table_data.columns = ['Timestamp', 'Rating', 'Customer Review', 'AI Summary', 'Management Action']

# Format rating as stars
table_data['Rating'] = table_data['Rating'].apply(lambda x: "★" * x + "☆" * (5-x))

st.dataframe(
    table_data,
    use_container_width=True,
    height=400,
    hide_index=True
)

# Control buttons
st.markdown("---")
button_col1, button_col2, button_col3 = st.columns([1, 1, 1])

with button_col2:
    if st.button("Refresh Dashboard", use_container_width=True):
        st.rerun()

st.markdown("---")
last_updated = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
st.caption(f" Total submissions in database: {len(df)}")
