import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

def draw_hive_network(hives):
    """
    hives = [
        {
            "id": "Hive A",
            "mother": node,
            "daughters": [nodes],
            "workers": [nodes]
        },
        ...
    ]
    """

    G = nx.Graph()

    pos = {}
    colors = []
    sizes = []

    x_offset = 0

    mother_nodes = []

    for hive in hives:
        hive_id = hive["id"]

        mother = hive["mother"]
        daughters = hive["daughters"]
        workers = hive["workers"]

        # Position mother
        G.add_node(f"M_{mother.id}")
        pos[f"M_{mother.id}"] = (x_offset, 2)
        colors.append("gold")
        sizes.append(800)

        mother_nodes.append(f"M_{mother.id}")

        # Daughters
        for i, d in enumerate(daughters):
            node_name = f"D_{d.id}"
            G.add_node(node_name)
            pos[node_name] = (x_offset - 1 + i, 1)

            G.add_edge(f"M_{mother.id}", node_name)

            colors.append("blue")
            sizes.append(400)

        # Workers (granddaughters)
        for i, w in enumerate(workers):
            node_name = f"W_{w.id}"
            G.add_node(node_name)
            pos[node_name] = (x_offset - 1 + i, 0)

            # Connect to a daughter (simple mapping)
            if daughters:
                G.add_edge(f"D_{daughters[0].id}", node_name)

            colors.append("green")
            sizes.append(300)

        x_offset += 4  # move next hive

    # 🔗 Sister-Mother connections (inter-hive)
    for i in range(len(mother_nodes)):
        for j in range(i + 1, len(mother_nodes)):
            G.add_edge(mother_nodes[i], mother_nodes[j])

    # Draw
    plt.figure(figsize=(10, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=colors,
        node_size=sizes,
        edge_color="gray"
    )

    plt.title("🐝 Multi-Hive Communication (Sis-Sis + Hierarchy)")

    st.pyplot(plt)