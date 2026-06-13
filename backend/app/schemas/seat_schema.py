from pydantic import BaseModel, ConfigDict

class SeatCreate(BaseModel):
    name: str

class SeatCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

class SeatPatternCreate(BaseModel):
    name: str
    seat_type: str
    is_private: bool
    min_people: int
    max_people: int

class SeatPatternCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    seat_type: str
    is_private: bool
    min_people: int
    max_people: int

class PatternMemberCreate(BaseModel):
    pattern_id: int
    seat_id: int