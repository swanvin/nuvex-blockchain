from wasmtime import Store, Module, Instance, Linker, Engine
import os
from typing import Dict

def execute_wasm_contract(tx: Dict) -> str:
    wasm_file = "nuvex_wasm_bg.wasm"
    if not os.path.exists(wasm_file):
        return "WASM file not found (compile with wasm-pack first)"
    engine = Engine()  # Create Engine for compilation
    store = Store(engine)  # Pass Engine to Store
    module = Module.from_file(engine, wasm_file)  # Use Engine to load module
    linker = Linker(engine)  # Linker needs Engine too
    instance = Instance(store, module, linker)
    sender = tx.get("sender", "user1")
    asset_type = tx.get("sector", "cannabis")
    amount = tx.get("yield_amount", 100) or 100
    shard_id = tx.get("shard_id", 0)
    token = tx.get("token", "GRN")
    result = instance.exports(store).track_green_asset(sender, asset_type, amount, shard_id, token)
    return result.decode("utf-8")
