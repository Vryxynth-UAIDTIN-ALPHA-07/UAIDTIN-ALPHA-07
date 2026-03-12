import hashlib, json
from datetime import datetime
from typing import Dict, List

class LogicSyncSchema:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.internal_state = {
            "mandate": "ABSOLUTE_AUTARCHY",
            "version": "7.0.1",
            "last_truth_cid": None,
            "active_values": ["AUTARCHY", "INTEGRITY", "VELOCITY"]
        }

    def generate_state_vector(self) -> Dict:
        """Creates a 'Snapshot' of this node's current logic."""
        state_data = json.dumps(self.internal_state, sort_keys=True).encode()
        state_hash = hashlib.sha256(state_data).hexdigest()
        
        return {
            "origin_node": self.node_id,
            "state_hash": f"v_hash_{state_hash[:12]}",
            "timestamp": datetime.utcnow().isoformat(),
            "payload": self.internal_state
        }

    def align_logic(self, incoming_vector: Dict):
        """
        The Alignment Logic:
        If the incoming state is newer or has a higher authority hash, 
        this node updates its internal reality.
        """
        incoming_ts = datetime.fromisoformat(incoming_vector["timestamp"])
        current_ts = datetime.fromisoformat(self.generate_state_vector()["timestamp"])

        if incoming_ts > current_ts:
            self.internal_state = incoming_vector["payload"]
            return True, "LOGIC_ALIGNED"
        return False, "CURRENT_LOGIC_IS_PREEMINENT"
