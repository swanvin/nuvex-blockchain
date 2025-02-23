from wasmtime import Store, Module, Instance, Linker, Engine, Func, FuncType, ValType
import os
from typing import Dict

def execute_wasm_contract(tx: Dict) -> str:
    wasm_file = "nuvex_wasm_bg.wasm"
    if not os.path.exists(wasm_file):
        return "WASM file not found (compile with wasm-pack first)"
    engine = Engine()
    store = Store(engine)
    module = Module.from_file(engine, wasm_file)
    linker = Linker(engine)

    # Define __wbindgen_string_new (simulate string allocation)
    memory = None  # Will be set after instantiation
    def string_new(ptr: int, len: int) -> int:
        nonlocal memory
        # Simulate allocation—return a dummy pointer (e.g., 0 for now)
        return 0  # Improve this later with real memory access
    
    linker.define(store, "wbg", "__wbindgen_string_new", Func(store, FuncType([ValType.i32(), ValType.i32()], [ValType.i32()]), string_new))
    linker.define(store, "wbg", "__wbindgen_throw", Func(store, FuncType([ValType.i32(), ValType.i32()], []), lambda x, y: None))
    linker.define(store, "wbg", "__wbg_now_807e54c39636c349", Func(store, FuncType([], [ValType.f64()]), lambda: float(os.time.time())))
    linker.define(store, "wbg", "__wbindgen_init_externref_table", Func(store, FuncType([], []), lambda: None))

    instance = linker.instantiate(store, module)
    exports = instance.exports(store)
    memory = exports.get("memory")  # Get memory export for string handling
    
    export_names = list(exports.keys())
    print("Available exports:", export_names)
    
    track_green_asset_func = exports.get("track_green_asset")
    if track_green_asset_func is None:
        return f"Export 'track_green_asset' not found. Available: {export_names}"
    
    sender = tx.get("sender", "user1")
    asset_type = tx.get("sector", "cannabis")
    amount = tx.get("yield_amount", 100) or 100
    shard_id = tx.get("shard_id", 0)
    token = tx.get("token", "GRN")
    result = track_green_asset_func(store, sender, asset_type, amount, shard_id, token)
    return result.decode("utf-8")
