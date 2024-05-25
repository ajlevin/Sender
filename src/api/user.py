from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
import math
from src import database as db

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(auth.get_api_key)],
)

class User(BaseModel):
    name: str
    email: str
    age: int


@router.post("/")
def create_user(new_profile: User):
    """
    Create New Climbing User 
    """
    insert_user_row = """
    INSERT INTO users (name, email, age) 
    VALUES(:profile_name, :profile_email, :profile_age) returning user_id
    """

    insert_user_dictionary ={
                                "profile_name": new_profile.name, 
                                "profile_email": new_profile.email,
                                "profile_age": new_profile.age
                            }

    try:
        with db.engine.begin() as connection:
            user_id = connection.execute(sqlalchemy.text(insert_user_row), insert_user_dictionary).scalar_one()
            
        return {
            "success": True,
            "user_id": user_id
            }
    
    except:
        return {"success": False}


@router.put("/user/{user_id}")
def update_user(user_id: int, altered_user: User):
    update_user_row = """
    UPDATE users 
    SET name = :updated_name, email = :updated_email, age = :updated_age 
    WHERE user_id = :user_id
    """

    update_user_dicitonary =    {
                                   "updated_name": altered_user.name,
                                   "updated_email": altered_user.email,
                                   "updated_age": altered_user.age,
                                   "user_id": user_id
                                }
    try:
        with db.engine.begin() as connection:
            connection.execute(sqlalchemy.text(update_user_row), update_user_dicitonary)
            
        return {"success": True}
    except:
        return {"success": False}


