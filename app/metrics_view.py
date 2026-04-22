import streamlit as st
import matplotlib.pyplot as plt

def show_metrics():
    st.subheader("📊 System Metrics")

    if "metrics" not in st.session_state:
        st.info("No metrics available yet")
        return

    metrics = st.session_state.metrics

    if not metrics["steps"]:
        st.info("No data to display")
        return

    # 📈 Leader changes graph
    plt.figure()

    plt.plot(
        metrics["steps"],
        metrics["leaders"],
        marker='o'
    )

    plt.title("Leader Changes Over Time")
    plt.xlabel("Step")
    plt.ylabel("Mother Node ID")

    st.pyplot(plt)

    # 💥 Failure count
    st.write(f"💥 Total Failures: {metrics['failures']}")