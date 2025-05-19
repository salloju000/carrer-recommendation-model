import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model and encoders
model = joblib.load('career_model.pkl')
label_encoders = joblib.load('encoders.pkl')

# ----- Custom Page Styling -----
st.set_page_config(page_title="Career Predictor", page_icon="🎯", layout="centered")

st.markdown(
    """
    <style>
        /* Global Styling for Dark Theme */
        .main {
            background-color: #121212;
            color: #fff;
            font-family: 'Arial', sans-serif;
            height: 100vh;
        }

        /* Title */
        .title {
            font-size: 48px;
            font-weight: 600;
            text-align: center;
            margin-top: 30px;
            color: #fff;
            text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.6);
        }

        /* Subtitle */
        .subtitle {
            font-size: 20px;
            text-align: center;
            margin-top: 10px;
            color: #b2bec3;
            font-weight: 400;
            margin-bottom: 30px;
        }

        /* Button Styling */
        .stButton>button {
            background-color: #2ecc71;
            color: white;
            border: none;
            padding: 0.5em 1.5em;
            font-size: 18px;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            transition: background-color 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #27ae60;
        }

        /* Slider Styling */
        .stSlider>div>div>input {
            width: 90%;
            margin: 0 auto;
            background: #444;
            border-radius: 10px;
            height: 8px;
        }

        .stSlider>div>div>input::-webkit-slider-runnable-track {
            background: #2ecc71;
            border-radius: 10px;
        }

        .stSlider>div>div>input::-webkit-slider-thumb {
            background: #fff;
            border-radius: 50%;
            height: 20px;
            width: 20px;
            border: 2px solid #2ecc71;
            cursor: pointer;
        }

        /* Result Box Styling */
        .result-box {
            padding: 30px;
            background-color: #2d3436;
            border-radius: 12px;
            margin-top: 30px;
            border-left: 5px solid #2ecc71;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            text-align: center;
        }

        /* Simple Animation for Result */
        .result-box h3 {
            font-size: 24px;
            font-weight: 700;
            color: #2ecc71;
        }

        .result-box p {
            font-size: 22px;
            font-weight: bold;
            color: #fff;
        }
    </style>
    """, unsafe_allow_html=True
)

# ----- Title -----
st.markdown('<div class="title">🎯 Career Path Recommendation</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Fill in your academic interests and skill levels to get personalized career suggestions.</div>', unsafe_allow_html=True)

# ----- Inputs -----
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("📅 Age", min_value=13, max_value=60, value=20)
        education_background = st.selectbox("🎓 Education Background", label_encoders['education_background'].classes_)
        favorite_subject = st.selectbox("📘 Favorite Subject", label_encoders['favorite_subject'].classes_)
        technical_skills = st.selectbox("💻 Technical Skill", label_encoders['technical_skills'].classes_)

    with col2:
        preferred_work_style = st.selectbox("🏢 Preferred Work Style", label_encoders['preferred_work_style'].classes_)
        
        # Sliders (Refined look)
        communication_skills = st.slider("🗣️ Communication Skills", 1, 5, 3)
        problem_solving_skills = st.slider("🧠 Problem Solving Skills", 1, 5, 4)
        creativity_level = st.slider("🎨 Creativity Level", 1, 5, 3)
        interest_in_research = st.slider("🔬 Interest in Research", 1, 5, 3)
        logical_reasoning_score = st.slider("🧩 Logical Reasoning Score", 1, 10, 7)

# ----- Prepare Input -----
input_data = pd.DataFrame([{
    'age': age,
    'education_background': label_encoders['education_background'].transform([education_background])[0],
    'favorite_subject': label_encoders['favorite_subject'].transform([favorite_subject])[0],
    'technical_skills': label_encoders['technical_skills'].transform([technical_skills])[0],
    'communication_skills': communication_skills,
    'problem_solving_skills': problem_solving_skills,
    'creativity_level': creativity_level,
    'interest_in_research': interest_in_research,
    'preferred_work_style': label_encoders['preferred_work_style'].transform([preferred_work_style])[0],
    'logical_reasoning_score': logical_reasoning_score
}])

# ----- Prediction Button -----
if st.button("🔍 Predict Career Path"):
    prediction = model.predict(input_data)
    result = label_encoders['chosen_career_path'].inverse_transform(prediction)[0]
    
    st.markdown(
        f"""
        <div class="result-box">
            <h3>✅ Recommended Career Path:</h3>
            <p>{result}</p>
        </div>
        """, unsafe_allow_html=True
    )
