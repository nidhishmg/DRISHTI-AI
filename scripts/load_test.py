import asyncio
import httpx
import time

async def send_complaint(i, client):
    payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": f"9198765{i:05d}",
                        "text": {"body": f"Ration issue complaint number {i}"}
                    }]
                }
            }]
        }]
    }
    try:
        await client.post("http://localhost:8000/webhook/whatsapp", json=payload)
    except Exception as e:
        print(f"Request {i} failed: {e}")

async def main():
    async with httpx.AsyncClient() as client:
        start = time.time()
        tasks = [send_complaint(i, client) for i in range(1000)]
        await asyncio.gather(*tasks)
        end = time.time()
        
    print(f"Ingested 1000 complaints in {end-start:.2f} seconds")
    print(f"Throughput: {1000/(end-start):.2f} req/s")

if __name__ == "__main__":
    asyncio.run(main())
