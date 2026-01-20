import os
import time
import subprocess
import requests

def test_redis_failure_recovery():
    print("Starting Ingestion...")
    # Simulate sending data
    requests.post("http://localhost:8000/webhook/whatsapp", json={
        "entry": [{"changes": [{"value": {"messages": [{"from": "12345", "text": {"body": "test"}}]}}]}]
    })
    
    print("Killing Redis...")
    subprocess.run("docker-compose kill redis", shell=True)
    
    print("Simulating ingestion during outage...")
    try:
        requests.post("http://localhost:8000/webhook/whatsapp", json={
            "entry": [{"changes": [{"value": {"messages": [{"from": "67890", "text": {"body": "test outage"}}]}}]}]
        }, timeout=2)
    except:
        print("Expected failure/timeout during redis outage")
        
    print("Reviving Redis...")
    subprocess.run("docker-compose start redis", shell=True)
    time.sleep(5)
    
    print("Verifying system returned to health...")
    r = requests.get("http://localhost:8000/health")
    assert r.status_code == 200
    print("System Healthy!")

if __name__ == "__main__":
    test_redis_failure_recovery()
