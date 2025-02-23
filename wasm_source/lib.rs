use wasm_bindgen::prelude::*;
use js_sys::Date;  // Add this for Date::now()
use serde::{Serialize, Deserialize};
use sha2::{Sha256, Digest};

#[derive(Serialize, Deserialize)]
struct Asset {
    token: String,
    asset_type: String,
    amount: u64,
    sender: String,
    shard_id: u64,
    timestamp: u64,
    tx_hash: String,
}

#[wasm_bindgen]
pub fn track_green_asset(sender: String, asset_type: String, amount: u64, shard_id: u64, token: String) -> JsValue {
    let valid_types: Vec<&str> = match token.as_str() {
        "GRN" => vec!["cannabis", "avocados", "spinach", "limes", "kale", "broccoli", "lettuce"],
        "PRN" => vec!["grapes", "purple_cabbage", "eggplants", "plums", "blackberries"],
        "RRN" => vec!["tomatoes", "red_peppers", "cherries"],
        _ => return JsValue::from_str("Error: Invalid token"),
    };
    if !valid_types.contains(&asset_type.as_str()) || amount < 1 || amount > 1_000_000 {
        return JsValue::from_str("Error: Invalid input (amount 1-1M)");
    }
    let mut hasher = Sha256::new();
    hasher.update(format!("{}-{}-{}-{}-{}", sender, asset_type, amount, shard_id, token));
    let tx_hash = format!("{:x}", hasher.finalize());
    let asset = Asset {
        token,
        asset_type,
        amount,
        sender,
        shard_id,
        timestamp: Date::now() as u64,  // Simplified js_sys::Date::now()
        tx_hash,
    };
    match serde_json::to_string(&asset) {
        Ok(json) => JsValue::from_str(&json),  // Convert String to &str
        Err(_) => JsValue::from_str("Error: Serialization failed"),
    }
}
