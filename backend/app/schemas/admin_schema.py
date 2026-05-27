from pydantic import BaseModel

class AdminCreate(BaseModel):
    name: str
    password: str

class AdminCreateResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True