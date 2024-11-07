from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from validators import CategorizeNewsData

from modules import CategorizeNews

categorize_news = APIRouter(
    prefix='/api',
    tags=['API']
)

@categorize_news.post('/categorize_news', name='Categorize news', status_code=200)
async def _categorize_news(r: Request, data: CategorizeNewsData):
    async with CategorizeNews() as module:
        response_json = await module._executing(data.to_json())
        
    return JSONResponse(
        content=response_json
    )
