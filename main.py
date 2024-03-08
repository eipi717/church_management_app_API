from fastapi import FastAPI
from routes.announcement_routes import router as announcement_router
from routes.user_routes import router as user_router
from routes.auth_routes import router as auth_router

app = FastAPI()

app.include_router(announcement_router, prefix='/announcement')

app.include_router(user_router, prefix='/user')

app.include_router(auth_router, prefix='/auth')


