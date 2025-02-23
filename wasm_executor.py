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

    # Define required imports (minimal set)
    linker.define(store, "wbg", "__wbindgen_string_new", Func(store, FuncType([ValType.i32(), ValType.i32()], [ValType.externref()]), lambda x, y: None))
    linker.define(store, "wbg", "__wbindgen_throw", Func(store, FuncType([ValType.i32(), ValType.i32()], []), lambda x, y: None))
    linker.define(store, "wbg", "__wbg_now_807e54c39636c349", Func(store, FuncType([], [ValType.f64()]), lambda: float(os.time.time())))
    linker.define(store, "wbg", "__wbindgen_init_externref_table", Func(store, FuncType([], []), lambda: None))

    instance = linker.instantiate(store, module)
    exports = instance.exports(store)
    
    # Debug: Use dir() to inspect exports object
    export_names = [name for name in dir(exports) if not name.startswith('_')]
    print("Available exports (via dir):", export_names)
    
    # Try fetching the export directly
    track_green_asset_func = getattr(exports, "track_green_asset", None)
    print(f"Fetched 'track_green_asset': {track_green_asset_func}")
    if track_green_asset_func is None:
        return f"Export 'track_green_asset' not found. Available: {export_names}"
    
    sender = tx.get("sender", "user1")
    asset_type = tx.get("sector", "cannabis")
    amount = tx.get("yield_amount", 100) or 100
    shard_id = tx.get("shard_id", 0)
    token = tx.get("token", "GRN")
    print("Calling track_green_asset with args:", sender, asset_type, amount, shard_id, token)
    result = track_green_asset_func(store, sender, asset_type, amount, shard_id, token)
    return result.decode("utf-8")
