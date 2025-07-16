import os
from fastapi import FastAPI
from .database import init_db
from .api.docs import router as docs_r
from .api.sse import router as sse_r
from .api.prompts import router as prompts_r
from .api.analyses import router as anal_r

app = FastAPI()

@app.on_event("startup")
async def on_start():
    await init_db()

app.include_router(docs_r)
app.include_router(sse_r)
app.include_router(prompts_r)
app.include_router(anal_r)
