import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def timing(request: Request, call_next):
    start = time.perf_counter()  # ДО endpoint-а
    response = await call_next(request)  # тут працює endpoint
    ms = (time.perf_counter() - start) * 1000  # ПІСЛЯ endpoint-а
    response.headers["X-Process-Time"] = f"{ms:.1f}ms"
    print(f"{request.method} {request.url.path} -> {response.status_code}")
    return response

@app.get("/hello")
def hello():
    return {"msg": "hi"}

