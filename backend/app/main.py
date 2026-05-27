from fastapi import FastAPI
from app.routers import admin_router, reserve_router, seat_router
from app.db import Base, engine
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router.router)
app.include_router(reserve_router.router)
app.include_router(seat_router.router)