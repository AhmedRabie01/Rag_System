from fastapi import FastAPI,APIRouter, Depends,UploadFile,status
from fastapi.responses import JSONResponse
import os 
from helpers.config import get_settings,Settings
from controllers import DataController,ProjectController
import aiofiles
from   models import ResponseSignal
import logging

logger=logging.getLogger('uviconrn.error')

data_route = APIRouter(
prefix="/api/v1/data",
tags=['api_v1','data'],
)

@data_route.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile ,
                       app_settings: Settings =Depends(get_settings)):
    """
    Upload file to project directory
    """
    data_controller = DataController()
    is_valid,reult_signal = data_controller.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'signal': reult_signal})
           
        
    project_dir_path = ProjectController().get_projcet_path(project_id=project_id)
    file_path,file_id = data_controller.generate_unique_file_path(
        orig_file_name=file.filename,
        project_id=project_id
    )

    try:


        async with aiofiles.open(file_path, mode='wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
         logger.error(f"Error while uploading file: {e}")
         return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'signal': ResponseSignal.FILE_UPLOAD_FAILED.value})

    return JSONResponse(
            # status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal':ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                 "file_id":file_id })


 