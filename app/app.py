import joblib
import pandas as pd
import streamlit as st
from pandas.api.types import CategoricalDtype
import numpy as np

# Load model and scaler

model = joblib.load('app/model.joblib')
scaler = joblib.load('app/scaler.joblib')

# Load data
file_path = 'data/Azerbaijan_bank_customers.csv'
df = pd.read_csv(file_path)

# Title
st.markdown("<h1 style='text-align: center;'>🔮 Customer Churn Prediction App</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>👥 Understand if a customer is likely to leave your bank</h4>", unsafe_allow_html=True)

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120)
with st.sidebar:
    st.header("📋 Customer Details")
    age = st.slider("🎂 Age", int(df['age'].min()), int(df['age'].max()), int(df['age'].min()))
    gender = st.radio("👤 Gender", ['Qadın', 'Kişi'])
    balance = st.slider("💰 Balance", int(df['balance'].min()), int(df['balance'].max()), int(df['balance'].mean()))
    credit_rating = st.slider("📊 Credit Rating", int(df['credit_rating'].min()), int(df['credit_rating'].max()), int(df['credit_rating'].mean()))
    is_active = st.checkbox("✅ Is Active?")
    monthly_income = st.slider("🤑 Monthly Income", float(df['monthly_income'].min()), float(df['monthly_income'].max()), df['monthly_income'].mean())
    credit_eligible = st.checkbox("🏦 Credit Eligible?")
    tenure = st.slider("📅 Tenure (Years)", int(df['tenure'].min()), int(df['tenure'].max()), int(df['tenure'].mean()))
    num_of_products = st.slider("📦 Number of Products", int(df['num_of_products'].min()), int(df['num_of_products'].max()), int(df['num_of_products'].mean()))
    has_credit_card = st.radio("💳 Has Credit Card?", ['yes', 'no'])
    estimated_salary = st.slider("💼 Estimated Salary", float(df['estimated_salary'].min()), float(df['estimated_salary'].max()), float(df['estimated_salary'].mean()))
    account = st.selectbox("🏛️ Account Type", ["Əmanət", "Cari", "Biznes", "Depozit"])
    branch = st.selectbox("📍 Branch", ["Bakı", "Gəncə", "Sumqayıt", "Şəki", "Lənkəran", "Mingəçevir", "Naxçıvan", "Qax", "Zaqatala", "Quba", "Qusar"])

# Organize input
input_data = {
    "age": [age],
    "gender": [gender],
    "balance": [balance],
    "credit_rating": [credit_rating],
    "is_active": [is_active],
    "monthly_income": [monthly_income],
    "credit_eligible": [credit_eligible],
    "tenure": [tenure],
    "num_of_products": [num_of_products],
    "has_credit_card": [has_credit_card],
    "estimated_salary": [estimated_salary],
    "account": [account],
    "branch": [branch]
}
input_df = pd.DataFrame(input_data)

# Display raw input
with st.expander("🛠️ Raw Input Data"):
    st.dataframe(input_df)

# Encoding
binary_cols = ['gender', 'has_credit_card']
binary_map = {'Kişi': 1, 'Qadın': 0, 'yes': 1, 'no': 0}
for col in binary_cols:
    input_df[col] = input_df[col].map(binary_map)

account_type = ["Biznes", "Cari", "Depozit", "Əmanət"]
branch_type = ["Bakı", "Gəncə", "Lənkəran", "Mingəçevir", "Naxçıvan", "Qax", "Quba", "Qusar", "Sumqayıt", "Zaqatala", "Şəki"]

input_df['account'] = input_df['account'].astype(CategoricalDtype(categories=account_type))
input_df = pd.get_dummies(input_df, columns=['account'], prefix='account')

input_df['branch'] = input_df['branch'].astype(CategoricalDtype(categories=branch_type))
input_df = pd.get_dummies(input_df, columns=['branch'], prefix='branch')

with st.expander("📦 Encoded Data"):
    st.dataframe(input_df)

# Scale
scaled_input = scaler.transform(input_df)

# Show scaled input
with st.expander("📊 Scaled Input Data"):
    st.dataframe(pd.DataFrame(scaled_input, columns=input_df.columns))

# Prediction
prediction = model.predict(scaled_input)[0]
prediction_proba = model.predict_proba(scaled_input)[0]

# Result Section
st.markdown("---")
st.subheader("🔍 Prediction Result")

col1, col2 = st.columns([1, 2])
with col1:
    emoji = "✅" if prediction == 0 else "⚠️"
    label = "Customer will stay" if prediction == 0 else "Customer might churn"
    st.success(f"{emoji} **{label}**")

with col2:
    st.markdown("#### 🔢 Prediction Probability")
    st.progress(prediction_proba[1])
    st.write(f"💡 Churn Probability: `{prediction_proba[1]:.2%}`")
    st.write(f"✔️ Retention Probability: `{prediction_proba[0]:.2%}`")

st.markdown("---")
st.caption("📍 This tool helps banks identify customers at risk of churning and take preventive actions.")
