import wasmer
from wasmer import Store, Module, Instance
import os

def execute_wasm_contract(tx: Dict) -> str:
    wasm_file = "track_green_asset.wasm"
    if not os.path.exists(wasm_file):
        return "WASM file not found (compile from Rust first)"
    store = Store()
    module = Module(store, open(wasm_file, "rb").read())
    instance = Instance(module)
    sender = tx.get("sender", "user1")
    asset_type = tx.get("sector", "cannabis")
    amount = tx.get("yield_amount", 100) or 100
    shard_id = tx.get("shard_id", 0)
    token = tx.get("token", "GRN")
    result = instance.exports.track_green_asset(sender, asset_type, amount, shard_id, token)
    return result.decode("utf-8")
