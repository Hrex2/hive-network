from core.network import create_network
from core.election import elect_mother
from core.recovery import recover

def test_failure():
    G, nodes = create_network(5)

    mother = elect_mother(nodes)
    mother.alive = False

    new_mother = recover(nodes)

    assert new_mother.alive == True
    assert new_mother.role == "mother"

    print("✅ Failure Recovery Test Passed")