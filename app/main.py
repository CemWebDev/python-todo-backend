from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, todo

app = FastAPI(
    title="Todo API with API Key Authentication",
    description="A RESTful API for managing todos with API key authentication",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(todo.router)

@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to the Todo API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)