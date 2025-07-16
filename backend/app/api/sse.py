from fastapi import APIRouter
from starlette.responses import StreamingResponse
from .deps import get_redis

router = APIRouter(prefix="/stream", tags=["sse"])

@router.get("/{file_id}")
async def sse(file_id: str):
    async def event_gen():
        r = await get_redis()
        pub = r.pubsub()
        await pub.subscribe(file_id)
        async for msg in pub.listen():
            if msg["type"] == "message":
                yield f"data: {msg['data'].decode()}\n\n"
    return StreamingResponse(event_gen(), media_type="text/event-stream")
