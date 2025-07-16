import uuid
from sqlalchemy import Column, String, Integer, Text, JSON, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    upload_time = Column(TIMESTAMP, server_default=func.now())
    status = Column(String, default="uploaded")
    current_stage = Column(String)
    progress = Column(Integer, default=0)
    extracted_text = Column(Text)
class PromptTemplate(Base):
    __tablename__ = "prompt_templates"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    prompt_text = Column(Text, nullable=False)
class AIAnalysis(Base):
    __tablename__ = "ai_analyses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    prompt_template_id = Column(UUID(as_uuid=True), ForeignKey("prompt_templates.id"))
    final_prompt = Column(Text, nullable=False)
    gemini_response = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
