from config import W_CPU, W_STABILITY, W_LATENCY

from utils.logger import log


def calculate_score(node):
    return (W_CPU * node.cpu) + (W_STABILITY * node.stability) - (W_LATENCY * node.latency)

def elect_mother(nodes):
    alive_nodes = [n for n in nodes.values() if n.alive]
    mother = max(alive_nodes, key=calculate_score)

    for n in nodes.values():
        n.role = "worker"

    mother.role = "mother"

    log(f"New Mother Elected → Node {mother.id}", "SUCCESS")
    return mother