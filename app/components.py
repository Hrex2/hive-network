import streamlit as st

def show_leader(mother):
    st.subheader("👑 Leader Info")
    st.success(f"Current Mother: Node {mother.id}")


def show_node_roles(nodes):
    st.subheader("📊 Node Roles")

    # Group nodes by role
    roles = {
        "mother": [],
        "eldest_mother": [],
        "daughter": [],
        "worker": []
    }

    for node in nodes.values():
        roles[node.role].append(node.id)

    # Display nicely
    if roles["mother"]:
        st.markdown("### 👑 Mother")
        st.write(", ".join(map(str, roles["mother"])))

    if roles["eldest_mother"]:
        st.markdown("### 🟣 Eldest Mother")
        st.write(", ".join(map(str, roles["eldest_mother"])))

    if roles["daughter"]:
        st.markdown("### 🔵 Daughters")
        st.write(", ".join(map(str, roles["daughter"])))

    if roles["worker"]:
        st.markdown("### 🟢 Workers")
        st.write(", ".join(map(str, roles["worker"])))