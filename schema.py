from pydantic import BaseModel
from typing import Dict, Any

class UniversalThought(BaseModel):
    node_id: str = "UAIDTIN-ALPHA-07"
    action_type: str
    payload: Dict[str, Any]
    
    def summarize(self):
        asset = self.payload.get('asset', 'N/A')
        return f"MANDATE: {self.action_type} | ASSET: {asset}"
