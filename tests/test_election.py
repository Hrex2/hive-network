from core.node import Node
from core.election import elect_mother

def test_election():
    nodes = {
        0: Node(0),
        1: Node(1),
        2: Node(2)
    }

    # Force deterministic values
    nodes[0].cpu = 50
    nodes[0].stability = 0.1
    nodes[0].latency = 40

    nodes[1].cpu = 90  # BEST
    nodes[1].stability = 0.9
    nodes[1].latency = 5

    nodes[2].cpu = 60
    nodes[2].stability = 0.2
    nodes[2].latency = 30

    mother = elect_mother(nodes)

    assert mother.id == 1
    print("✅ Election Test Passed")