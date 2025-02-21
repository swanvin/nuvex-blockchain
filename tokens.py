from typing import Dict, List

class TokenRegistry:
    def __init__(self, tokens: List[str]):
        self.balances: Dict[str, Dict[str, float]] = {token: {} for token in tokens}

    def add_balance(self, address: str, token: str, amount: float):
        if token not in self.balances:
            raise ValueError("Invalid token")
        self.balances[token][address] = self.balances[token].get(address, 0) + amount
