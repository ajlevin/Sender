from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
import math
from src import database as db

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/create")
def create_user():
    """ """
    
    return "1"

