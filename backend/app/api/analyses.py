from fastapi import APIRouter, Depends, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas

router = APIRouter(prefix="/analysis", tags=["analysis"])
limiter = Limiter(key_func=get_remote_address)
router.state.limiter = limiter

@router.post("/", response_model=schemas.AnalyseOut)
@limiter.limit("10/minute")
async def analyze(req: schemas.AnalyseReq, db: AsyncSession = Depends(get_db)):
    doc = await db.get(models.Document, req.file_id)
    prompt = await db.get(models.PromptTemplate, req.prompt_id)
    if not doc or not prompt or not doc.extracted_text:
        raise HTTPException(400, "Invalid")
    final = prompt.prompt_text.replace("{document_content}", doc.extracted_text)
    resp = "<fake gemini response>"
    await crud.save_analysis(db, req.file_id, req.prompt_id, final, resp)
    return {"gemini_response": resp}
