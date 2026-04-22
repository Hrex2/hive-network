import streamlit as st

def init_metrics():
    if "metrics" not in st.session_state:
        st.session_state.metrics = {
            "steps": [],
            "leaders": [],
            "failures": 0
        }

def update_metrics(step, mother_id):
    st.session_state.metrics["steps"].append(step)
    st.session_state.metrics["leaders"].append(mother_id)

def record_failure():
    st.session_state.metrics["failures"] += 1