import wasmer
from wasmer import Store, Module, Instance
import os
from typing import Dict

def execute_wasm_contract(tx: Dict) -> str:
    wasm_file = "nuvex_wasm_bg.wasm.compiled"
    if not os.path.exists(wasm_file):
        return "Precompiled WASM file not found (run precompile_wasm.py first)"
    store = Store()
    module = Module.deserialize_from_file(store, wasm_file)
    instance = Instance(module)
    sender = tx.get("sender", "user1")
    asset_type = tx.get("sector", "cannabis")
    amount = tx.get("yield_amount", 100) or 100
    shard_id = tx.get("shard_id", 0)
    token = tx.get("token", "GRN")
    result = instance.exports.track_green_asset(sender, asset_type, amount, shard_id, token)
    return result.decode("utf-8")
