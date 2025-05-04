from fastapi import FastAPI, Depends
from . import database, models, crud, schemas

app = FastAPI()

@app.get("/hello", response_model=schemas.Message)
def hello():
    return {"message": "Hello from FastAPI!"}

@app.get("/items", response_model=list[schemas.Item])
def read_items(db=Depends(database.get_db)):
    return crud.get_items(db)