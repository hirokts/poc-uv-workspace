from fastapi import FastAPI
from libs import now_iso

app = FastAPI()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "time": now_iso(),
    }


def main():
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
    