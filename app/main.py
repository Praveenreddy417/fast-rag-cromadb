from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.chat import router as chat_router
from app.api.routes.healthcheck import router as healthcheck_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FastAPI RAG Service")


origins = [
    "https://your-frontend.vercel.app",  # production frontend
    "http://localhost:3000"              # local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(healthcheck_router)
