import streamlit as st
import sys
import os
import time

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Auto refresh (heartbeat loop)
from streamlit_autorefresh import st_autorefresh

# App modules
from app.state import init_state
from app.components import show_leader, show_node_roles
from app.logs_view import show_logs
from app.metrics import init_metrics, update_metrics, record_failure
from app.metrics_view import show_metrics

# Core logic
from core.election import elect_mother
from core.clustering import assign_daughters, assign_workers
from core.recovery import recover, awaken_node

# Visualization
from visualization.plot import draw_network
from visualization.hive_plot import draw_hive_network   # ✅ NEW

st.set_page_config(layout="wide")

# 🔁 Auto refresh every 2 seconds
st_autorefresh(interval=2000, key="heartbeat")

st.title("🐝 Hive Leader Simulation")

# ---------------- INIT ---------------- #
if "nodes" not in st.session_state:
    G, nodes, mother = init_state()

    st.session_state.G = G
    st.session_state.nodes = nodes
    st.session_state.mother = mother

# Track MULTIPLE failed nodes
if "failed_nodes" not in st.session_state:
    st.session_state.failed_nodes = []

# Heartbeat timer
if "last_heartbeat" not in st.session_state:
    st.session_state.last_heartbeat = time.time()

# Metrics init
init_metrics()

# Step counter
if "step" not in st.session_state:
    st.session_state.step = 0

st.session_state.step += 1

# ---------------- HEARTBEAT ---------------- #
current_time = time.time()

if not st.session_state.mother.alive:
    if current_time - st.session_state.last_heartbeat > 2:
        st.warning("⚠️ Heartbeat lost! Triggering re-election...")

        st.session_state.mother = recover(st.session_state.nodes)

        daughters = assign_daughters(
            st.session_state.nodes,
            st.session_state.mother,
            3
        )
        assign_workers(st.session_state.nodes, daughters)

        update_metrics(st.session_state.step, st.session_state.mother.id)

        st.session_state.last_heartbeat = current_time

# ---------------- BUTTONS ---------------- #
col1, col2, col3 = st.columns(3)

# 💥 FAIL
if col1.button("💥 Fail Mother"):
    st.session_state.failed_nodes.append(st.session_state.mother)

    st.session_state.mother.alive = False
    st.session_state.last_heartbeat = time.time()

    record_failure()

# 🔄 RE-ELECTION
if col2.button("🔄 Re-Election"):
    st.session_state.mother = elect_mother(st.session_state.nodes)

    daughters = assign_daughters(
        st.session_state.nodes,
        st.session_state.mother,
        3
    )
    assign_workers(st.session_state.nodes, daughters)

    update_metrics(st.session_state.step, st.session_state.mother.id)

# 🔁 AWAKEN
if col3.button("🔁 Awaken Mother"):
    if st.session_state.failed_nodes:

        node_to_awake = st.session_state.failed_nodes.pop(0)

        awaken_node(
            node_to_awake,
            st.session_state.mother
        )

        st.success(
            f"Node {node_to_awake.id} is now Eldest-Mother"
        )

    else:
        st.info("No failed nodes available")

# ---------------- LAYOUT ---------------- #
left, right = st.columns([2, 1])

with left:
    st.subheader("🌐 Single Hive View")
    draw_network(st.session_state.G, st.session_state.nodes)

    # ---------------- MULTI-HIVE VIEW ---------------- #
    st.subheader("🌐 Multi-Hive Communication (Sis–Sis Model)")

    nodes_list = list(st.session_state.nodes.values())

    if len(nodes_list) >= 10:

        # Hive A (current)
        hive1 = {
            "id": "Hive A",
            "mother": st.session_state.mother,
            "daughters": nodes_list[1:3],
            "workers": nodes_list[3:6]
        }

        # Hive B (simulated)
        other_mother = nodes_list[6]  # DO NOT change role globally

        hive2 = {
            "id": "Hive B",
            "mother": other_mother,
            "daughters": nodes_list[7:9],
            "workers": nodes_list[9:]
        }

        draw_hive_network([hive1, hive2])

    else:
        st.info("Need at least 10 nodes for multi-hive view")

with right:
    show_leader(st.session_state.mother)

    # Heartbeat status
    if st.session_state.mother.alive:
        st.success("❤️ Heartbeat Active")
    else:
        st.error("💔 Heartbeat Lost")

    show_node_roles(st.session_state.nodes)

    # Show failed nodes queue
    if st.session_state.failed_nodes:
        st.write(
            "💀 Failed Nodes:",
            [n.id for n in st.session_state.failed_nodes]
        )

# ---------------- LOGS ---------------- #
show_logs()

# ---------------- METRICS ---------------- #
show_metrics()