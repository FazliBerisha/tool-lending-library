from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Tool Lending Library API"}

@app.get("/tools")
async def get_tools():
    # This is a placeholder. In the future, you'll fetch this from a database.
    tools = [
        {"id": 1, "name": "Hammer", "available": True},
        {"id": 2, "name": "Drill", "available": False},
    ]
    return {"tools": tools}