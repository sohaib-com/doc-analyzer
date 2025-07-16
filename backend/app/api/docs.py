from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud
import pdfplumber

router = APIRouter(prefix="/docs", tags=["docs"])

@router.post("/upload", response_model=UploadResp)
async def upload(background: BackgroundTasks, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if file.content_type not in ("application/pdf", "text/plain"):
        raise HTTPException(400, "Only PDF/TXT accepted")
    data = await file.read()
    if len(data) > 5*1024*1024:
        raise HTTPException(400, "Max 5MB")
    doc = await crud.create_document(db, file.filename, len(data))
    background.add_task(process_doc, doc.id, data, db.session)
    return {"file_id": doc.id}

async def process_doc(doc_id, data, session):
    from .deps import get_redis
    import asyncio
    db = session
    red = await get_redis()
    await crud.update_doc_progress(db, await db.get(models.Document, doc_id), "extracting", 10)
    text = data.decode(errors="ignore") if b"\n" in data[:100] else ""
    if not text:
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            text = "\n".join(p.page.extract_text() or "" for p in pdf.pages)
    await crud.update_doc_progress(db, db.get(models.Document, doc_id), "extracting", 50)
    await crud.save_extracted(db, db.get(models.Document, doc_id), text)
    await red.publish(str(doc_id), '{"stage":"ready","progress":100}')
