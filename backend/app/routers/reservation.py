from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.tool_service import ToolService
from app.services.reservation_service import ReservationService
from app.schemas.tool import Tool, ToolCreate
from app.schemas.reservation import Reservation, ReservationCreate
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/reserve", response_model=Reservation, status_code=status.HTTP_201_CREATED)
def reserve_tool(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint to create a reservation for a tool.
    """
    tool = ToolService.get_tool(db, reservation.tool_id)
    if not tool or not tool.is_available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tool not available for reservation")
    
    new_reservation = ReservationService.create_reservation(db, reservation, current_user.id)
    ToolService.update_tool_availability(db, reservation.tool_id, False)
    return new_reservation

@router.post("/checkout/{tool_id}", status_code=status.HTTP_200_OK)
def check_out_tool(tool_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Endpoint to check out a tool.
    """
    reservation = ReservationService.get_active_reservation(db, tool_id, current_user.id)
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active reservation found")
    
    ToolService.update_tool_availability(db, tool_id, False)
    return {"msg": f"Tool '{tool_id}' checked out successfully"}

@router.post("/return/{tool_id}", status_code=status.HTTP_200_OK)
def return_tool(tool_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Endpoint to return a tool.
    """
    reservation = ReservationService.get_active_reservation(db, tool_id, current_user.id)
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active reservation found")
    
    ToolService.update_tool_availability(db, tool_id, True)
    reservation.is_active = False
    db.commit()
    return {"msg": f"Tool '{tool_id}' returned successfully"}
