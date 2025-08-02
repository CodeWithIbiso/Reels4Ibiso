from pydantic import BaseModel
from typing import Optional

class PracticeBase(BaseModel):
    name: str
    address: str

class PracticeCreate(PracticeBase):
    pass

class PracticeInDB(PracticeBase):
    id: Optional[str]

class PracticeResponse(PracticeInDB):
    pass