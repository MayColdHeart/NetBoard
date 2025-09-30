from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
async def hello_get():
    return {"message": "Hello, GET!"}

@app.post("/data")
async def hello_post(data: dict):
    return {"message": "Hello, POST!", "received": data}