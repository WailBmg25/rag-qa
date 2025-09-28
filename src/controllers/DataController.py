import re
from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseStatus
import os
class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def get_clean_filename(self, original_filename: str) -> str:
        # remove any special characters except underscores and .
        cleaned_filename = re.sub(r'[^\w.]', '', original_filename.strip())
        # replace spaces with underscores
        cleaned_filename = cleaned_filename.replace(' ', '_')
        return cleaned_filename

    def generate_unique_filename(self, original_filename: str, project_id: str) -> str:
        clean_filename = self.get_clean_filename(original_filename)
        project_dir = ProjectController().get_project_path(project_id)
        random_key = self.generate_random_string()
        #New file path with random key prefix
        new_file_path = os.path.join(project_dir, random_key + "_" + clean_filename)
        # Ensure the file path is unique
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_dir, random_key + "_" + clean_filename)
        return new_file_path, random_key + "_" + clean_filename

    async def validate_data(self, file: UploadFile, project_id: str):
        # Validate file properties
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseStatus.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE:
            return False, ResponseStatus.FILE_SIZE_EXCEEDED.value        
        return True, ResponseStatus.FILE_VALIDATION_SUCCESS.value