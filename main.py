from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
import uvicorn

from routers import *

app = FastAPI(
    title='Application',
    version='0.0.1',
    redoc_url=None
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(r: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            'detail': exc.errors()
        })
    )

app.include_router(
    fetch_news
)

app.include_router(
    categorize_news
)

app.include_router(
    similar_articles
)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8001, reload=True)
