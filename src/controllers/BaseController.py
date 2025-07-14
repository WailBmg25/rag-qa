from helpers.config import Settings, get_settings
import os
import random
import string
class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_path = os.path.dirname(os.path.dirname(__file__))
        self.file_path = os.path.join(self.base_path, 'assets/files')
    def get_project_path(self, project_id: str) :
        # Construct the project path based on the project ID
        project_dir = os.path.join(self.file_path, project_id)
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        return project_dir
    def generate_random_string(self, length: int = 14) -> str:
        # Generate a random string of fixed length
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))