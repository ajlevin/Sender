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

class Profile(BaseModel):
    profile_name: str
    profile_email: str
    age: int


@router.post("/")
def create_user(new_profile: Profile):
    """
    Create New Climbing User 
    """
    insert_user_row = """
    INSERT INTO profile (name, email, age) 
    VALUES(:profile_name, :profile_email, :profile_age) returning profile_id
    """
    # Add Try Except To Ensure Row Was Actually Inserted.
    with db.engine.begin() as connection:
        user_id = connection.execute(sqlalchemy.text(insert_user_row), 
                                     {
                                      "profile_name": new_profile.profile_name, 
                                      "profile_email": new_profile.profile_email,
                                      "profile_age": new_profile.age
                                      }).scalar_one()

    return {
        "success": True,
        "user_id": user_id
        }

