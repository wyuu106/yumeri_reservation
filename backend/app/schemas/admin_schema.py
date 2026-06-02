from pydantic import BaseModel, ConfigDict

class AdminCreate(BaseModel):
    name: str
    password: str

class AdminCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    name: str