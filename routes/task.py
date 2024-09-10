from fastapi import APIRouter, HTTPException, Depends,Request,status
from fastapi.responses import JSONResponse
from config.db import conn
from models.task import tasks
from schemas.task import Task, TaskUpdate
from models.user import users
from models.admin import admin
import logging
from sqlalchemy import select,  and_

task = APIRouter()


def row_to_dict(row):
    """ Convert SQLAlchemy row to a dictionary """
    if row is None:
        return {}
    return dict(row._mapping) if hasattr(row, '_mapping') else dict(row)

# Utility function to check if a record exists
def record_exists(table, id):
    query = select(table.c.id).where(table.c.id == id)
    result = conn.execute(query)
    return result.fetchone() is not None



@task.post("/")
async def create_task(task: Task):
    try:
        # Check if admin exists
        # query = select(admin.c.admin_id).where(admin.c.admin_id == task.admin_id)
        # admin_exists = await conn.fetch_one(query)
        # if not admin_exists:
        #     raise HTTPException(status_code=404, detail="Admin not found")

        #query = select([admin.c.admin_id]).where(admin.c.admin_id == task.admin_id)

        #task_data = await request.json()

       # print(task.title);
    
        title = task.title
        description = task.description
        status_code = task.status
        assigned_to = task.assigned_to
        admin_id = task.admin_id

        if not title.strip() or not status_code.strip() or not assigned_to or not admin_id:
            missing_fields = []
            if not title.strip():
                missing_fields.append("title")
            if not status_code.strip():
                missing_fields.append("status")
            if not assigned_to:
                missing_fields.append("assigned_to")
            if not admin_id:
                missing_fields.append("admin_id")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"success": 0, "msg": f"Missing fields: {', '.join(missing_fields)}"}
            )
    

          # Check if user exists
        if not record_exists(users, assigned_to):
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"success": 0, "msg": "User not found"})
        
        query = select(admin.c.admin_id).where(admin.c.admin_id == task.admin_id)
        result = conn.execute(query).fetchone()
        if not result:
            #raise HTTPException(status_code=404, detail="Admin not found")
            return JSONResponse(status_code=404, content={"success": 0, "msg": "Admin not found"})

        # Insert new task
        query = tasks.insert().values(
            title=task.title,
            description=task.description,
            status=task.status,
            assigned_to=task.assigned_to,
            admin_id=task.admin_id  # Include admin_id in task creation
        )
        conn.execute(query)
        conn.commit()

        #return {"msg": "Task created successfully"}
        return JSONResponse(status_code=200, content={"success": 1, "msg": "Task created successfully"})


    except Exception as e:
        logging.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@task.put("/{id}")
async def update_task_status(id: int, task: TaskUpdate):
    try:
        # Validate the status and assigned_to fields
        status_code = task.status
        assigned_to = task.assigned_to
    
        if not status_code.strip() or not assigned_to:
            missing_fields = []
            if not status_code.strip():
                missing_fields.append("status")
            if not assigned_to:
                missing_fields.append("assigned_to")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"success": 0, "msg": f"Missing fields: {', '.join(missing_fields)}"}
            )

        # Check if the task is authorized with the same user
        query = select(tasks.c.admin_id).where(
            and_(
                tasks.c.id == id,  # Check the task ID
                tasks.c.assigned_to == assigned_to  # Check if assigned to the correct user
            )
        )
        result = conn.execute(query).fetchone()
        if not result:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": 0, "msg": "You are not authorized to update this task."}
            )

        # Update the task status
        update_query = tasks.update().where(tasks.c.id == id).values(
            status=status_code
        )
        result = conn.execute(update_query)
        conn.commit()

        if result.rowcount:
            return {"msg": "Task updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Task not found")

    except Exception as e:
        logging.error(f"Error updating task status for id {id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
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
