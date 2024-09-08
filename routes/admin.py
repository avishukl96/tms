from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from config.db import conn
from models.admin import admin
from schemas.admin import Admin, AdminCreate
from sqlalchemy import select, insert
   
router = APIRouter()

@router.post("/admins/", response_model=Admin)
def create_admin(admin_data: AdminCreate, db: Session = Depends(conn)):
    stmt = insert(admin).values(
        admin_name=admin_data.admin_name,
        admin_email=admin_data.admin_email,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    ).returning(admin.c.admin_id)

    result = db.execute(stmt)
    db.commit()
    created_admin = db.execute(select(admin).where(admin.c.admin_id == result.scalar_one())).first()
    if created_admin is None:
        raise HTTPException(status_code=404, detail="Admin not created")
    
    return created_admin

@router.get("/admins/", response_model=List[Admin])
def read_admins(skip: int = 0, limit: int = 10, db: Session = Depends(conn)):
    stmt = select(admin).offset(skip).limit(limit)
    result = db.execute(stmt).fetchall()
    return result

@router.get("/admins/{admin_id}", response_model=Admin)
def read_admin(admin_id: int, db: Session = Depends(conn)):
    stmt = select(admin).where(admin.c.admin_id == admin_id)
    result = db.execute(stmt).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    return result
