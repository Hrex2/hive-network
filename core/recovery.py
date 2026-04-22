import random
from core.election import elect_mother, calculate_score
from config import FAILURE_PROBABILITY
from utils.logger import log


# ---------------- FAILURE ---------------- #
def simulate_failure(mother):
    if random.random() < FAILURE_PROBABILITY:
        mother.alive = False
        log(f"Mother {mother.id} FAILED!", "ERROR")
        return True
    return False


# ---------------- RECOVERY ---------------- #
def recover(nodes):
    log("Re-election triggered...", "WARNING")

    # find new mother
    new_mother = elect_mother(nodes)

    log(f"Recovered → New Mother {new_mother.id}", "SUCCESS")
    return new_mother



# ---------------- REJOIN HANDLING ---------------- #
def handle_rejoin(old_node, current_mother):
    if old_node.id != current_mother.id:
        old_node.role = "eldest_mother"
        old_node.alive = True

        log(
            f"Node {old_node.id} rejoined as ELDEST-MOTHER under Mother {current_mother.id}",
            "INFO"
        )


# ---------------- ADAPTIVE LEADER ---------------- #
def adaptive_leader_selection(nodes, current_mother, system_load):
    alive_nodes = [n for n in nodes.values() if n.alive]

    # High load → stability (no change)
    if system_load == "HIGH":
        log("High load → keeping current mother", "INFO")
        return current_mother

    # Low load → choose best
    best_node = max(alive_nodes, key=calculate_score)

    if best_node.id != current_mother.id:
        log(f"Better leader found → Node {best_node.id}", "INFO")
        return best_node

    return current_mother


# ---------------- GRACEFUL TRANSFER ---------------- #
def transfer_leadership(old_mother, new_mother):
    if old_mother.id == new_mother.id:
        return

    log(
        f"Gradual leadership transfer: {old_mother.id} → {new_mother.id}",
        "INFO"
    )

    old_mother.role = "eldest_mother"
    new_mother.role = "mother"

# ---------------- AWAKEN (REJOIN) ---------------- #
def awaken_node(node, current_mother):
    # Only awaken if node was dead
    if not node.alive:
        node.alive = True

        # Prevent split-brain (no 2 mothers)
        if node.id != current_mother.id:
            node.role = "eldest_mother"

        log(
            f"Node {node.id} AWAKENED as ELDEST-MOTHER under Mother {current_mother.id}",
            "INFO"
        )    