from typing import List, Union
from pydantic import BaseModel

class Entry(BaseModel):
    id: int
    session_id: int
    recording_id: Union[None,str]
    tag: str
    value: float
    timestamp: float

    class Config:
        orm_mode = True

class EntriesForTag:
    tag: str
    results: List[Entry]

class GraphingSession:
    id: int
    name: str
    data: str

    class Config:
        orm_mode = True