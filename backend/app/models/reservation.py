from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Reservation(Base):
    """
    Represents a tool reservation in the database.
    
    Attributes:
        id (int): Primary key
        tool_id (int): Foreign key to the tool being reserved
        user_id (int): Foreign key to the user making the reservation
        start_date (DateTime): When the reservation begins
        end_date (DateTime): When the reservation ends
        status (str): Current status of the reservation (pending, approved, rejected, completed)
        created_at (DateTime): When the reservation was created
    """
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, ForeignKey("tools.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    tool = relationship("Tool", back_populates="reservations")
    user = relationship("User", back_populates="reservations")
