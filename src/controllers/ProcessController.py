from .BaseController import BaseController
from langchain.document_loaders import PyMuPDFLoader
from langchain.document_loaders import TextLoader
from models import ProcessingEnum
import os

class ProcessController(BaseController):
     def __init__(self,project_id:str):
          super().__init__()
          self.project_id = project_id
          self.project_path = self.get_project_path(project_id)

     def get_file_extension(self,file_id: str) -> str:

          return file_id.split('.')[-1] if '.' in file_id else ''

     def get_file_loader(self,file_id: str):
          extension = self.get_file_extension(file_id)
          file_path = os.path.join(self.project_path, file_id)

          if extension == ProcessingEnum.PDF.value:
               return PyMuPDFLoader(file_path)
          elif extension == ProcessingEnum.TEXT.value:
               return TextLoader(file_path, encoding='utf-8')
          return None

     def get_file_content(self, file_id: str):
          loader = self.get_file_loader(file_id)
          
          return loader.load() 
     