@'
# Equilibra - App de Organização de Finanças Pessoais com IA

Projeto protótipo profissionalizado de backend e IA para um aplicativo de finanças pessoais. Inclui **API REST** com FastAPI, **banco SQLite** via SQLModel, **módulos de IA** (classificação, previsão, detecção de anomalias), scripts de treino, e endpoints para CRUD de usuários, transações e metas. Pronto para integração com frontend (React Native) e publicação no GitHub.

---

## Estrutura do repositório e arquivos principais

**Estrutura recomendada**
equilibra/ 
    │── data/ 
    │ └── gastos.csv 
    │── backend/ 
    │ ├── main.py 
    │ ├── database.py 
    │ ├── models_db.py 
    │ ├── schemas.py 
    │ ├── ai_model.py 
    │ ├── train.py 
    │ └── requirements.txt 
    │── .gitignore 
    │── README.md

    
**Principais arquivos e responsabilidades**
- **backend/main.py** — API FastAPI com rotas para usuários, transações, metas e analytics.
- **backend/database.py** — inicialização do SQLite e sessão SQLModel.
- **backend/models_db.py** — modelos ORM: User, Transaction, Goal.
- **backend/schemas.py** — Pydantic schemas para validação de entrada.
- **backend/ai_model.py** — treino, persistência e inferência dos modelos de IA.
- **backend/train.py** — script que carrega `data/gastos.csv`, treina e salva modelos.
- **data/gastos.csv** — dataset inicial fictício para treino.
- **requirements.txt** — dependências do backend.
- **.gitignore** — ignorar venv, caches, arquivos binários e modelos.

---

## Instalação e execução local

**1. Clone e entre na pasta**
```bash
git clone https://github.com/seu-usuario/equilibra.git
cd equilibra/backend

**2. Crie e ativo ambiente virtual**
python -m venv venv
# Windows PowerShell
.\venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

**3. Instale dependências**
pip install -r requirements.txt

**4. Treine os modelos**
python train.py

**5. Rode e a API**
uvicorn main:app --reload

Acesse a documentação interativa:
http://127.0.0.1:8000/docs

Endpoints principais e exemplos

Usuários
    POST /users/ — criar usuário
    Body: {"name":"Fábio","email":"fabio@example.com"}  
    Resposta: {"id":1,"name":"Fábio","email":"fabio@example.com"}
    GET /users/{user_id} — obter usuário

Transações
    POST /transactions/ — criar transação (classificação automática)
    Body: {"user_id":1,"mes":11,"valor":900,"descricao":"Padaria","data":"2026-02-24"}  
    Resposta: {"id":10,"categoria":"Alimentação"}
    GET /transactions/user/{user_id} — listar transações do usuário

Metas
    POST /goals/ — criar meta
    Body: {"user_id":1,"title":"Viagem","target_amount":5000,"current_amount":500,"target_date":"2026-12-01"}
    GET /goals/user/{user_id} — listar metas do usuário
    GET /goals/projection/{goal_id} — projeção da meta

    Resposta exemplo:
    {
        "goal_id": 1,
        "title": "Viagem",
        "remaining_amount": 4500.0,
        "avg_monthly_spend": 1500.0,
        "monthly_needed": 375.0,
        "months_needed": 12
    }

Analytics e IA

    GET /analytics/predict_month/{mes} — previsão de gasto para mês
    GET /analytics/analyze_transaction/?descricao=Padaria&valor=900 — retorna categoria sugerida e flag de anomalia

IA e lógica de negócio

    Modelos implementados
    Classificação de transações: CountVectorizer + MultinomialNB para mapear descricao → categoria.
    Previsão de gastos: LinearRegression (mês → gasto) como protótipo; fácil substituição por ARIMA/LSTM/Prophet.
    Detecção de anomalias: IsolationForest para sinalizar gastos atípicos.

    Projeção de metas
    Se target_date informado: calcula meses até a data e divide o valor restante por meses.
    Se target_date não informado: sugere economia mensal baseada em 20% do gasto médio dos últimos 6 meses; calcula meses necessários.
    avg_monthly_spend é calculado a partir das últimas transações do usuário (últimos 6 registros por padrão).

    Comportamento automático

    Ao criar transação, o backend tenta classificar automaticamente a categoria e salva junto.

    Endpoint de análise retorna categoria sugerida, flag de anomalia e previsão de gasto.