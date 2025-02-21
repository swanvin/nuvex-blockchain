import hashlib
import time
from typing import Dict

def perform_pouw_task(index: int, sector: str, data: Dict, shard_id: int, token: str) -> Dict:
    start_time = time.time()
    if token == "GRN":
        if sector == "cannabis":
            batch_id = data.get("batch_id", "batch-001")
            thc_level = data.get("thc_level", 15.0)
            proof_input = f"{shard_id}-{token}-{batch_id}-{thc_level}-{index}".encode()
            proof = hashlib.sha256(proof_input).hexdigest()
            result = "Compliant" if thc_level <= 20.0 else "Non-compliant"
        elif sector == "green_produce":
            yield_amount = data.get("yield_amount", 1000)
            soil_health = data.get("soil_health_index", 7.5)
            carbon_offset = yield_amount * 0.02
            proof_input = f"{shard_id}-{token}-{yield_amount}-{soil_health}-{carbon_offset}-{index}".encode()
            proof = hashlib.sha256(proof_input).hexdigest()
            result = f"{carbon_offset} kg CO2 offset, Soil: {soil_health}/10"
    elif token == "PRN" and sector == "purple_crops":
        batch_id = data.get("batch_id", "grape-001")
        pesticide_level = data.get("pesticide_level", 0.1)
        brix_level = data.get("brix_level", 24.0)
        brix_min = data.get("brix_min", 22.0)
        proof_input = f"{shard_id}-{token}-{batch_id}-{pesticide_level}-{brix_level}-{index}".encode()
        proof = hashlib.sha256(proof_input).hexdigest()
        result = "EU Organic" if pesticide_level < 0.5 and brix_level >= brix_min else "Non-compliant"
    elif token == "RRN" and sector == "red_crops":
        shipment_id = data.get("shipment_id", "tomato-001")
        safety_score = data.get("safety_score", 95)
        water_content = data.get("water_content", 94)
        proof_input = f"{shard_id}-{token}-{shipment_id}-{safety_score}-{water_content}-{index}".encode()
        proof = hashlib.sha256(proof_input).hexdigest()
        result = "FDA Compliant" if safety_score >= 90 and 90 <= water_content <= 96 else "Non-compliant"
    else:
        raise ValueError("Invalid sector/token")
    elapsed = time.time() - start_time
    return {
        "shard_id": shard_id,
        "token": token,
        "block_index": index,
        "proof": proof,
        "useful_work": f"Shard {shard_id}: {token} Verified {sector} - {result}",
        "execution_time": f"{elapsed:.3f}s"
    }
