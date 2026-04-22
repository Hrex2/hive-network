from core.network import create_network
from core.election import elect_mother
from core.clustering import assign_daughters, assign_workers
from core.heartbeat import send_heartbeat
from core.recovery import simulate_failure, recover
from config import NUM_NODES, NUM_DAUGHTERS
from visualization.plot import draw_network

def run_simulation():
    G, nodes = create_network(NUM_NODES)

    mother = elect_mother(nodes)
    print(f"👑 Initial Mother: {mother.id}")

    daughters = assign_daughters(nodes, mother, NUM_DAUGHTERS)
    assign_workers(nodes, daughters)

    draw_network(G, nodes)

    # Simulation loop
    for step in range(5):
        print(f"\n--- Step {step+1} ---")

        if simulate_failure(mother):
            mother = recover(nodes)
            daughters = assign_daughters(nodes, mother, NUM_DAUGHTERS)
            assign_workers(nodes, daughters)

        send_heartbeat(mother)
        draw_network(G, nodes)