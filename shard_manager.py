from typing import Dict, List

class ShardManager:
    def __init__(self, shard_count: int):
        self.count = shard_count
        self.shards: Dict[int, List[Dict]] = {}

    def add_block(self, shard_id: int, block: Dict):
        if shard_id not in self.shards:
            self.shards[shard_id] = []
        self.shards[shard_id].append(block)

    def get_latest_block(self, shard_id: int) -> Dict:
        return self.shards[shard_id][-1] if shard_id in self.shards and self.shards[shard_id] else None
