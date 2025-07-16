from sqlalchemy.future import select
from . import models

async def create_document(db, filename, size):
    doc = models.Document(filename=filename, file_size=size, status="uploaded", progress=0)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc

async def update_doc_progress(db, doc, stage, progress):
    doc.current_stage = stage
    doc.progress = progress
    await db.commit()

async def save_extracted(db, doc, text):
    doc.extracted_text = text
    doc.status = "ready"
    doc.progress = 100
    await db.commit()
async def list_prompts(db):
    res = await db.execute(select(models.PromptTemplate))
    return res.scalars().all()

async def create_prompt(db, data):
    p = models.PromptTemplate(**data.dict())
    db.add(p)
    await db.commit()
    await db.refresh(p)
    return p
async def save_analysis(db, doc_id, prompt_id, final_prompt, resp):
    from .models import AIAnalysis
    a = AIAnalysis(document_id=doc_id, prompt_template_id=prompt_id,
                   final_prompt=final_prompt, gemini_response=resp)
    db.add(a)
    await db.commit()
    return a
