#Esse script treina os modelos e salva os arquivos .pkl

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Carregar dataset
df = pd.read_csv("data/gastos.csv")

# --- Modelo de previsão de gastos ---
X = df[["mes"]]
y = df["gastos"]

regressor = LinearRegression()
regressor.fit(X, y)
joblib.dump(regressor, "modelo_gastos.pkl")

# --- Modelo de classificação de categorias ---
vectorizer = CountVectorizer()
X_text = vectorizer.fit_transform(df["descricao"])
y_cat = df["categoria"]

clf = MultinomialNB()
clf.fit(X_text, y_cat)

joblib.dump(clf, "modelo_classificacao.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Modelos treinados e salvos com sucesso!")
