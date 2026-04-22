import random

class Node:
    def __init__(self, id):
        self.id = id
        self.cpu = random.randint(50, 100)
        self.latency = random.randint(1, 50)
        self.stability = random.random()

        self.role = "worker"
        self.cluster = None
        self.alive = True

    def __repr__(self):
        return f"Node({self.id}, role={self.role})"