import uvicorn
from fastapi import FastAPI

from app.routes.notes import notes_router


app = FastAPI()
app.include_router(notes_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1',
                port=8080, reload=True)