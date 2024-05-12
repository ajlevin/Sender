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
    INSERT INTO users (user_id, name, email, age) 
    VALUES(:user_id, :profile_name, :profile_email, :profile_age) returning user_id
    """

    get_max_user_id_query = """
    SELECT MAX(user_id) AS max_user_id FROM users
    """

    try:
        with db.engine.begin() as connection:
            max_user_id = connection.execute(sqlalchemy.text(get_max_user_id_query)).fetchone()
            user_id = max_user_id.max_user_id
            
            user_insert = connection.execute(sqlalchemy.text(insert_user_row), 
                                        {
                                        "user_id": user_id + 1,
                                        "profile_name": new_profile.name, 
                                        "profile_email": new_profile.email,
                                        "profile_age": new_profile.age
                                        })
            

        return {
            "success": True,
            "user_id": user_id + 1
            }
    except Exception as e:
        return {"success": False, "error_message": str(e)}


@router.put("/user/{user_id}")
def update_user(user_id: int, altered_user: User):
    update_user_row = """
    UPDATE users 
    SET name = :updated_name, email = :updated_email, age = :updated_age 
    WHERE user_id = :user_id
    """
    try:
        with db.engine.begin() as connection:
            connection.execute(sqlalchemy.text(update_user_row),
                               {
                                   "updated_name": altered_user.name,
                                   "updated_email": altered_user.email,
                                   "updated_age": altered_user.age,
                                   "user_id": user_id
                               })
        return {"success": True}
    
    except Exception as e:
        return {"success": False, "error_message": str(e)}


