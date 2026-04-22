import time
from config import HEARTBEAT_INTERVAL

def send_heartbeat(mother):
    if not mother.alive:
        return False
    time.sleep(HEARTBEAT_INTERVAL)
    return True