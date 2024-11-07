from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from validators import CategorizeNewsData

from modules import SimilarArticles

similar_articles = APIRouter(
    prefix='/api',
    tags=['API']
)

@similar_articles.get('/similar_articles', name='Similar articles', status_code=200)
async def _similar_articles(r: Request, text: str = Query(...)):
    async with SimilarArticles() as module:
        response_json = await module._executing(text)
        
    return JSONResponse(
        content=response_json
    )
