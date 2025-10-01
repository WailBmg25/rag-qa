from enum import Enum
class ResponseStatus(Enum):
     FILE_VALIDATION_SUCCESS = "File validated successfully"
     FILE_TYPE_NOT_SUPPORTED = "File type not supported"
     FILE_SIZE_EXCEEDED = "File size exceeded the limit"
     FILE_UPLOAD_FAILED = "File upload failed"
     FILE_UPLOAD_SUCCESS = "File uploaded successfully"
     FILE_PROCESSING_FAILED = "File processing failed"
     FILE_PROCESSING_SUCCESS = "File processed successfully"