from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.services.tool_submission_service import ToolSubmissionService
from app.schemas.tool_submission import ToolSubmission, ToolSubmissionCreate
from app.core.deps import get_current_user
from app.models.user import User
from app.services.file_service import FileService

router = APIRouter()

@router.post("/")
async def create_tool_submission(
    name: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    condition: str = Form(...),
    image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Handle image upload if provided
        image_url = None
        if image:
            try:
                image_url = await FileService.save_upload(image, "tool-images")
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error uploading image: {str(e)}"
                )

        submission_data = ToolSubmissionCreate(
            name=name,
            description=description,
            category=category,
            condition=condition
        )
        
        submission = ToolSubmissionService.create_submission(
            db=db,
            submission=submission_data,
            user_id=current_user.id,
            image_url=image_url
        )
        
        return submission
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error creating submission: {str(e)}")  # Add this for debugging
        raise HTTPException(status_code=400, detail=str(e))

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
