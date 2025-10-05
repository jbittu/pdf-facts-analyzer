from pydantic import BaseModel
from typing import List

class Match(BaseModel):
    snippet: str
    page: int | None
    start_char: int | None
    end_char: int | None
    rationale: str

class PointerResult(BaseModel):
    pointer: str
    matches: List[Match]