from pydantic import BaseModel
from uuid import UUID

class UploadResp(BaseModel):
    file_id: UUID

class PromptTemplateCreate(BaseModel):
    name: str
    prompt_text: str

class PromptTemplateOut(BaseModel):
    id: UUID
    name: str
    prompt_text: str

    class Config:
        orm_mode = True

class AnalyseReq(BaseModel):
    file_id: UUID
    prompt_id: UUID

class AnalyseOut(BaseModel):
    gemini_response: str
