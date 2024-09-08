from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AdminBase(BaseModel):
    admin_name: str
    admin_email: Optional[EmailStr]

class AdminCreate(AdminBase):
    pass

class Admin(AdminBase): 
    admin_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  
