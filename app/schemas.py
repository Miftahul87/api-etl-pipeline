from datetime import datetime
from pydantic import BaseModel, ConfigDict
class TriggerResponse(BaseModel):
    run_id:int
    status:str
    message:str
class RunResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; status:str; started_at:datetime; finished_at:datetime|None
    extracted_count:int; loaded_count:int; rejected_count:int; error_message:str|None
class RecordResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; external_id:str; name:str; email:str|None; amount:float|None
    source_updated_at:str|None; payload:dict
