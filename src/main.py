
from fastapi import FastAPI
import uvicorn
import asyncio
import time
import threading

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms

app = FastAPI()
app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)

@app.get("/sync/{id}")
def sync_func(id: int):
    print(f"sync. Потоков: {threading.active_count()}")
    print(f"sync. Начал {id}: {time.time():.2f}")
    time.sleep(3)
    print(f"sync. Закончил {id}: {time.time():.2f}")

@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async. Потоков: {threading.active_count()}")
    print(f"async. Начал {id}: {time.time():.2f}")
    await asyncio.sleep(3)
    print(f"async. Закончил {id}: {time.time():.2f}")





if __name__ == "__main__":
    uvicorn.run("main:app", reload=False)