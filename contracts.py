# --- TECHNO-LEGAL PROTOCOL ---
# CONTRACT_ID: TL-SETTLE-001
# STATUS: ACTIVE | SELF_EXECUTING: TRUE

import datetime
from zoneinfo import ZoneInfo

class SmartContract:
    def __init__(self):
        self.harare_tz = ZoneInfo("Africa/Harare")

    def validate_agreement(self, amount: float, condition_met: bool):
        """
        A self-executing logic gate.
        If the condition is True, the 'contract' signs the execution.
        """
        timestamp = datetime.datetime.now(self.harare_tz).strftime('%Y-%m-%d %H:%M:%S')
        
        if amount <= 0:
            return {"status": "VOID", "msg": "VALUE_ERROR: Amount must be > 0"}
        
        if condition_met:
            return {
                "status": "EXECUTED",
                "timestamp": timestamp,
                "msg": f"CONTRACT_FULFILLED: Settlement of {amount} units authorized.",
                "hash": hash(f"{timestamp}{amount}AUTHORIZED") # Primitive signature
            }
        else:
            return {"status": "PENDING", "msg": "CONDITION_NOT_MET: Awaiting verification."}
