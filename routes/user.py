from fastapi import APIRouter, HTTPException
from config.db import conn
from models.index import users
from schemas.index import User
import logging

user = APIRouter()

def row_to_dict(row):
    """ Convert SQLAlchemy row to a dictionary """
    if row is None:
        return {}
    return dict(row._mapping) if hasattr(row, '_mapping') else dict(row)

def get_all_users():
    """ Fetch all users from the database and convert them to a list of dictionaries """
    results = conn.execute(users.select()).fetchall()
    return [row_to_dict(row) for row in results]

@user.get("/")
async def read_all_data():
    try:
        return get_all_users()
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user.get("/{id}")
async def read_data(id: int):
    try:
        result = conn.execute(users.select().where(users.c.id == id)).fetchone()
        if result:
            return row_to_dict(result)
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logging.error(f"Error fetching data for id {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user.post("/")
async def write_data(user: User):
    try:
        conn.execute(users.insert().values(
            name=user.name,
            email=user.email,
            password=user.password
        ))
        return get_all_users()  # Return all data after insertion
    except Exception as e:
        logging.error(f"Error inserting data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user.put("/{id}")
async def update_data(id: int, user: User):
    try:
        result = conn.execute(users.update().where(users.c.id == id).values(
            name=user.name,
            email=user.email,
            password=user.password
        ))
        if result.rowcount:
            return get_all_users()  # Return all data after update
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logging.error(f"Error updating data for id {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user.delete("/{id}")
async def delete_data(id: int):
    try:
        result = conn.execute(users.delete().where(users.c.id == id))
        if result.rowcount:
            return get_all_users()  # Return all data after deletion
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logging.error(f"Error deleting data for id {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user.get("/debug")
async def debug_endpoint():
    response_data = {"complex": "data"}  # Replace with actual data
    logging.info(f"Response Data: {response_data}")
    return response_data
