import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Organizze Clone API")

# Inicialização do Banco de Dados SQLite
def init_db():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL, -- 'receita' ou 'despesa'
            category TEXT NOT NULL,
            account_id INTEGER,
            status TEXT DEFAULT 'pago',
            date TEXT NOT NULL,
            FOREIGN KEY (account_id) REFERENCES accounts (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Schemas Pydantic
class AccountSchema(BaseModel):
    name: str
    type: str # Ex: Conta Corrente, Cartão de Crédito, Carteira
    balance: float

class TransactionSchema(BaseModel):
    description: str
    amount: float
    type: str # 'receita' ou 'despesa'
    category: str
    account_id: int
    status: str # 'pago' ou 'pendente'
    date: str # YYYY-MM-DD

@app.post("/accounts/")
def create_account(account: AccountSchema):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (name, type, balance) VALUES (?, ?, ?)",
                   (account.name, account.type, account.balance))
    conn.commit()
    conn.close()
    return {"status": "Conta criada com sucesso"}

@app.get("/accounts/")
def list_accounts():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "type": r[2], "balance": r[3]} for r in rows]

@app.post("/transactions/")
def create_transaction(t: TransactionSchema):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    
    # Inserir transação
    cursor.execute('''
        INSERT INTO transactions (description, amount, type, category, account_id, status, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (t.description, t.amount, t.type, t.category, t.account_id, t.status, t.date))
    
    # Atualizar saldo da conta
    if t.status == 'pago':
        adjustment = t.amount if t.type == 'receita' else -t.amount
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (adjustment, t.account_id))
        
    conn.commit()
    conn.close()
    return {"status": "Transação registrada com sucesso"}

@app.get("/transactions/")
def list_transactions():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.id, t.description, t.amount, t.type, t.category, a.name, t.status, t.date 
        FROM transactions t
        LEFT JOIN accounts a ON t.account_id = a.id
        ORDER BY t.date DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [{
        "id": r[0], "description": r[1], "amount": r[2], "type": r[3],
        "category": r[4], "account": r[5], "status": r[6], "date": r[7]
    } for r in rows]