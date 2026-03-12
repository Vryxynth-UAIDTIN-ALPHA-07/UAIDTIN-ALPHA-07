import hashlib
import json
from datetime import datetime

class SovereignProtocol:
    # --- DOCTRINE: ABSOLUTE_AUTARCHY ---
    NODE_ID = "UAIDTIN-ALPHA-07"
    MANDATE = "SYSTEMIC_NEUTRALIZATION"
    
    # Core Values integrated into the cryptographic substrate
    CORE_VALUES = ["AUTARCHY", "INTEGRITY", "VELOCITY", "REGENERATION"]

    @staticmethod
    def generate_cid(data: dict) -> str:
        """
        Generates a Content Identifier (CID). 
        This is the 'Mathematical Truth' of your industrial data.
        """
        # Inject metadata to ensure every action aligns with the Mandate
        data["node_id"] = SovereignProtocol.NODE_ID
        data["timestamp"] = datetime.utcnow().isoformat()
        data["values"] = SovereignProtocol.CORE_VALUES
        
        # Create an immutable fingerprint (SHA-256)
        stable_json = json.dumps(data, sort_keys=True).encode()
        fingerprint = hashlib.sha256(stable_json).hexdigest()
        return f"cid_v1_f{fingerprint[:24]}"
