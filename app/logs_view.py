import streamlit as st
import os

def show_logs():
    st.subheader("📜 System Logs")

    log_file = "results/logs/simulation.log"

    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines[-10:]:
            st.text(line.strip())
    else:
        st.info("No logs available yet")