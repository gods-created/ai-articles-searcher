from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from validators import FetchNewsData

from modules import FetchNews

fetch_news = APIRouter(
    prefix='/api',
    tags=['API']
)

@fetch_news.post('/fetch_news', name='Fetch news', status_code=200)
async def _fetch_news(r: Request, data: FetchNewsData):
    async with FetchNews() as module:
        response_json = await module._executing(data.to_json())
        
    return JSONResponse(
        content=response_json
    )
