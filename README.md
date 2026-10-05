# 💼 Organizze Clone — Gerenciador Financeiro Pessoal

Um sistema completo de gestão financeira pessoal inspirado no **Organizze**, desenvolvido com **FastAPI** no backend (API RESTful + SQLite) e **Streamlit** no frontend para visualização e controle de contas, receitas e despesas.

---

## 🚀 Funcionalidades

- **Visão Geral / Dashboard:** Resumo do saldo total acumulado em contas, métricas de receitas e despesas do mês e tabela com as transações mais recentes.
- **Lançamentos:** Cadastro de receitas e despesas com categoria, conta/cartão associado, data, descrição e status (pago ou pendente).
- **Contas & Cartões:** Gerenciamento de saldo e contas (Conta Corrente, Cartão de Crédito, Investimentos, Dinheiro).
- **Relatórios:** Gráficos visuais por categoria de despesa para análise detalhada do orçamento.
- **Persistência de Dados:** Banco de dados relacional SQLite configurado automaticamente.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://docs.pydantic.dev/), [SQLite3](https://docs.python.org/3/library/sqlite3.html)
- **Frontend:** [Streamlit](https://streamlit.io/), [Pandas](https://pandas.pydata.org/)
- **Servidor Web:** [Uvicorn](https://www.uvicorn.org/)

---

## 📦 Estrutura do Projeto

```text
.
├── app.py          # Servidor Backend (FastAPI + SQLite)
├── frontend.py     # Interface do Usuário (Streamlit)
├── finance.db      # Banco de dados SQLite (gerado automaticamente)
└── README.md       # Documentação do projeto