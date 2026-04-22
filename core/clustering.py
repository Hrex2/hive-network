from core.election import calculate_score
from utils.logger import log
def assign_daughters(nodes, mother, k):
    others = [n for n in nodes.values() if n.id != mother.id and n.alive]
    sorted_nodes = sorted(others, key=calculate_score, reverse=True)

    daughters = sorted_nodes[:k]

    for d in daughters:
        d.role = "daughter"
    log(f"Assigned {len(daughters)} Daughters under Mother {mother.id}", "INFO")
    return daughters


def assign_workers(nodes, daughters):
    for node in nodes.values():
        if node.role == "worker" and node.alive:
            assigned = daughters[node.id % len(daughters)]
            node.cluster = assigned.id