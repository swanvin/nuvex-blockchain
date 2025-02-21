#!/bin/bash
echo "Compiling track_green_asset.wasm..."
cd wasm_source
wasm-pack build --target web --out-dir ../ --out-name track_green_asset
mv ../track_green_asset.wasm ../
cd ..
echo "Compilation complete. WASM file is in root directory."
