import streamlit as st
import numpy as np
import pandas as pd
from xgboost import XGBRegressor

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(page_title="Fitness & Diet Predictor", page_icon="🔥")

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
# Session Setup
# -------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 1

# -------------------------------------------------
# Dynamic Title
# -------------------------------------------------
if "gender" in st.session_state:
    st.title(f"🔥 {st.session_state.gender} Fitness & Diet Planner")
else:
    st.title("🔥 Fitness & Diet Planner")

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
# STEP 2 → Goal
# -------------------------------------------------
elif st.session_state.step == 2:

    st.subheader("🎯 Select Your Goal")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔥 Weight Loss"):
            st.session_state.goal = "Weight Loss"
            st.session_state.step = 3

    with col2:
        if st.button("💪 Weight Gain"):
            st.session_state.goal = "Weight Gain"
            st.session_state.step = 3

# -------------------------------------------------
# STEP 3 → Age + Weight
# -------------------------------------------------
elif st.session_state.step == 3:

    st.subheader("📋 Enter Your Details")

    age = st.slider("Age", 10, 80, 25)
    weight = st.slider("Weight (kg)", 30, 150, 70)

    if st.button("Next ➡"):
        st.session_state.age = age
        st.session_state.weight = weight
        st.session_state.step = 4

# -------------------------------------------------
# STEP 4 → Exercise Hours
# -------------------------------------------------
elif st.session_state.step == 4:

    st.subheader("⏱ Select Exercise Duration")

    hours = st.slider("Exercise Hours", 0.5, 5.0, 1.0, step=0.5)

    if st.button("🔥 Calculate Calories"):

        st.session_state.hours = hours
        duration_minutes = hours * 60

        # Average fixed values
        height = 170
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
                                st.session_state.weight,
                                duration_minutes,
                                heart_rate,
                                body_temp,
                                gender_female,
                                gender_male]])

        prediction = model.predict(input_data)

        st.session_state.calories = prediction[0]
        st.session_state.step = 5

# -------------------------------------------------
# STEP 5 → Result + Food Suggestion
# -------------------------------------------------
elif st.session_state.step == 5:

    st.success("🔥 Calories Prediction Result")

    st.write("### 📋 Your Details:")
    st.write(f"👤 Gender: {st.session_state.gender}")
    st.write(f"🎯 Goal: {st.session_state.goal}")
    st.write(f"🎂 Age: {st.session_state.age}")
    st.write(f"⚖ Weight: {st.session_state.weight} kg")
    st.write(f"⏱ Exercise: {st.session_state.hours} hours")

    st.write("### 🔥 Estimated Calories Burned:")
    st.success(f"{st.session_state.calories:.2f} Calories")

    # ---------------- FOOD SUGGESTION ----------------

    st.write("## 🥗 Personalized Food Suggestion")

    if st.session_state.goal == "Weight Loss":

        st.info("Calorie Deficit Diet Plan")

        st.write("### 🥦 Recommended Foods:")
        st.markdown("""
        - 🥗 Spinach, Broccoli, Cucumber
        - 🍎 Apple, Papaya, Orange
        - 🍗 Boiled Chicken
        - 🥚 Egg Whites
        - 🥣 Oats, Brown Rice
        - 🥛 Low-fat Yogurt
        - 🥜 Almonds (Limited)
        """)

        st.write("### 🚫 Avoid:")
        st.markdown("""
        - 🍟 Fried Food
        - 🍕 Fast Food
        - 🥤 Sugary Drinks
        - 🍩 Sweets & Bakery
        """)

        st.success("👉 Do 30-45 min cardio daily + Maintain calorie deficit.")

    else:

        st.info("Calorie Surplus Muscle Building Plan")

        st.write("### 💪 Recommended Foods:")
        st.markdown("""
        - 🍗 Chicken Breast, Fish
        - 🥚 Whole Eggs
        - 🥛 Milk, Peanut Butter
        - 🍚 Rice, Potatoes
        - 🍌 Banana Shake
        - 🥜 Dry Fruits
        - 🧀 Paneer
        """)

        st.success("👉 Focus on strength training + High protein intake.")

    if st.button("🔄 Start Again"):
        st.session_state.clear()