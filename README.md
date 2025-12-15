AI Intern Assessment
## Overview
End-to-end AI-powered restaurant feedback system featuring rating prediction through prompt engineering and a production-ready two-dashboard web application for customer feedback management.


## Task 1: Rating Prediction

Evaluated 3 prompting approaches on Yelp reviews:
- V1 Basic: 61.1% accuracy
- V2 Few-Shot: 63.6% accuracy (best)
- V3 Structured: 44.4% accuracy
- <img width="702" height="200" alt="image" src="https://github.com/user-attachments/assets/c9b11f52-2ecf-4220-bc68-d4d53b8eea4b" />


**Model:** Google Gemini 2.5 Flash  
**Dataset:** 200 sampled Yelp reviews

## Task 2: Two Dashboards

**User Dashboard:** Customer feedback portal with AI-generated responses  
<img width="1832" height="983" alt="image" src="https://github.com/user-attachments/assets/b1019488-dff7-4841-a92f-b4d7ee426b2f" />

**Admin Dashboard:** Real-time analytics with AI summaries and action recommendations
<img width="1859" height="1013" alt="image" src="https://github.com/user-attachments/assets/0143544b-b817-439d-9687-d7e1a344d50c" />


**Tech Stack:** Streamlit + Google Gemini API + CSV storage

## Deployment Links
- User Dashboard: https://ai-talent-aquisition-ry6pxqxjsiy8xzeknrz5sb.streamlit.app/
- Admin Dashboard: https://ai-talent-aquisition-mdxrmqz2g677azbvnxvdwv.streamlit.app/
- Assessment Report Link: https://drive.google.com/file/d/18x6Kp7499EtxBFVTS6gRukXZLcz8e5rK/view?usp=sharing
## Key Features
- 3 prompt engineering techniques with evaluation
- Interactive rating slider with step-by-step guidance
- Real-time AI responses using RTC prompting framework
- Live admin analytics with filtering and sorting
- Automated business insights and recommendations

## Technologies
Python | Streamlit | Google Gemini API | Pandas | Jupyter
