from fastapi import APIRouter, HTTPException, Depends
from config.db import conn
from models.task import tasks
from schemas.task import Task, TaskUpdate
from models.user import users
import logging

task = APIRouter()


def row_to_dict(row):
    """ Convert SQLAlchemy row to a dictionary """
    if row is None:
        return {}
    return dict(row._mapping) if hasattr(row, '_mapping') else dict(row)


@task.post("/")
async def create_task(task: Task):
    try:
        # Check if admin exists
        # admin_exists = conn.execute("SELECT 1 FROM administrator WHERE admin_id = :id", {"id": task.admin_id}).fetchone()
        # if not admin_exists:
        #     raise HTTPException(status_code=404, detail="Admin not found")

        # Insert new task
        conn.execute(tasks.insert().values(
            title=task.title,
            description=task.description,
            status=task.status,
            assigned_to=task.assigned_to,
            admin_id=task.admin_id  # Include admin_id in task creation
        ))
        conn.commit()
        return {"msg": "Task created successfully"}
    except Exception as e:
        logging.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@task.put("/{id}")
async def update_task_status(id: int, task: TaskUpdate):
    try:
        # Update the task status
        result = conn.execute(tasks.update().where(tasks.c.id == id).values(
            status=task.status
        ))
        conn.commit()
        if result.rowcount:
            return {"msg": "Task updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        logging.error(f"Error updating task status for id {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@task.get("/")
async def get_all_tasks():
    try:
        results = conn.execute(tasks.select()).fetchall()

        return [row_to_dict(row) for row in results]
        #return [dict(row) for row in results]
    except Exception as e:
        logging.error(f"Error fetching tasks: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@task.get("/{id}")
async def get_task_by_id(id: int):
    try:
        result = conn.execute(tasks.select().where(tasks.c.id == id)).fetchone()
        # if result:
        #     return dict(result)
        # else:
        #     raise HTTPException(status_code=404, detail="Task not found")

        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        user_dict = row_to_dict(result)
        return user_dict
    except Exception as e:
        logging.error(f"Error fetching task for id {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
