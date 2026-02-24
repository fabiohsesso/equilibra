from fastapi import FastAPI
from model import prever_gasto, classificar_transacao

app = FastAPI(title="Finance AI API")

@app.get("/")
def root():
    return {"message": "API de Finanças Pessoais com IA"}

@app.get("/prever/{mes}")
def previsao(mes: int):
    valor = prever_gasto(mes)
    return {"mes": mes, "previsao_gasto": round(valor, 2)}

@app.get("/classificar/")
def classificacao(descricao: str):
    categoria = classificar_transacao(descricao)
    return {"descricao": descricao, "categoria_sugerida": categoria}
