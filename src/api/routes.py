from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
import math
from src import database as db

router = APIRouter(
    prefix="/routes",
    tags=["routes"],
    dependencies=[Depends(auth.get_api_key)],
)

class Route(BaseModel):
    route_name: str
    route_location: str
    difficulty_level: int
    style: str
    
@router.post("/")
def create_route(new_route: Route):
    """
    Create New Climbing Route 
    """
    insert_route_row = """
    INSERT INTO routes (name, location, difficulty_level, style) 
    VALUES(:name, :location, :difficulty_level, :style)
    """
    try:
        with db.engine.begin() as connection:
            new_route = connection.execute(sqlalchemy.text(insert_route_row), 
                                        {
                                        "name": new_route.route_name, 
                                        "location": new_route.route_location,
                                        "difficulty_level": new_route.difficulty_level,
                                        "style": new_route.style
                                        })
        return {
            "success": True,
            }
    
    except Exception as e:
        return {"success": False, "error_message": str(e)}