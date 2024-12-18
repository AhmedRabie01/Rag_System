from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re 
import os

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale= 1048576

    def validate_uploaded_file(self,file):
        # Implement validation logic here
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False,ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False,ResponseSignal.FILE_SIZE_EXCEEDS.value
        return True,ResponseSignal.FILE_UPLOAD_SUCCESS.value
    
    def generate_unique_filename(self, orig_file_name: str, project_id: str):
        random_key = self.generate_random_string()
        project_path = ProjectController().get_projcet_path(project_id=project_id)
        clean_file_name = self.get_clean_filename(orig_file_name=orig_file_name)
    
        # Proper usage of os.path.join
        new_file_path = os.path.join(
            project_path,
            f"{random_key}_{clean_file_name}"
        )
    
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                f"{random_key}_{clean_file_name}"
            )
        
        return new_file_path


    def get_clean_filename(self,orig_file_name:str):
        clean_file_name = re.sub(r'[^\w.]','',orig_file_name.strip())
        cleaned_filename = clean_file_name.replace("","_")
        return cleaned_filename