import joblib

def prever_gasto(mes: int):
    modelo = joblib.load("modelo_gastos.pkl")
    return modelo.predict([[mes]])[0]

def classificar_transacao(descricao: str):
    modelo = joblib.load("modelo_classificacao.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    X_new = vectorizer.transform([descricao])
    return modelo.predict(X_new)[0]
