from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.routes import todos
from fastapi.middleware.cors import CORSMiddleware


# Lifespan context manager (replaces on_event)
@asynccontextmanager
async def lifespan(app_: FastAPI):
    # Database initialization - using async approach with SQLAlchemy
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cleanup (if needed)


# Create FastAPI app with lifespan
app = FastAPI(title="Todo API", lifespan=lifespan)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(todos.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
