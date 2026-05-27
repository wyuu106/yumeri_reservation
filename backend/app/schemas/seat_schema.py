from pydantic import BaseModel

class SeatCreate(BaseModel):
    id: int
    name: str

class SeatPatternCreate(BaseModel):
    id: int
    name: str
    seat_type: str
    is_private: bool
    min_people: int
    max_people: int

class PatternMemberCreate(BaseModel):
    pattern_id: int
    seat_id: int