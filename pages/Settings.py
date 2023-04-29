import streamlit as st
from data_connection import Connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = Connector(os.environ.get("host"), os.environ.get("user"), os.environ.get("password"))

st.title("Settings")

# owners
st.subheader("Owners")
st.dataframe(conn.get_owners(), use_container_width=True)

with st.expander("Add owner"):
    form = st.form(f"form_owners")
    first_name = form.text_input("First name")
    last_name = form.text_input("Last name")
    form.submitted = form.form_submit_button("Add")

    if form.submitted:
        conn.add_owner(first_name, last_name)
        st.experimental_rerun()

st.divider()

# account content
st.subheader("Account contents")
st.dataframe(conn.get_account_contents(), use_container_width=True)

with st.expander("Add account content"):
    form = st.form(f"form_account_contents")
    name = form.text_input("Name")
    description = form.text_input("Description")
    form.submitted = form.form_submit_button("Add")

    if form.submitted:
        conn.add_account_content(name, description)
        st.experimental_rerun()

st.divider()

# account types
st.subheader("Account types")
st.dataframe(conn.get_account_types(), use_container_width=True)

with st.expander("Add account type"):
    form = st.form(f"form_account_types")
    name = form.text_input("Name")
    description = form.text_input("Description")
    form.submitted = form.form_submit_button("Add")

    if form.submitted:
        conn.add_account_type(name, description)
        st.experimental_rerun()

st.divider()

# accounts
st.subheader("Accounts")
st.dataframe(conn.get_accounts(), use_container_width=True)

with st.expander("Add account"):
    form = st.form(f"form_accounts")
    name = form.text_input("Name")
    acc_type = form.selectbox("Account type", [""] + conn.get_account_types()["name"].tolist())
    acc_content = form.selectbox("Account content", [""] + conn.get_account_contents()["name"].tolist())
    owner1 = form.selectbox("First owner", [""] + conn.get_owners()["first_name"].tolist())
    owner2 = form.selectbox("Second owner", [""] + conn.get_owners()["first_name"].tolist())
    form.submitted = form.form_submit_button("Add")

    if form.submitted:
        if owner1 == owner2:
            st.error('First and second owners cannot be the same person!', icon="🚨")
        elif acc_type == "":
            st.error('Account type cannot be empty!', icon="🚨")
        elif acc_content == "":
            st.error('Account content cannot be empty!', icon="🚨")
        elif owner1 == "":
            st.error('First owner cannot be empty!', icon="🚨")
        elif name == "":
            st.error('Account name cannot be empty!', icon="🚨")
        else:
            conn.add_account(name, acc_type, acc_content, owner1, owner2)
            st.experimental_rerun()

st.divider()

# debt types
st.subheader("Debt types")
st.dataframe(conn.get_debt_types(), use_container_width=True)

with st.expander("Add debt type"):
    form = st.form(f"form_debt_types")
    name = form.text_input("Name")
    description = form.text_input("Description")
    form.submitted = form.form_submit_button("Add")

    if form.submitted:
        conn.add_debt_type(name, description)
        st.experimental_rerun()

# investment types
st.subheader("Investment types")
st.dataframe(conn.get_investment_types(), use_container_width=True)

with st.expander("Add investment type"):
    form = st.form(f"form_investment_types")
    name = form.text_input("Name")
    description = form.text_input("Description")
    form.submitted = form.form_submit_button("Add")

    if form.submitted:
        conn.add_investment_type(name, description)
        st.experimental_rerun()

# income types
st.subheader("Income types")
st.dataframe(conn.get_income_types(), use_container_width=True)

with st.expander("Add income type"):
    form = st.form(f"form_income_types")
    name = form.text_input("Name")
    description = form.text_input("Description")
    form.submitted = form.form_submit_button("Add")

    if form.submitted:
        conn.add_income_type(name, description)
        st.experimental_rerun()

# expense tags
st.subheader("Expense tags")
st.dataframe(conn.get_expense_tags(), use_container_width=True)

with st.expander("Add expense tag"):
    form = st.form(f"form_expense_tags")
    name = form.text_input("Name")
    description = form.text_input("Description")
    form.submitted = form.form_submit_button("Add")

    if form.submitted:
        conn.add_expense_tag(name, description)
        st.experimental_rerun()