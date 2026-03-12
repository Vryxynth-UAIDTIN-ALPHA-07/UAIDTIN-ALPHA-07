# --- UNIVERSAL LOGIC SCHEMA ---
# VERSION: 1.0.0 | PROTOCOL: JSON_STRUCT_01
# PURPOSE: DEFINING THE 'THOUGHT' ARCHITECTURE

from pydantic import BaseModel
from typing import Dict, Any, Optional

class UniversalThought(BaseModel):
    # 1. Identity
    node_id: str = "UAIDTIN-ALPHA-07"
    
    # 2. Intent (The 'Verb')
    action_type: str  # e.g., "SETTLEMENT", "MARKET_SCOUT", "SYSTEM_SYNC"
    
    # 3. Context (The 'Nouns')
    payload: Dict[str, Any] # e.g., {"asset": "Gold", "value": 2300}
    
    # 4. Constraints (The 'Law')
    metadata: Optional[Dict[str, Any]] = {"priority": "HIGH", "version": "1.0"}

    def summarize(self):
        return f"NODE {self.node_id} IS EXECUTING {self.action_type} ON {self.payload.get('asset', 'DATA')}"
