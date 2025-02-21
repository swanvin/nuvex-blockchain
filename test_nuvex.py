from nuvex import NuvexBlockchain
import time

def test_nuvex():
    nvx = NuvexBlockchain()
    nvx.add_stake("validator1", 100.0)
    txs = [
        {"sector": "cannabis", "batch_id": "CA-123", "thc_level": 18.5, "shard_id": 0, "token": "GRN", "sender": "farmer1"},
        {"sector": "green_produce", "yield_amount": 1500, "soil_health_index": 8.2, "shard_id": 1, "token": "GRN", "sender": "farmer2"},
        {"sector": "purple_crops", "batch_id": "grape-001", "pesticide_level": 0.2, "brix_level": 24.5, "brix_min": 22.0, "shard_id": 2, "token": "PRN", "sender": "farmer3"},
        {"sector": "red_crops", "shipment_id": "tomato-001", "safety_score": 92, "water_content": 95, "shard_id": 3, "token": "RRN", "sender": "farmer4"},
    ]
    for tx in txs:
        result = nvx.execute_transaction(tx)
        print(f"Transaction Result: {result}")
    for shard_id in range(nvx.shards.count):
        latest_block = nvx.shards.get_latest_block(shard_id)
        print(f"Shard {shard_id} Latest Block: {latest_block}")

def test_double_spend_rejection():
    nvx = NuvexBlockchain()
    nvx.add_stake("validator1", 100.0)
    tx = {"sector": "cannabis", "batch_id": "CA-123", "thc_level": 18.5, "shard_id": 0, "token": "GRN"}
    nvx.execute_transaction(tx)
    try:
        nvx.execute_transaction(tx)
        assert False, "Double-spend not detected!"
    except ValueError as e:
        assert "Double-spend detected" in str(e)
        print("Double-spend rejection test passed!")

def test_shard_consistency():
    nvx = NuvexBlockchain()
    nvx.add_stake("validator1", 100.0)
    tx1 = {"sector": "cannabis", "batch_id": "CA-124", "thc_level": 17.0, "shard_id": 0, "token": "GRN"}
    tx2 = {"sector": "green_produce", "yield_amount": 2000, "soil_health_index": 7.8, "shard_id": 1, "token": "GRN"}
    nvx.execute_transaction(tx1)
    nvx.execute_transaction(tx2)
    shard0_block = nvx.shards.get_latest_block(0)
    shard1_block = nvx.shards.get_latest_block(1)
    assert shard0_block["index"] == 1, "Shard 0 index mismatch"
    assert shard1_block["index"] == 1, "Shard 1 index mismatch"
    print("Shard consistency test passed!")

def test_high_load():
    nvx = NuvexBlockchain()
    nvx.add_stake("validator1", 100.0)
    transactions = [
        {"sector": "cannabis", "batch_id": f"CA-{i}", "thc_level": 18.5, "shard_id": i % 4, "token": "GRN"}
        for i in range(1000)
    ]
    start_time = time.time()
    for tx in transactions:
        nvx.execute_transaction(tx)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Processed 1000 transactions in {elapsed_time:.2f} seconds")
    assert elapsed_time < 10, "Transaction processing took too long!"

if __name__ == "__main__":
    test_nuvex()
    test_double_spend_rejection()
    test_shard_consistency()
    test_high_load()
