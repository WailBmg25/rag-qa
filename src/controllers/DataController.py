import re
from .BaseController import BaseController
from fastapi import UploadFile,status
from fastapi.responses import JSONResponse
from models import ResponseStatus
import os
import aiofiles
import logging
class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("uvicorn.error")

    def get_clean_filename(self, original_filename: str) -> str:
        # remove any special characters except underscores and .
        cleaned_filename = re.sub(r'[^\w.]', '', original_filename.strip())
        # replace spaces with underscores
        cleaned_filename = cleaned_filename.replace(' ', '_')
        return cleaned_filename

    def generate_unique_filename(self, original_filename: str, project_id: str) -> str:
        clean_filename = self.get_clean_filename(original_filename)
        project_dir = self.get_project_path(project_id)
        random_key = self.generate_random_string()
        new_file_path = os.path.join(project_dir, random_key + "_" + clean_filename)
        # Ensure the file path is unique
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_dir, random_key + "_" + clean_filename)
        return new_file_path, random_key + "_" + clean_filename

    async def validate_data(self, file: UploadFile, project_id: str):
        # Validate file properties
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": ResponseStatus.FILE_TYPE_NOT_SUPPORTED.value})
        if file.size > self.app_settings.FILE_MAX_SIZE:
            return False, JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": ResponseStatus.FILE_SIZE_EXCEEDED.value})

        file_path, file_name = self.generate_unique_filename(file.filename, project_id)
        try:
            # Save the file to the project directory
            async with aiofiles.open(file_path, 'wb') as out_file:
                while chunk := await file.read(self.app_settings.FILE_DEFAULT_CHUNK_SIZE):
                    await out_file.write(chunk)
        except Exception as e:
            self.logger.error(f"Error saving file {file.filename}: {e}")
            return False, JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": ResponseStatus.FILE_UPLOAD_FAILED.value})
        
        return True, JSONResponse(status_code=status.HTTP_200_OK, content={"message": ResponseStatus.FILE_UPLOAD_SUCCESS.value, "file_name": file_name})
