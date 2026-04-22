import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

def draw_network(G, nodes):
    plt.clf()

    colors = []
    sizes = []

    for i in G.nodes():
        node = nodes[i]

        if not node.alive:
            colors.append("black")   # dead node
            sizes.append(200)

        elif node.role == "mother":
            colors.append("gold")    # main leader 👑
            sizes.append(800)

        elif node.role == "eldest_mother":
            colors.append("purple")  # backup leader 🔮
            sizes.append(650)

        elif node.role == "daughter":
            colors.append("blue")    # sub-leader
            sizes.append(400)

        else:
            colors.append("green")   # worker
            sizes.append(300)

    # Slight dynamic movement (animation feel)
    pos = nx.spring_layout(G, seed=42)

    nx.draw(
        G,
        pos,
        node_color=colors,
        node_size=sizes,
        with_labels=True,
        edge_color="gray",
        width=1.5,
        font_weight="bold"
    )

    plt.title("Hive Network (Live System)")

    st.pyplot(plt.gcf())