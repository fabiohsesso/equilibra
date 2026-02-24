# Equilibra - App de Organização de Finanças Pessoais com IA

Este projeto é um protótipo de **API em Python com FastAPI** que utiliza **Inteligência Artificial** para:
- Prever gastos futuros com base em dados históricos.
- Classificar transações automaticamente em categorias (ex.: Transporte, Alimentação, Lazer).

O projeto foi desenvolvido como parte do desafio **"Criando um APP de Organização de Finanças Pessoais com Vibe Coding"** do Bootcamp CAIXA – Inteligência Artificial na Prática.

---

## 🚀 Tecnologias utilizadas
- [Python 3.13+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Scikit-learn](https://scikit-learn.org/)
- [Pandas](https://pandas.pydata.org/)
- [Joblib](https://joblib.readthedocs.io/)

---

## 📂 Estrutura do projeto
equilibra/
│── data/
│   └── gastos.csv          # Dataset fictício
│── train.py                # Script para treinar os modelos
│── model.py                # Funções de previsão e classificação
│── main.py                 # API FastAPI
│── requirements.txt        # Dependências do projeto
│── README.md               # Documentação


---

## ⚙️ Instalação e execução

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/equilibra.git
cd equilibra

### 2. Crie o ambiente virtual
python -m venv venv

### Ative o ambiente
Windows (PowerShell): 
.\venv\Scripts\activate

Linux/Mac:
source venv/bin/activate

### 3. Instale as dependências
pip install -r requirements.txt

### 4. Treine os modelos
python train.py

### 5. Rode a API
uvicorn main:app --reload
