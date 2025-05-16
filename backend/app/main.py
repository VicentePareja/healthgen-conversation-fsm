from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import database, models, crud, schemas
from .api.chat import router as chat_router

app = FastAPI()

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

@app.get("/hello", response_model=schemas.Message)
def hello():
    return {"message": "Hello from FastAPI!"}

@app.get("/items", response_model=list[schemas.Item])
def read_items(db=Depends(database.get_db)):
    return crud.get_items(db)