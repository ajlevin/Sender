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
    try:
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
    except Exception as e:
        return {"success": False, "error_message": str(e)}


@router.put("/AlterProfile/{user_id}")
def update_user(user_id: int, altered_profile: Profile):
    update_user_row = """
    UPDATE profile 
    SET name = :updated_name, email = :updated_email, age = :updated_age 
    WHERE profile_id = :user_id
    """
    try:
        with db.engine.begin() as connection:
            connection.execute(sqlalchemy.text(update_user_row),
                               {
                                   "updated_name": altered_profile.profile_name,
                                   "updated_email": altered_profile.profile_email,
                                   "updated_age": altered_profile.age,
                                   "user_id": user_id
                               })
        return {"success": True}
    
    except Exception as e:
        return {"success": False, "error_message": str(e)}


