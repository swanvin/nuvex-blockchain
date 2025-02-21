# Nuvex (NVX) Blockchain

A next-generation blockchain for fast, scalable, and sustainable transactions. Supports GRN (cannabis/green produce), PRN (purple crops), and RRN (red crops) tokens.

## Features
- Hybrid PoS + PoUW consensus
- Sharding for 10,000+ TPS
- WASM smart contracts
- Multi-token ecosystem (GRN, PRN, RRN)
- Double-spend prevention

## Installation
1. Clone the repo: `git clone https://github.com/swanvin/nuvex-blockchain.git`
2. Install Python dependencies: `pip install -r requirements.txt`
3. Install Rust and wasm-pack: `curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh`
4. Compile WASM contract:
   ```bash
   chmod +x compile_wasm.sh
   ./compile_wasm.sh
