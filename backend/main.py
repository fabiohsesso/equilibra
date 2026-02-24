from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import select
from database import init_db, get_session
from models_db import User, Transaction, Goal
from schemas import UserCreate, TransactionCreate, GoalCreate
from sqlmodel import Session
import ai_model
from typing import List
import math

app = FastAPI(title="Equilibra - Finance AI API")

# Inicializa DB
init_db()

# --- Users ---
@app.post("/users/", response_model=dict)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User(name=user.name, email=user.email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"id": db_user.id, "name": db_user.name, "email": db_user.email}

@app.get("/users/{user_id}", response_model=dict)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email, "balance": user.balance}

# --- Transactions ---
@app.post("/transactions/", response_model=dict)
def create_transaction(tx: TransactionCreate, session: Session = Depends(get_session)):
    # classify description automatically
    try:
        categoria = ai_model.classify_descricao(tx.descricao)
    except Exception:
        categoria = None
    db_tx = Transaction(user_id=tx.user_id, mes=tx.mes, valor=tx.valor, descricao=tx.descricao, categoria=categoria, data=tx.data)
    session.add(db_tx)
    session.commit()
    session.refresh(db_tx)
    return {"id": db_tx.id, "categoria": db_tx.categoria}

@app.get("/transactions/user/{user_id}", response_model=List[dict])
def list_transactions(user_id: int, session: Session = Depends(get_session)):
    statement = select(Transaction).where(Transaction.user_id == user_id)
    results = session.exec(statement).all()
    return [t.dict() for t in results]

# --- Goals ---
@app.post("/goals/", response_model=dict)
def create_goal(goal: GoalCreate, session: Session = Depends(get_session)):
    db_goal = Goal(user_id=goal.user_id, title=goal.title, target_amount=goal.target_amount, current_amount=goal.current_amount, target_date=goal.target_date)
    session.add(db_goal)
    session.commit()
    session.refresh(db_goal)
    return {"id": db_goal.id, "title": db_goal.title}

@app.get("/goals/user/{user_id}", response_model=List[dict])
def list_goals(user_id: int, session: Session = Depends(get_session)):
    statement = select(Goal).where(Goal.user_id == user_id)
    results = session.exec(statement).all()
    return [g.dict() for g in results]

# --- Analytics endpoints ---
@app.get("/analytics/predict_month/{mes}", response_model=dict)
def predict_month(mes: int):
    try:
        pred = ai_model.predict_gasto(mes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"mes": mes, "previsao_gasto": round(pred, 2)}

@app.get("/analytics/analyze_transaction/")
def analyze_transaction(descricao: str, valor: float = 0.0):
    """
    Retorna categoria sugerida, se é anomalia e score de previsão para mês atual.
    """
    try:
        categoria = ai_model.classify_descricao(descricao)
    except Exception:
        categoria = None
    try:
        anomaly = ai_model.detect_anomaly(valor)
    except Exception:
        anomaly = None
    return {"descricao": descricao, "categoria_sugerida": categoria, "anomaly_flag": anomaly}

@app.get("/goals/projection/{goal_id}", response_model=dict)
def goal_projection(goal_id: int, session: Session = Depends(get_session)):
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    # Estimate monthly average expense using last 6 months from DB
    stmt = select(Transaction).where(Transaction.user_id == goal.user_id).order_by(Transaction.id.desc()).limit(6)
    txs = session.exec(stmt).all()
    if txs:
        avg_monthly_spend = sum(t.valor for t in txs) / max(1, len(txs))
    else:
        avg_monthly_spend = 0.0

    # Simple strategy: recommend saving = (target_amount - current_amount) / months_until_target
    # If no target_date, compute months needed assuming user saves 20% of avg monthly spend
    remaining = max(0.0, goal.target_amount - goal.current_amount)
    if goal.target_date:
        # compute months until target_date (approx)
        from datetime import datetime
        try:
            target_dt = datetime.fromisoformat(goal.target_date)
            now = datetime.now()
            months = max(1, (target_dt.year - now.year) * 12 + (target_dt.month - now.month))
        except Exception:
            months = 12
        monthly_needed = remaining / months
        months_needed = months
    else:
        # assume user can save 20% of avg monthly spend
        suggested_save = max(1.0, 0.2 * avg_monthly_spend)
        months_needed = math.ceil(remaining / suggested_save) if suggested_save > 0 else None
        monthly_needed = suggested_save if months_needed is not None else None

    return {
        "goal_id": goal.id,
        "title": goal.title,
        "remaining_amount": round(remaining, 2),
        "avg_monthly_spend": round(avg_monthly_spend, 2),
        "monthly_needed": round(monthly_needed, 2) if monthly_needed else None,
        "months_needed": months_needed
    }
