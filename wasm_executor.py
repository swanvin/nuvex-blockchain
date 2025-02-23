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

    # Define __wbindgen_string_new (wbg namespace)
    linker.define(
        store,
        "wbg",
        "__wbindgen_string_new",
        Func(
            store,
            FuncType([ValType.i32(), ValType.i32()], [ValType.externref()]),
            lambda x, y: None  # Dummy: null externref
        )
    )

    # Define __wbindgen_throw (wbg namespace)
    linker.define(
        store,
        "wbg",
        "__wbindgen_throw",
        Func(
            store,
            FuncType([ValType.i32(), ValType.i32()], []),
            lambda x, y: None  # Dummy: no-op
        )
    )

    # Define __wbg_now_807e54c39636c349 (wbg namespace)
    linker.define(
        store,
        "wbg",
        "__wbg_now_807e54c39636c349",
        Func(
            store,
            FuncType([], [ValType.f64()]),
            lambda: float(os.time.time())  # Dummy timestamp
        )
    )

    # Define __wbindgen_init_externref_table (wbg namespace)
    linker.define(
        store,
        "wbg",
        "__wbindgen_init_externref_table",
        Func(
            store,
            FuncType([], []),
            lambda: None  # Dummy: no-op
        )
    )

    instance = linker.instantiate(store, module)
    exports = instance.exports(store)
    
    # Debug: Print available exports
    export_names = [key for key in exports.__dict__.keys() if not key.startswith('_')]
    print("Available exports:", export_names)
    
    # Try possible export names
    track_green_asset_func = exports.get("track_green_asset")
    if track_green_asset_func is None:
        track_green_asset_func = exports.get("__wasm_export_track_green_asset")
        if track_green_asset_func is None:
            return f"Export 'track_green_asset' not found. Available: {export_names}"  # Exit here
    
    sender = tx.get("sender", "user1")
    asset_type = tx.get("sector", "cannabis")
    amount = tx.get("yield_amount", 100) or 100
    shard_id = tx.get("shard_id", 0)
    token = tx.get("token", "GRN")
    result = track_green_asset_func(store, sender, asset_type, amount, shard_id, token)
    return result.decode("utf-8")
