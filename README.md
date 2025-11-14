# Credit Card Fraud Detection System Using ML  
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)  
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red)  
![scikit--learn](https://img.shields.io/badge/scikit_learn-1.3%2B-orange)  
![License](https://img.shields.io/badge/License-MIT-green)

## Data Set Download Link
    https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

---
 **Real-time fraud detection web app** using **Logistic Regression** and **Streamlit**.  
 Upload any `creditcard.csv`, auto-balance classes, train instantly, and test transactions with **30 features** (`Time`, `V1–V28`, `Amount`).  
 **V1–V28 are PCA-anonymized** – privacy preserved.


---


## Features


| Feature | Description |
|-------|-----------|
| **CSV Upload** | Upload Data set Downloaded From Kaggle `creditcard.csv` |
| **Auto-Balancing** | Undersamples legit class to match fraud count |
| **Instant Training** | Logistic Regression trains in seconds |
| **Real-time Prediction** | Enter 30 feature values → get **Fraud / Legit** result |
| **Sample Load Buttons** | One-click load real fraud/legit examples |
| **Clean UI** | Wide layout, responsive, user-friendly |
| **No Scaling Needed** | V1–V28 already PCA-transformed |


---

## How It Works

### 1. **Data Preprocessing**
**legit**
```python
legit = data[data.Class == 0]
```
**fraud**
```
fraud = data[data.Class == 1]
```
**legit sample**
```
legit_sample = legit.sample(n=len(fraud))
```
**balanced**
```
balanced = pd.concat([legit_sample, fraud])
```
### 2. Train-Test Split
```
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=2
)
```
### 3. Model

```
model = LogisticRegression()
model.fit(X_train, y_train)
```


### 4. Prediction

User inputs: Time, V1, V2, ..., V28, Amount
Model predicts: 0 = Legitimate | 1 = Fraudulent

V1 to V28 – What Are They?

Anonymized PCA Components

Original features (card number, location, merchant, etc.) were transformed using Principal Component Analysis (PCA).
V1–V28 = New numerical features (no real-world meaning).
Privacy preserved – cannot reverse to original data.



You input numerical values only – just like in the dataset.
