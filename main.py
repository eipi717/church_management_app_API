from fastapi import FastAPI
from routes.announcement_routes import router as announcement_router

app = FastAPI()

app.include_router(announcement_router, prefix='/announcement')


