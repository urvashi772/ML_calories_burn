# 🔥 Fitness & Diet Planner (ML Based)

A Machine Learning based Streamlit web application that predicts calories burned during exercise and provides personalized food recommendations based on user fitness goals.

---

## 🚀 Project Overview

This application allows users to:

- 👤 Select Gender
- 🎯 Choose Fitness Goal (Weight Loss / Weight Gain)
- 🎂 Enter Age & Weight
- ⏱ Select Exercise Duration
- 🔥 Predict Calories Burned using XGBoost
- 🥗 Get Personalized Food Suggestions
- 💪 Receive Goal-Based Diet & Workout Advice

The system combines Machine Learning + Smart Diet Recommendation to create a complete fitness assistant.

---

## 🧠 Machine Learning Model

- Algorithm: **XGBoost Regressor**
- Dataset: Calories Burn Dataset
- Features Used:
  - Age
  - Height (average)
  - Weight
  - Exercise Duration (minutes)
  - Heart Rate (average)
  - Body Temperature (average)
  - Gender (Encoded)

The model predicts estimated calories burned based on exercise duration and physical attributes.

---

## 🥗 Diet Recommendation System

### 🔥 Weight Loss Mode
- Low calorie foods
- High fiber vegetables
- Lean protein
- Avoid fried & sugary foods
- Cardio workout suggestion

### 💪 Weight Gain Mode
- High protein foods
- Calorie surplus focus
- Muscle building foods
- Strength training suggestion

---

## 🖥 App Flow
Gender Selection
↓
Goal Selection (Loss/Gain)
↓
Age + Weight Input
↓
Exercise Hours
↓
Calories Prediction
↓
Personalized Food Suggestion


---

## 🛠 Tech Stack

Python

Streamlit

Pandas

NumPy

XGBoost

Scikit-learn

## 🎯 Key Features

✔ Multi-step interactive UI
✔ Dynamic title update
✔ Session state handling
✔ Machine Learning prediction
✔ Personalized diet plan
✔ Clean and structured code