import streamlit as st
from data_connection import Connector
import os
from dotenv import load_dotenv

load_dotenv()

month_select = ["All", "January", "February", "March", "April", "May", "June", "July", "August", "September",
                "October", "November", "December"]

if 'month_select' not in st.session_state or st.session_state.month_select is None:
    st.session_state['month_select'] = 'All'

conn = Connector(os.environ.get("host"), os.environ.get("user"), os.environ.get("password"))

if st.session_state.month_select == "All":
    incomes = conn.get_incomes()
    expenses = conn.get_expenses()
else:
    incomes = conn.get_incomes_filtered(month_select.index(st.session_state.month_select))
    expenses = conn.get_expenses_filtered(month_select.index(st.session_state.month_select))

incomes_total = incomes['value'].sum()
expenses_total = expenses['value'].sum()

st.title("Budget")
col_a, col_b = st.columns(2)
with col_a:
    st.metric("Budget this month", f"{incomes_total - expenses_total:.2f}$")

with col_b:
    st.selectbox("Month", month_select, key='month_select')

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Income")
    with st.expander("Add income"):
        form = st.form(f"form_income")
        account = form.selectbox("Account", [""] + conn.get_accounts()["name"].tolist())
        inc_type = form.selectbox("Type", [""] + conn.get_income_types()["name"].tolist())
        name = form.text_input("Name")
        date = form.date_input("Date")
        current_value = form.number_input("Value", min_value=0.0, value=0.0, step=0.001)
        form.submitted = form.form_submit_button("Add")

        if form.submitted:
            conn.add_income(account, inc_type, name, date, current_value)
            st.experimental_rerun()

    st.dataframe(incomes)

    st.divider()

    st.write(f"**Total income: {incomes_total:.2f}**")

with col2:
    st.subheader("Expenses")
    with st.expander("Add expense"):
        with st.form(f"form_expense"):
            account = st.selectbox("Account", [""] + conn.get_accounts()["name"].tolist())
            name = st.text_input("Name")
            date = st.date_input("Date")
            current_value = st.number_input("Value", min_value=0.0, value=0.0, step=0.001)
            st.write("Tags")
            tags = conn.get_expense_tags()["name"].tolist()
            chk_boxes = []
            col_tag1, col_tag2 = st.columns(2)
            with col_tag1:
                for t in tags[:int(len(tags)/2)]:
                    chk_boxes.append([st.checkbox(t), t])
            with col_tag2:
                for t in tags[int(len(tags)/2):]:
                    chk_boxes.append([st.checkbox(t), t])

            submitted = st.form_submit_button("Add")

            if submitted:
                id = conn.add_expense(name, account, date, current_value)

                for c in chk_boxes:
                    if c[0]:
                        conn.add_expense_tag_link(id, c[1])
                st.experimental_rerun()

    st.dataframe(expenses)

    st.divider()

    st.write(f"**Total expenses: {expenses_total:.2f}**")