from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.tool_submission_service import ToolSubmissionService
from app.schemas.tool_submission import ToolSubmission, ToolSubmissionCreate
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ToolSubmission)
def submit_tool(
    submission: ToolSubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ToolSubmissionService.create_submission(db, submission, current_user.id)

@router.get("/pending", response_model=List[ToolSubmission])
def get_pending_submissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return ToolSubmissionService.get_pending_submissions(db)

@router.put("/{submission_id}/approve")
def approve_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    result = ToolSubmissionService.approve_submission(db, submission_id)
    if not result:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    return {"message": "Tool submission approved and tool created successfully"}

@router.put("/{submission_id}/reject")
def reject_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return ToolSubmissionService.reject_submission(db, submission_id)
