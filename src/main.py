from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    return {"status": "received", "data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




