# Churn Predictor Streamlit App with PostgreSQL

An end-to-end machine learning application that predicts employee churn using synthetically generated data. It features a Streamlit-based front-end, a machine learning model, and PostgreSQL for data storage.

---

## 🧩 Features

- Generates realistic employee data using `Faker`
- Stores generated data in a PostgreSQL database via `psycopg3`
- Trains a churn prediction model with `scikit-learn`
- Interactive Streamlit UI for real-time predictions
- Notebook for data generation and model training

---

## ⚙️ Tech Stack

- Python
- Streamlit
- scikit-learn
- psycopg3
- PostgreSQL
- Faker
- pandas / numpy / matplotlib

---

## 📂 Project Structure

churn-predictor-streamlit-postgres/
├── app
  ├── app.py # Streamlit application
  ├── model.joblib # Trained model
  ├── scaler.joblib
├── data
  ├── Azerbaijan_bank_customers.csv (data that created with faker)
├── data_generating
  ├── main.py  # Main notebook (Faker) 
├── model
  ├── preprocess_and_train.ipynb # Main notebook (ETL + training)
├── store_postgre
  ├── main.ipynb # PostgreSQL connection setup (psycopg2)  
├── requirements.txt # All dependencies
└──  README.md # Project documentation


