# needs uvicorn installed: pip install uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    print("Hello World")