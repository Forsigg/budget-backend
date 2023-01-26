from fastapi import FastAPI

from apps.user.views import users_router

app = FastAPI()

app.include_router(users_router)
