from fastapi import (
    FastAPI
)

app = FastAPI()

status = {

    "market":
    "RUNNING",

    "ai":
    "RUNNING",

    "paper":
    "RUNNING"
}


@app.get("/status")
def get_status():

    return status


@app.get("/health")
def health():

    return {

        "ok":
        True
    }