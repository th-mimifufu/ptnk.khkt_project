from typing import List
from fastapi import APIRouter, Request, HTTPException, Query
import asyncio
from pydantic import BaseModel

from src.core.config import settings
from src.services.l2.schema import UserInputL2, L2PredictResult

router = APIRouter(tags=["Gợi ý xét tuyển"])

@router.post("/predict/l2", response_model=List[L2PredictResult])
def predict_major_l2(user: UserInputL2, request: Request):
    if not user.is_tinh_tp_valid:
        return []
    return request.app.state.l2.predict(user)

# -------- BATCH L2 --------
class L2BatchRequest(BaseModel):
    items: List[UserInputL2]

@router.post("/predict/l2/batch", response_model=List[List[L2PredictResult]])
async def predict_major_l2_batch(
    payload: L2BatchRequest,
    request: Request,
    concurrency: int | None = Query(None, ge=1, description="override mức đồng thời"),
):
    items = payload.items
    if len(items) > settings.BATCH_MAX_ITEMS:
        raise HTTPException(413, f"Too many items; max={settings.BATCH_MAX_ITEMS}")

    limit = concurrency or settings.MAX_BATCH_CONCURRENCY
    sem = asyncio.Semaphore(limit)

    async def worker(idx: int, user: UserInputL2):
        if not user.is_tinh_tp_valid:
            return idx, []
        async with sem:
            # chạy predict sync trong thread pool
            res = await asyncio.to_thread(request.app.state.l2.predict, user)
            return idx, res

    tasks = [worker(i, u) for i, u in enumerate(items)]
    done = await asyncio.gather(*tasks)
    done.sort(key=lambda t: t[0]) 
    return [res for _, res in done]
