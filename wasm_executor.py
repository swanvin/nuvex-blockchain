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

    linker.define(store, "wbg", "__wbindgen_string_new", Func(store, FuncType([ValType.i32(), ValType.i32()], [ValType.externref()]), lambda x, y: None))
    linker.define(store, "wbg", "__wbindgen_throw", Func(store, FuncType([ValType.i32(), ValType.i32()], []), lambda x, y: None))
    linker.define(store, "wbg", "__wbg_now_807e54c39636c349", Func(store, FuncType([], [ValType.f64()]), lambda: float(os.time.time())))
    linker.define(store, "wbg", "__wbindgen_init_externref_table", Func(store, FuncType([], []), lambda: None))

    instance = linker.instantiate(store, module)
    exports = instance.exports(store)
    
    export_names = list(exports.keys())
    print("Available exports:", export_names)
    
    track_green_asset_func = exports.get("track_green_asset")
    print(f"Fetched 'track_green_asset': {track_green_asset_func}")
    if track_green_asset_func is None:
        return f"Export 'track_green_asset' not found. Available: {export_names}"
    
    sender = tx.get("sender", "user1")
    asset_type = tx.get("sector", "cannabis")
    amount = tx.get("yield_amount", 100) or 100
    shard_id = tx.get("shard_id", 0)
    token = tx.get("token", "GRN")
    print("Calling track_green_asset with args:", sender, asset_type, amount, shard_id, token)
    # 8 params: ptr/len for each string, direct i32 for amount/shard_id
    result = track_green_asset_func(
        0, len(sender),      # sender_ptr, sender_len (dummy ptr=0)
        0, len(asset_type),  # asset_type_ptr, asset_type_len
        amount,              # amount
        shard_id,            # shard_id
        0, len(token)        # token_ptr, token_len
    )
    return result.decode("utf-8")
