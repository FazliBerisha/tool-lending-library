from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class ToolSubmission(Base):
    __tablename__ = "tool_submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)
    condition = Column(String)
    image_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="tool_submissions")
