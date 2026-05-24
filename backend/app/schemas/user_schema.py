from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    password: str

class UserCreateResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True