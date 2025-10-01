from .BaseController import BaseController
from .ProjectController import ProjectController
from langchain.document_loaders import PyMuPDFLoader
from langchain.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum
import os

class ProcessController(BaseController):
     def __init__(self,project_id:str):
          super().__init__()
          self.project_id = project_id
          self.project_path = ProjectController().get_project_path(project_id)

     def get_file_extension(self,file_id: str) -> str:

          return file_id.split('.')[-1] if '.' in file_id else ''

     def get_file_loader(self,file_id: str):
          extension = self.get_file_extension(file_id)
          file_path = os.path.join(self.project_path, file_id)

          if extension == ProcessingEnum.PDF.value:
               return PyMuPDFLoader(file_path)
          if extension == ProcessingEnum.TEXT.value:
               return TextLoader(file_path, encoding='utf-8')
          return None

     def get_file_content(self, file_id: str):
          loader = self.get_file_loader(file_id)
          
          return loader.load() 
     def process_file_content(self, file_content:list, file_id:str, chunk_size:int=100, overlap_size:int=20):
          text_splitter = RecursiveCharacterTextSplitter(
               chunk_size=chunk_size,
               chunk_overlap=overlap_size,
               length_function=len,
          )
          file_content_text=[doc.page_content for doc in file_content]
          file_content_metadata=[doc.metadata for doc in file_content]
          chunks = text_splitter.create_documents(
               file_content_text,
               metadatas=file_content_metadata
          )
          return chunks