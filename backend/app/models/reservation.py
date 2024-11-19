from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(Integer, ForeignKey("tools.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reservation_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    is_checked_out = Column(Boolean, default=False)

    tool = relationship("Tool", back_populates="reservations")
    user = relationship("User", back_populates="reservations")