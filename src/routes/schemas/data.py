from typing import Optional
from pydantic import BaseModel

class DataRequest(BaseModel):

     file_id: str
     chunk_size: Optional[int] = 120
     overlap_size: Optional[int] = 20
     do_reset: Optional[bool] = False