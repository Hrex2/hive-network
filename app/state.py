from core.network import create_network
from core.election import elect_mother
from core.clustering import assign_daughters, assign_workers

def init_state(num_nodes=10, num_daughters=3):
    G, nodes = create_network(num_nodes)

    mother = elect_mother(nodes)
    daughters = assign_daughters(nodes, mother, num_daughters)
    assign_workers(nodes, daughters)

    return G, nodes, mother