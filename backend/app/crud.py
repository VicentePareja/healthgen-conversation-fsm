# backend/app/crud.py

from sqlalchemy.orm import Session
from . import models

def get_items(db: Session):
    return db.query(models.Item).all()