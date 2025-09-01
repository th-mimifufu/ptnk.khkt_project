from typing import List
from fastapi import APIRouter, Request, HTTPException, Query
import asyncio
from pydantic import BaseModel

from src.core.config import settings
from src.services.l1.schema import UserInputL1, L1PredictResult

router = APIRouter(tags=["Gợi ý xét tuyển"])

@router.post("/predict/l1", response_model=List[L1PredictResult])
def predict_major_l1(user: UserInputL1, request: Request):
    if not user.is_tinh_tp_valid:
        return []
    return request.app.state.l1.predict(user)

# -------- BATCH L1 --------
class L1BatchRequest(BaseModel):
    items: List[UserInputL1]

@router.post("/predict/l1/batch", response_model=List[List[L1PredictResult]])
async def predict_major_l1_batch(
    payload: L1BatchRequest,
    request: Request,
    concurrency: int | None = Query(None, ge=1),
):
    items = payload.items
    if len(items) > settings.BATCH_MAX_ITEMS:
        raise HTTPException(413, f"Too many items; max={settings.BATCH_MAX_ITEMS}")

    limit = concurrency or settings.MAX_BATCH_CONCURRENCY
    sem = asyncio.Semaphore(limit)

    async def worker(idx: int, user: UserInputL1):
        if not user.is_tinh_tp_valid:
            return idx, []
        async with sem:
            res = await asyncio.to_thread(request.app.state.l1.predict, user)
            return idx, res

    results = await asyncio.gather(*[worker(i, u) for i, u in enumerate(items)])
    results.sort(key=lambda t: t[0])
    return [res for _, res in results]
