from fastapi import FastAPI
from routes.index import user
#calling Fastapi
app = FastAPI()
app.include_router(user)


from fastapi import FastAPI
from routes.user import user
from routes.task import task
# from routes.admin import admin

app = FastAPI()

app.include_router(user, prefix="/users")
app.include_router(task, prefix="/tasks")
#app.include_router(admin, prefix="/admin")
