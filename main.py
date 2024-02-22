from fastapi import FastAPI
from routes.announcement_routes import router as announcement_router
from routes.user_routes import router as user_router

app = FastAPI()

app.include_router(announcement_router, prefix='/announcement')

app.include_router(user_router, prefix='/user')


