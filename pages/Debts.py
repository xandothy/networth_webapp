import streamlit as st
from data_connection import Connector
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

if 'timeframe_select' not in st.session_state or st.session_state.timeframe_select is None:
    st.session_state['timeframe_select'] = 'Day'


timeframe = {
    "Day": -2,
    "Month": -30,
    "Year": -365,
    "5 Years": -1825,
    "10 Years": -3650,
    "25 Years": -9125,
    "All": 0
}

conn = Connector(os.environ.get("host"), os.environ.get("user"), os.environ.get("password"))

timeframe_sb = None

col1, col2 = st.columns(2)
with col1:
    st.title("Debts")

with col2:
    timeframe_sb = st.selectbox("Timeframe", timeframe.keys(),
                                index=list(timeframe.keys()).index(st.session_state.timeframe_select),
                                key='timeframe_select')

st.divider()


def add_debt_data(debt):
    history = conn.get_debt_history(debt["ID"])
    l = history['value'].tolist()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(debt["name"])
    with col2:
        try:
            dlt = f"{(l[-1] - l[timeframe[st.session_state.timeframe_select]]) / l[timeframe[st.session_state.timeframe_select]] * 100}%"
        except:
            dlt = "not enough data"
        st.metric("Total value", f"{debt['amount'] * -debt['value']:.2f}$", delta=dlt)

    df = conn.get_debt_history(debt['ID'])
    df["value"] = df["value"].astype(float)
    df["amount"] = df["amount"].astype(float)
    st.line_chart(df, x="date", y=["amount", "value"])

    with st.expander("Update position"):
        form = st.form(f"form_{debt['name']}")
        current_amount = form.number_input("Amount", min_value=0.0, value=float(debt["amount"]), step=0.001)
        current_value = form.number_input("Value", min_value=0.0, value=float(debt["value"]), step=0.001)
        form.submitted = form.form_submit_button("Update")

        if form.submitted:
            conn.add_debt_history(debt["ID"], datetime.date.today(), current_amount, current_value)
            st.experimental_rerun()

    st.divider()


debts = conn.get_debts()

for index, row in debts.iterrows():
    add_debt_data(row)
    
with st.sidebar.form("Add debt"):
    st.title("Add debt")
    debt_name = st.text_input("Name of the debt")
    debt_account = st.selectbox("Account", conn.get_accounts()["name"])
    debt_type = st.selectbox("Type", conn.get_debt_types()["name"])
    date = st.date_input("Date")
    amount = st.number_input("Amount", min_value=0.0, value=0.0, step=0.001)
    value = st.number_input("Value", min_value=0.0, value=0.0, step=0.001)
    submitted = st.form_submit_button("Add")
    
    if submitted:
        id = conn.add_debt(debt_name, debt_account, debt_type)
        conn.add_debt_history(id, date, amount, value)
        st.experimental_rerun()
