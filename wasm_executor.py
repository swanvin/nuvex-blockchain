from wasmtime import Store, Module, Instance, Linker, Engine, Func, FuncType, ValType
import os
from typing import Dict
from ctypes import create_string_buffer, memmove, c_void_p

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
    
    malloc = exports.get("__wbindgen_malloc")
    memory = exports.get("memory")
    if malloc is None or memory is None:
        return "Missing malloc or memory exports"

    sender = tx.get("sender", "user1")
    asset_type = tx.get("sector", "cannabis")
    amount = tx.get("yield_amount", 100) or 100
    shard_id = tx.get("shard_id", 0)
    token = tx.get("token", "GRN")

    # Allocate and write strings to WASM memory
    sender_bytes = sender.encode("utf-8")
    sender_ptr = malloc(store, len(sender_bytes), 4)
    sender_buffer = create_string_buffer(sender_bytes)
    base_addr = int(c_void_p.from_buffer(memory.data_ptr(store)).value)  # Get raw address
    memmove(base_addr + sender_ptr, sender_buffer, len(sender_bytes))

    asset_type_bytes = asset_type.encode("utf-8")
    asset_type_ptr = malloc(store, len(asset_type_bytes), 4)
    asset_type_buffer = create_string_buffer(asset_type_bytes)
    memmove(base_addr + asset_type_ptr, asset_type_buffer, len(asset_type_bytes))

    token_bytes = token.encode("utf-8")
    token_ptr = malloc(store, len(token_bytes), 4)
    token_buffer = create_string_buffer(token_bytes)
    memmove(base_addr + token_ptr, token_buffer, len(token_bytes))

    print("Calling track_green_asset with args:", sender, asset_type, amount, shard_id, token)
    result = track_green_asset_func(
        store,
        sender_ptr, len(sender_bytes),
        asset_type_ptr, len(asset_type_bytes),
        amount,
        shard_id,
        token_ptr, len(token_bytes)
    )
    return result.decode("utf-8")
