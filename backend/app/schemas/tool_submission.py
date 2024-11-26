from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ToolSubmissionBase(BaseModel):
    name: str
    description: str
    category: str
    condition: str

class ToolSubmissionCreate(ToolSubmissionBase):
    pass

class ToolSubmission(ToolSubmissionBase):
    id: int
    user_id: int
    status: str
    submitted_at: datetime
    user_name: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        orm_mode = True
