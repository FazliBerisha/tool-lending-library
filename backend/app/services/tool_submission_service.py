from sqlalchemy.orm import Session
from app.models.tool_submission import ToolSubmission
from app.schemas.tool_submission import ToolSubmissionCreate
from typing import List, Optional
from app.models.tool import Tool
from app.models.user import User

class ToolSubmissionService:
    @staticmethod
    def create_submission(db: Session, submission: ToolSubmissionCreate, user_id: int, image_url: Optional[str] = None):
        db_submission = ToolSubmission(
            name=submission.name,
            description=submission.description,
            category=submission.category,
            condition=submission.condition,
            user_id=user_id,
            image_url=image_url
        )
        db.add(db_submission)
        db.commit()
        db.refresh(db_submission)
        return db_submission

    @staticmethod
    def get_pending_submissions(db: Session) -> List[ToolSubmission]:
        submissions = db.query(ToolSubmission, User.username)\
            .join(User, ToolSubmission.user_id == User.id)\
            .filter(ToolSubmission.status == "pending")\
            .all()
        
        # Convert to dictionary and add username
        result = []
        for submission, username in submissions:
            submission_dict = {
                "id": submission.id,
                "name": submission.name,
                "description": submission.description,
                "category": submission.category,
                "condition": submission.condition,
                "user_id": submission.user_id,
                "status": submission.status,
                "submitted_at": submission.submitted_at,
                "user_name": username
            }
            result.append(submission_dict)
        
        return result

    @staticmethod
    def approve_submission(db: Session, submission_id: int):
        submission = db.query(ToolSubmission).filter(ToolSubmission.id == submission_id).first()
        if submission:
            new_tool = Tool(
                name=submission.name,
                description=submission.description,
                category=submission.category,
                condition=submission.condition,
                owner_id=submission.user_id,
                is_available=True,
                image_url=submission.image_url
            )
            try:
                db.add(new_tool)
                submission.status = "approved"
                db.commit()
                db.refresh(submission)
                db.refresh(new_tool)
                print(f"Tool created with image URL: {new_tool.image_url}")
            except Exception as e:
                print(f"Error approving submission: {str(e)}")
                db.rollback()
                raise
                
            return submission
        return None

    @staticmethod
    def reject_submission(db: Session, submission_id: int):
        submission = db.query(ToolSubmission).filter(ToolSubmission.id == submission_id).first()
        if submission:
            submission.status = "rejected"
            db.commit()
            db.refresh(submission)
        return submission
