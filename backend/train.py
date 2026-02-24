import pandas as pd
from ai_model import train_models_from_df

def main():
    df = pd.read_csv("../data/gastos.csv")
    # Normalize column names to expected ones
    df = df.rename(columns={
        "gastos": "valor",
        "descricao": "descricao",
        "categoria": "categoria",
        "mes": "mes"
    })
    # Ensure types
    df["mes"] = df["mes"].astype(int)
    df["valor"] = df["valor"].astype(float)
    train_models_from_df(df)
    print("Treinamento concluído e modelos salvos em backend/")

if __name__ == "__main__":
    main()
