import joblib
import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import IsolationForest

MODEL_DIR = os.path.dirname(__file__)

MODEL_GASTOS = os.path.join(MODEL_DIR, "modelo_gastos.pkl")
MODEL_CLASS = os.path.join(MODEL_DIR, "modelo_classificacao.pkl")
VECTORIZER = os.path.join(MODEL_DIR, "vectorizer.pkl")
MODEL_ANOMALY = os.path.join(MODEL_DIR, "modelo_anomalia.pkl")

def train_models_from_df(df: pd.DataFrame):
    """
    Treina e salva modelos a partir de um DataFrame com colunas:
    ['mes','valor','descricao','categoria']
    """
    # Regressão para previsão de gastos por mês (usando mes -> valor)
    X = df[["mes"]]
    y = df["valor"]
    reg = LinearRegression()
    reg.fit(X, y)
    joblib.dump(reg, MODEL_GASTOS)

    # Classificação de descrição -> categoria
    vectorizer = CountVectorizer()
    X_text = vectorizer.fit_transform(df["descricao"].astype(str))
    clf = MultinomialNB()
    clf.fit(X_text, df["categoria"].astype(str))
    joblib.dump(clf, MODEL_CLASS)
    joblib.dump(vectorizer, VECTORIZER)

    # Anomalia (IsolationForest) baseado em valor
    iso = IsolationForest(contamination=0.05, random_state=42)
    iso.fit(df[["valor"]])
    joblib.dump(iso, MODEL_ANOMALY)

def load_regressor():
    return joblib.load(MODEL_GASTOS)

def load_classifier():
    return joblib.load(MODEL_CLASS), joblib.load(VECTORIZER)

def load_anomaly():
    return joblib.load(MODEL_ANOMALY)

def predict_gasto(mes: int):
    reg = load_regressor()
    pred = reg.predict([[mes]])[0]
    return float(pred)

def classify_descricao(descricao: str):
    clf, vectorizer = load_classifier()
    X_new = vectorizer.transform([descricao])
    pred = clf.predict(X_new)[0]
    return str(pred)

def detect_anomaly(valor: float):
    iso = load_anomaly()
    pred = iso.predict([[valor]])  # -1 anomaly, 1 normal
    return int(pred[0])
