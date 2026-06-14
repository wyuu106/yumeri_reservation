from pydantic import BaseModel, ConfigDict
from datetime import date

class AdminCreate(BaseModel):
    name: str
    password: str

class AdminCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    name: str

class ClosedDateCreate(BaseModel):
    closed_date: date

class ClosedDateCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    closed_date: date