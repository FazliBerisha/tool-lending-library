import os
import uuid
from fastapi import UploadFile
from pathlib import Path

class FileService:
    UPLOAD_DIR = Path("uploads")
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".jfif", ".webp", ".bmp"}

    @classmethod
    async def save_upload(cls, file: UploadFile, subfolder: str = "") -> str:
        try:
            print(f"Saving file: {file.filename} to {subfolder}")
            
            # Create upload directory if it doesn't exist
            upload_path = cls.UPLOAD_DIR / subfolder
            upload_path.mkdir(parents=True, exist_ok=True)

            # Generate unique filename
            ext = Path(file.filename).suffix.lower()
            if ext not in cls.ALLOWED_EXTENSIONS:
                raise ValueError(
                    f"Invalid file type: {ext}. Allowed types: {', '.join(cls.ALLOWED_EXTENSIONS)}"
                )

            # Convert JFIF to JPG for better compatibility
            if ext == '.jfif':
                ext = '.jpg'

            filename = f"{uuid.uuid4()}{ext}"
            file_path = upload_path / filename

            # Save file
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)

            print(f"File saved successfully: {file_path}")
            return f"http://localhost:8000/uploads/{subfolder}/{filename}"
            
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            raise
