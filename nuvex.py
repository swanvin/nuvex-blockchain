import time
import hashlib
import json
from typing import List, Dict
from powu import perform_pouw_task
from wasm_executor import execute_wasm_contract
from shard_manager import ShardManager
from tokens import TokenRegistry

class NuvexBlockchain:
    MAX_SUPPLY = 750_000_000  # Hard-coded max supply
    INITIAL_SUPPLY = 750_000_000 * 0.5  # 50% pre-mined (375M NVX)
    HALVING_INTERVAL = 4 * 365 * 24 * 60 * 60  # 4 years in seconds
    BURN_RATE = 0.01  # 1% of tx fees burned

    def __init__(self, shard_count: int = 4):
        self.shards = ShardManager(shard_count)
        self.token_registry = TokenRegistry(["GRN", "PRN", "RRN"])
        self.chain: List[Dict] = []
        self.stake: Dict[str, float] = {}
        self.processed_tx_hashes: set = set()
        self.total_supply = self.INITIAL_SUPPLY
        self.genesis_timestamp = time.time()
        self.blocks_mined = 0
        self.genesis_block()

    def genesis_block(self):
        for shard_id in range(self.shards.count):
            block = {
                "shard_id": shard_id,
                "index": 0,
                "timestamp": time.time(),
                "previous_hash": "0",
                "transactions": [],
                "hash": self.calculate_hash(0, "0", [], shard_id)
            }
            self.shards.add_block(shard_id, block)

    def calculate_hash(self, index: int, previous_hash: str, transactions: List, shard_id: int) -> str:
        value = f"{shard_id}{index}{previous_hash}{json.dumps(transactions)}{time.time()}"
        return hashlib.sha256(value.encode()).hexdigest()

    def add_stake(self, address: str, amount: float):
        self.stake[address] = self.stake.get(address, 0) + amount

    def validate_block(self, block: Dict, shard_id: int) -> bool:
        prev_block = self.shards.get_latest_block(shard_id)
        if prev_block is None or block["index"] != prev_block["index"] + 1 or block["previous_hash"] != prev_block["hash"]:
            return False
        return True

    def hash_transaction(self, tx: Dict) -> str:
        tx_string = str(sorted(tx.items()))
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def get_current_reward(self) -> float:
        elapsed = time.time() - self.genesis_timestamp
        halvings = int(elapsed // self.HALVING_INTERVAL)
        base_reward = 5.0 / (2 ** halvings)
        return max(base_reward, 0.1)

    def mine_block(self, shard_id: int, transactions: List[Dict], validator: str) -> Dict:
        if validator not in self.stake or self.stake[validator] < 1.0:
            raise ValueError("Insufficient stake")
        
        prev_block = self.shards.get_latest_block(shard_id)
        pouw_results = []
        for tx in transactions:
            tx_hash = self.hash_transaction(tx)
            if tx_hash in self.processed_tx_hashes:
                raise ValueError("Double-spend detected! Transaction rejected.")
            self.processed_tx_hashes.add(tx_hash)
            sector = tx.get("sector", "unknown")
            token = tx.get("token", "GRN")
            pouw_result = perform_pouw_task(prev_block["index"] + 1, sector, tx, shard_id, token)
            pouw_results.append(pouw_result)

        reward = self.get_current_reward()
        burn_amount = reward * self.BURN_RATE
        net_reward = reward - burn_amount

        if self.total_supply + net_reward > self.MAX_SUPPLY:
            raise ValueError("Max supply exceeded")

        block = {
            "shard_id": shard_id,
            "index": prev_block["index"] + 1,
            "timestamp": time.time(),
            "previous_hash": prev_block["hash"],
            "transactions": transactions,
            "pouw_results": pouw_results,
            "reward": reward,
            "burned_nvx": burn_amount,
            "hash": self.calculate_hash(prev_block["index"] + 1, prev_block["hash"], transactions, shard_id)
        }
        
        if self.validate_block(block, shard_id):
            self.shards.add_block(shard_id, block)
            self.reward_validator(validator, shard_id, net_reward)
            self.total_supply += net_reward
            self.blocks_mined += 1
            return block
        raise ValueError("Block validation failed")

    def reward_validator(self, validator: str, shard_id: int, net_reward: float):
        self.stake[validator] += net_reward
        for tx in self.shards.get_latest_block(shard_id)["transactions"]:
            token = tx.get("token", "GRN")
            self.token_registry.add_balance(validator, token, 10.0)

    def execute_transaction(self, tx: Dict) -> str:
        shard_id = tx.get("shard_id", 0)
        wasm_result = execute_wasm_contract(tx)
        self.mine_block(shard_id, [tx], "validator1")
        return wasm_result

if __name__ == "__main__":
    nvx = NuvexBlockchain()
    nvx.add_stake("validator1", 100.0)
    tx = {"sector": "cannabis", "batch_id": "CA-123", "thc_level": 18.5, "shard_id": 0, "token": "GRN"}
    print(nvx.execute_transaction(tx))
    print(f"Total Supply: {nvx.total_supply}")
