from fastapi import FastAPI,APIRouter, Depends,UploadFile,status
from fastapi.responses import JSONResponse
import os 
from helpers.config import get_settings,Settings
from controllers import DataController,ProjectController,ProcessController 
import aiofiles
from   models import ResponseSignal
import logging
from .schemes.data import ProcessRequest

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
                 "file_id":file_id ,
                 "file_path":file_path})



@data_route.post("/process/{project_id}")
async def process_endpoint(project_id:str,process_request: ProcessRequest):
   file_id = process_request.file_id
   chunk_size = process_request.chunk_size
   overlap_size = process_request.overlap_size


   process_controller = ProcessController(projcet_id=project_id)
   file_content = process_controller.get_file_content(file_id)
   file_chunks = process_controller.process_file_content(
       file_content=file_content,
       file_id=file_id,
       chunk_size=chunk_size,
       overlap_size=overlap_size)
   
   if file_chunks is None or len(file_chunks) ==0:
       return JSONResponse(status_code =  status.HTTP_400_BAD_REQUEST,
       content={'signal': ResponseSignal.PROCESSING_FAILED.value})

   return file_chunks