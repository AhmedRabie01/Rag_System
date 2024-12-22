from fastapi import FastAPI,APIRouter, Depends,UploadFile,status,Request
from fastapi.responses import JSONResponse
import os 
from helpers.config import get_settings,Settings
from controllers import DataController,ProjectController,ProcessController
import aiofiles
from   models import ResponseSignal
import logging
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunk


logger=logging.getLogger('uviconrn.error')

data_route = APIRouter(
prefix="/api/v1/data",
tags=['api_v1','data'],
)


@data_route.post("/upload/{project_id}")
async def upload_data(request:Request,project_id: str, file: UploadFile ,
                       app_settings: Settings =Depends(get_settings)):
    """
    Upload file to project directory
    """
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)

    project_model = await project_model.get_or_create_project(project_id=project_id)

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
            content={'signal': ResponseSignal.FILE_UPLOAD_FAILED.value
                      })
            
    return JSONResponse(
            # status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal':ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                 "file_id":file_id, 
                  "Project_id":project_id })



@data_route.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: str, process_request: ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_or_create_project(project_id=project_id)

    process_controller = ProcessController(project_id=project_id)

    file_content = process_controller.get_file_content(file_id=file_id)

    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.PROCESSING_FAILED.value}
        )

    file_chunks_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i + 1,
            chunk_project_id=project.id,
        )
        for i, chunk in enumerate(file_chunks)
    ]

    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

    if do_reset == 1:
        _ = await chunk_model.delete_chunks_by_project_id(project_id=project.id)


    no_records = await chunk_model.insert_many_chunks(chunks=file_chunks_records)

    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_records
        }
    )


