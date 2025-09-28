from fastapi import FastAPI, APIRouter, Depends,UploadFile, status
from fastapi.responses import JSONResponse
from helpers import get_settings, Settings
from controllers import DataController, ProjectController
from models.enums.ResponseEnums import ResponseStatus
import aiofiles
import logging
from .schemas import DataRequest

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["/api/v1/", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str,file: UploadFile, app_settings: Settings = Depends(get_settings)):
    data_controller = DataController()
     # validate file properties
    is_valid, response = await data_controller.validate_data(file,project_id)
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": response})
    #1 Generate a unique filename and path
    file_path, file_id = data_controller.generate_unique_filename(file.filename, project_id)

    try:
            #2 Save the file to the project directory
            async with aiofiles.open(file_path, 'wb') as out_file:
                while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                    await out_file.write(chunk)
    except Exception as e:
        logger.error(f"Error uploading file {file.filename}: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": ResponseStatus.FILE_UPLOAD_FAILED.value})
        
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": ResponseStatus.FILE_UPLOAD_SUCCESS.value, "file_id": file_id})


@data_router.post("/proces s/{project_id}")
async def process_data(project_id: str, data_request: DataRequest):
    # Process the data using the provided DataRequest schema
    file_id = data_request.file_id
    return file_id
