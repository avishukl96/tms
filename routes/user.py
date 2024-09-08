from fastapi import APIRouter, HTTPException, Depends
from config.db import conn
from models.user import users
from schemas.user import User, UserLogin #, UserOut
from schemas.user import User, UserLogin
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import logging
from sqlalchemy import insert


user = APIRouter()

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def row_to_dict(row):
    """ Convert SQLAlchemy row to a dictionary """
    if row is None:
        return {}
    return dict(row._mapping) if hasattr(row, '_mapping') else dict(row)

def get_all_users():
    """ Fetch all users from the database and convert them to a list of dictionaries """
    results = conn.execute(users.select()).fetchall()
    return [row_to_dict(row) for row in results]

def get_user_by_id(user_id: int):
    """ Fetch a user by their ID from the database and convert the result to a dictionary """
    try:
        result = conn.execute(users.select().where(users.c.id == user_id)).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        user_dict = row_to_dict(result)
        return user_dict
    except Exception as e:
        logging.error(f"Error fetching user by ID: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

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

@user.post("/register")
async def register_user(user: User):
    try:
        # Check if user already exists
        existing_user = conn.execute(users.select().where(users.c.email == user.email)).fetchone()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash the user's password and insert the new user
        hashed_password = get_password_hash(user.password)
        conn.execute(users.insert().values(
            name=user.name,
            email=user.email,
            password=hashed_password
        ))
        conn.commit() 
        return get_all_users()  # Return all data after insertion
        # print(hashed_password)
        # return {"msg": "User registered successfully"}
    except Exception as e:
        logging.error(f"Error inserting data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@user.post("/login")
# async def login_user(user: UserLogin):
#     try:
#         # Fetch user by email
#         db_user = conn.execute(users.select().where(users.c.email == user.email)).fetchone()
#         hashed_password = get_password_hash(user.password)
#         if db_user is None or not verify_password(hashed_password, db_user.password):
#             raise HTTPException(status_code=400, detail="Invalid credentials")

#         # Generate JWT token
#         access_token = create_access_token(data={"sub": db_user.email})
#         return {"access_token": access_token, "token_type": "bearer"}
#     except Exception as e:
#         logging.error(f"Error during login: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

async def login_user(user: UserLogin):
    try:
        # Fetch user by email
        db_user = conn.execute(users.select().where(users.c.email == user.email)).fetchone()
        #print(db_user.id)
        if db_user is None:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        # Get hashed password from the database
        stored_hashed_password = db_user.password
        
        # Verify the password
        if not verify_password(user.password, stored_hashed_password):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        userdata= get_user_by_id(db_user.id);
        # Generate JWT token
        access_token = create_access_token(data={"sub": db_user.email})
        return {"access_token": access_token, "token_type": "bearer","user":userdata}
    except Exception as e:
        logging.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@user.put("/{id}")
async def update_data(id: int, user: User):
    try:
        result = conn.execute(users.update().where(users.c.id == id).values(
            name=user.name,
            email=user.email,
            password=get_password_hash(user.password)  # Hash the password before updating
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
