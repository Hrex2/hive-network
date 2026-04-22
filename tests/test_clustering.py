from core.node import Node
from core.clustering import assign_daughters

def test_clustering():
    nodes = {i: Node(i) for i in range(5)}

    mother = nodes[0]
    mother.role = "mother"

    daughters = assign_daughters(nodes, mother, k=2)

    assert len(daughters) == 2
    for d in daughters:
        assert d.role == "daughter"

    print("✅ Clustering Test Passed")