from fastapi import FastAPI, APIRouter, Depends,UploadFile
from helpers.config import get_settings, Settings
from controllers import DataController

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["/api/v1/", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str,file: UploadFile, app_settings: Settings = Depends(get_settings)):
     # validate file properties
    is_valid, response = await DataController().validate_data(file,project_id)
    if not is_valid:
        return response
    return response