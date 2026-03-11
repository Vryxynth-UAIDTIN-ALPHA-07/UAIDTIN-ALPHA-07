# --- SOVEREIGN CONSTITUTION ---
# VERSION: 1.0.0 | STATUS: IMMUTABLE_CORE
# PRIMARY_GOVERNANCE_RULES

class SovereignLaw:
    # Rule 1: Priority Sectors Only
    VALID_SECTORS = ["OPTIMIZE", "SYNC", "NODE", "LEDGER", "HARARE", "SETTLE"]
    
    # Rule 2: Minimum Integrity Threshold
    # Any mandate with priority below this is ignored by the mesh.
    MIN_PRIORITY = 1
    
    # Rule 3: Zero-Debtor Protocol
    # The node cannot authorize a settlement if it results in a negative balance.
    STRICT_SETTLEMENT = True

    @classmethod
    def validate_mandate(cls, instruction: str):
        """The Judicial Filter: Hardcoded logic that cannot be bypassed."""
        cmd = instruction.upper().split()
        if not cmd:
            return False, "EMPTY_MANDATE"
        
        # Sector Enforcement
        if not any(sector in cmd for sector in cls.VALID_SECTORS):
            return False, f"ILLEGAL_SECTOR: {cmd[0]} is outside Governance Scope."
        
        return True, "AUTHORIZED"
