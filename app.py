import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import streamlit as st

# load data
data = pd.read_csv('creditcard.csv')

# separate legitimate and fraudulent transactions
legit = data[data.Class == 0]
fraud = data[data.Class == 1]

# undersample legitimate transactions to balance the classes
legit_sample = legit.sample(n=len(fraud), random_state=2)
data = pd.concat([legit_sample, fraud], axis=0)

# split data into training and testing sets
X = data.drop(columns="Class", axis=1)
y = data["Class"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=2)

# scale features to help convergence
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# train logistic regression model with increased iterations
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

# evaluate model performance
train_acc = accuracy_score(model.predict(X_train_scaled), y_train)
test_acc = accuracy_score(model.predict(X_test_scaled), y_test)

# create Streamlit app
st.title("Credit Card Fraud Detection Model")
st.write("Model trained. Training accuracy: {:.4f}, Test accuracy: {:.4f}".format(train_acc, test_acc))
st.write("Enter feature values below (one input per field) and click Submit.")

# load full csv once more to provide sample rows for user convenience
full_data = pd.read_csv('creditcard.csv')

# helper to populate session_state keys
def populate_session_with_row(row):
    for i, col in enumerate(X.columns):
        key = f"feat_{i}"
        # use float(row[col]) in case values are strings
        try:
            st.session_state[key] = float(row[col])
        except Exception:
            st.session_state[key] = 0.0

st.write("Quick samples:")
col1, col2 = st.columns(2)
with col1:
    if st.button("Load first fraud sample"):
        fraud_rows = full_data[full_data['Class'] == 1]
        if len(fraud_rows) > 0:
            populate_session_with_row(fraud_rows.iloc[0])
        else:
            st.warning("No fraud rows found in CSV")
with col2:
    if st.button("Load first legit sample"):
        legit_rows = full_data[full_data['Class'] == 0]
        if len(legit_rows) > 0:
            populate_session_with_row(legit_rows.iloc[0])
        else:
            st.warning("No legit rows found in CSV")

# build a form with numeric inputs for each feature to avoid comma-parsing issues
with st.form("input_form"):
    input_values = []
    for i, col in enumerate(X.columns):
        key = f"feat_{i}"
        # provide existing session_state value if present, else default 0.0
        default_val = float(st.session_state.get(key, 0.0))
        val = st.number_input(label=col, value=default_val, format="%.6f", key=key)
        input_values.append(val)
    submitted = st.form_submit_button("Submit")

if submitted:
    try:
        features = np.array(input_values, dtype=np.float64).reshape(1, -1)
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)
        if prediction[0] == 0:
            st.success("Legitimate transaction")
        else:
            st.error("Fraudulent transaction")
    except Exception as e:
        st.error(f"Error processing input: {e}")
