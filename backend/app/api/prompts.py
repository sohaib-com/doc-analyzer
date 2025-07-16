from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas
router = APIRouter(prefix="/prompts", tags=["prompts"])

@router.get("/", response_model=list[schemas.PromptTemplateOut])
async def list_prompts(db: AsyncSession = Depends(get_db)):
    return await crud.list_prompts(db)

@router.post("/", response_model=schemas.PromptTemplateOut)
async def create_prompt(data: schemas.PromptTemplateCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_prompt(db, data)
