import asyncio
import json
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 获取当前脚本所在目录
base_path = os.path.dirname(os.path.abspath(__file__))
counter_file = os.path.join(base_path, "counter.json")

# 启动时从文件读取计数
def load_counter() -> int:
    if os.path.exists(counter_file):
        try:
            with open(counter_file, "r") as f:
                data = json.load(f)
                return int(data.get("visits", 0))
        except Exception:
            pass
    return 0

visit_count = load_counter()

def save_counter():
    with open(counter_file, "w") as f:
        json.dump({"visits": visit_count}, f)

# 每5分钟持久化一次
async def periodic_save():
    while True:
        await asyncio.sleep(300)
        save_counter()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_save())

@app.on_event("shutdown")
async def shutdown_event():
    save_counter()

# 1. 挂载静态资源目录 (例如 image 文件夹)
image_path = os.path.join(base_path, "image")
if os.path.exists(image_path):
    app.mount("/image", StaticFiles(directory=image_path), name="image")

# 2. 根目录直接返回 index.html，并递增计数
@app.get("/")
async def read_index():
    global visit_count
    visit_count += 1
    index_file = os.path.join(base_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "index.html not found"}

# 3. 返回当前访问计数
@app.get("/api/counter")
async def get_counter():
    return JSONResponse({"visits": visit_count})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
