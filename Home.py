import streamlit as st
import pandas as pd
import numpy as np
from data_connection import Connector
import util
import datetime
import asyncio
import time
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

timeframe_sb = None

conn = Connector(os.environ.get("host"), os.environ.get("user"), os.environ.get("password"))

investments = conn.get_investments()
debts = conn.get_debts()
incomes = conn.get_incomes()
expenses = conn.get_expenses()
net_worth = util.calculate_networth(investments, debts, incomes, expenses)

conn.add_net_worth(datetime.date.today(), net_worth)
net_worth_history = conn.get_net_worth()
net_worth_history["value"] = net_worth_history["value"].astype(float)
l = net_worth_history['value'].tolist()

col1, col2 = st.columns(2)
with col1:
    try:
        dlt = f"{(l[-1] - l[timeframe[st.session_state.timeframe_select]]) / l[timeframe[st.session_state.timeframe_select]] * 100}%"
    except:
        dlt = "not enough data"
    st.metric("Net worth", f"{net_worth:.2f}$", delta=dlt)

with col2:
    timeframe_sb = st.selectbox("Timeframe", timeframe.keys(),
                                index=list(timeframe.keys()).index(st.session_state.timeframe_select),
                                key='timeframe_select')

st.title("Net worth manager")

st.subheader("Investments")
investments

st.subheader("Debts")
debts

st.subheader("Net worth")
st.line_chart(net_worth_history, x="date", y="value")