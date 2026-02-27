import streamlit as st
import numpy as np
import pandas as pd
from xgboost import XGBRegressor

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(page_title="Calories Predictor", page_icon="🔥")

# -------------------------------------------------
# Train Model (Cached)
# -------------------------------------------------
@st.cache_resource
def train_model():
    calories = pd.read_csv("calories.csv")
    exercise_data = pd.read_csv("exercise.csv")

    calories_data = pd.concat([exercise_data, calories['Calories']], axis=1)
    calories_data = pd.get_dummies(calories_data, columns=['Gender'])

    X = calories_data.drop(columns=['User_ID', 'Calories'], axis=1)
    Y = calories_data['Calories']

    model = XGBRegressor()
    model.fit(X, Y)

    return model

model = train_model()

# -------------------------------------------------
# Session State Setup
# -------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 1

# -------------------------------------------------
# Dynamic Title
# -------------------------------------------------
if "gender" not in st.session_state:
    st.title("🔥 Calories Burn Predictor")
else:
    if st.session_state.gender == "Male":
        st.markdown("<h1 style='color:blue;'>🔥 Male Calories Burn Predictor</h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='color:pink;'>🔥 Female Calories Burn Predictor</h1>", unsafe_allow_html=True)

# -------------------------------------------------
# STEP 1 → Gender
# -------------------------------------------------
if st.session_state.step == 1:

    st.subheader("👤 Select Your Gender")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("♂ Male"):
            st.session_state.gender = "Male"
            st.session_state.step = 2

    with col2:
        if st.button("♀ Female"):
            st.session_state.gender = "Female"
            st.session_state.step = 2

# -------------------------------------------------
# STEP 2 → Age
# -------------------------------------------------
elif st.session_state.step == 2:

    st.subheader("🎂 Select Your Age")

    age = st.slider("Age", 10, 80, 25)

    if st.button("Next ➡"):
        st.session_state.age = age
        st.session_state.step = 3

# -------------------------------------------------
# STEP 3 → Hours
# -------------------------------------------------
elif st.session_state.step == 3:

    st.subheader("⏱ Select Exercise Duration (Hours)")

    hours = st.slider("Hours of Exercise", 0.5, 5.0, 1.0, step=0.5)

    if st.button("🔥 Calculate Calories"):

        st.session_state.hours = hours

        duration_minutes = hours * 60

        # Default average values
        height = 170
        weight = 70
        heart_rate = 100
        body_temp = 37.0

        if st.session_state.gender == "Male":
            gender_male = 1
            gender_female = 0
        else:
            gender_male = 0
            gender_female = 1

        input_data = np.array([[st.session_state.age,
                                height,
                                weight,
                                duration_minutes,
                                heart_rate,
                                body_temp,
                                gender_female,
                                gender_male]])

        prediction = model.predict(input_data)

        st.session_state.calories = prediction[0]
        st.session_state.step = 4

# -------------------------------------------------
# STEP 4 → Result Page
# -------------------------------------------------
elif st.session_state.step == 4:

    st.success("🔥 Calories Prediction Result")

    st.write("### 📋 Your Selected Details:")
    st.write(f"👤 Gender: {st.session_state.gender}")
    st.write(f"🎂 Age: {st.session_state.age} years")
    st.write(f"⏱ Exercise Duration: {st.session_state.hours} hours")

    st.write("### 🔥 Estimated Calories Burned:")
    st.success(f"{st.session_state.calories:.2f} Calories")

    if st.button("🔄 Start Again"):
        st.session_state.clear()