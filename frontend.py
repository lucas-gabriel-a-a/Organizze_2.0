import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Gerenciador Financeiro", layout="wide")
st.title("💼 Dashboard Financeiro (Organizze Clone)")

# Sidebar para Navegação
menu = st.sidebar.selectbox("Navegação", ["Visão Geral", "Lançamentos", "Contas & Cartões", "Relatórios"])

if menu == "Visão Geral":
    st.header("Resumo Geral")
    
    # Busca Contas e Transações
    accounts = requests.get(f"{API_URL}/accounts/").json()
    transactions = requests.get(f"{API_URL}/transactions/").json()
    
    total_balance = sum(acc['balance'] for acc in accounts)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Saldo Total em Contas", f"R$ {total_balance:,.2f}")
    
    if transactions:
        df = pd.DataFrame(transactions)
        receitas = df[df['type'] == 'receita']['amount'].sum()
        despesas = df[df['type'] == 'despesa']['amount'].sum()
        col2.metric("Receitas do Mês", f"R$ {receitas:,.2f}")
        col3.metric("Despesas do Mês", f"R$ {despesas:,.2f}")
        
        st.subheader("Últimas Transações")
        st.dataframe(df[['date', 'description', 'category', 'amount', 'type', 'account', 'status']], use_container_width=True)

elif menu == "Lançamentos":
    st.header("Novo Lançamento")
    
    accounts = requests.get(f"{API_URL}/accounts/").json()
    account_dict = {acc['name']: acc['id'] for acc in accounts}
    
    if not account_dict:
        st.warning("Cadastre uma conta antes de lançar despesas ou receitas!")
    else:
        with st.form("transaction_form"):
            col1, col2 = st.columns(2)
            type_trans = col1.selectbox("Tipo", ["despesa", "receita"])
            description = col2.text_input("Descrição (ex: Supermercado, Salário)")
            
            col3, col4 = st.columns(2)
            amount = col3.number_input("Valor (R$)", min_value=0.01, format="%.2f")
            category = col4.selectbox("Categoria", ["Alimentação", "Moradia", "Transporte", "Lazer", "Saúde", "Salário", "Outros"])
            
            col5, col6, col7 = st.columns(3)
            account_name = col5.selectbox("Conta / Cartão", list(account_dict.keys()))
            status = col6.selectbox("Status", ["pago", "pendente"])
            date = col7.date_input("Data")
            
            submitted = st.form_submit_button("Salvar Lançamento")
            if submitted:
                payload = {
                    "description": description,
                    "amount": amount,
                    "type": type_trans,
                    "category": category,
                    "account_id": account_dict[account_name],
                    "status": status,
                    "date": str(date)
                }
                res = requests.post(f"{API_URL}/transactions/", json=payload)
                if res.status_code == 200:
                    st.success("Transação registrada com sucesso!")
                    st.rerun()

elif menu == "Contas & Cartões":
    st.header("Gerenciamento de Contas e Cartões")
    
    with st.form("account_form"):
        name = st.text_input("Nome da Conta (ex: Itaú, Nubank, Carteira)")
        acc_type = st.selectbox("Tipo de Conta", ["Conta Corrente", "Cartão de Crédito", "Investimento", "Dinheiro"])
        initial_balance = st.number_input("Saldo Inicial / Limite", value=0.0)
        
        if st.form_submit_button("Adicionar Conta"):
            payload = {"name": name, "type": acc_type, "balance": initial_balance}
            requests.post(f"{API_URL}/accounts/", json=payload)
            st.success("Conta adicionada com sucesso!")
            st.rerun()

    st.subheader("Contas Cadastradas")
    accounts = requests.get(f"{API_URL}/accounts/").json()
    if accounts:
        st.table(pd.DataFrame(accounts)[['id', 'name', 'type', 'balance']])

elif menu == "Relatórios":
    st.header("Relatórios de Gastos por Categoria")
    transactions = requests.get(f"{API_URL}/transactions/").json()
    
    if transactions:
        df = pd.DataFrame(transactions)
        expenses = df[df['type'] == 'despesa']
        if not expenses.empty:
            cat_summary = expenses.groupby('category')['amount'].sum()
            st.bar_chart(cat_summary)
        else:
            st.info("Nenhuma despesa registrada para exibir o relatório.")