from .BaseController import BaseController
import os
class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id: str):
        # Construct the project path based on the project ID
        project_dir = os.path.join(self.file_path, project_id)
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        return project_dir