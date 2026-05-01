from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import init_db
from routes.analyze import router as analyze_router
from routes.contacts import router as contacts_router
from routes.history import router as history_router

# Lifespan context manager (replaces on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    print("🚀 SilentSOS Backend Started!")
    print("📊 Database initialized")
    print("🔗 API available at http://localhost:8000")
    print("📖 API docs at http://localhost:8000/docs")
    yield
    # Shutdown (cleanup if needed)
    print("👋 SilentSOS Backend Shutting Down")

# Create FastAPI app with lifespan
app = FastAPI(
    title="SilentSOS API",
    description="AI-powered invisible emergency signal system",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "SilentSOS API is running",
        "status": "active",
        "endpoints": [
            "POST /api/analyze-message",
            "GET /api/contacts",
            "POST /api/contacts",
            "DELETE /api/contacts/{id}",
            "GET /api/alerts",
            "GET /api/alerts/stats",
            "GET /api/alerts/{id}"
        ]
    }

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "healthy"}

# Register all routes
app.include_router(analyze_router, prefix="/api", tags=["Analysis"])
app.include_router(contacts_router, prefix="/api", tags=["Contacts"])
app.include_router(history_router, prefix="/api", tags=["History"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)