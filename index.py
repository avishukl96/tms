from fastapi import FastAPI
from routes.index import user
#calling Fastapi
app = FastAPI()
app.include_router(user)


