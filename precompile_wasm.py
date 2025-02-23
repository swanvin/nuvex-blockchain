from wasmer import Store, Module
import os

wasm_file = "nuvex_wasm_bg.wasm"
if not os.path.exists(wasm_file):
    print("WASM file not found—compile with wasm-pack first!")
    exit(1)

store = Store()
wasm_bytes = open(wasm_file, "rb").read()
module = Module(store, wasm_bytes)
module.serialize_to_file("nuvex_wasm_bg.wasm.compiled")
print("Precompiled WASM saved as nuvex_wasm_bg.wasm.compiled!")
