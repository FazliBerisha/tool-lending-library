from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, ForeignKey("tools.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    reservation_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)

    tool = relationship("Tool", back_populates="reservations") # For tool
    user = relationship("User", back_populates="reservations") # For user 