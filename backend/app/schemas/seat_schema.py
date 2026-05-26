from pydantic import BaseModel

class SeatData(BaseModel):
    people: int
    type: str