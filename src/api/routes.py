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
    location: str
    yds: str
    trad: bool
    sport: bool
    other: bool
    description: str
    protection: str
    route_lat: str
    route_lon: str
    
@router.get("/recommend")
def recommend_route(user_id: int):
    """
    Recommend Climbing Routes for A Specific User
    """
    recommended_routes = []
    user_locations = []

    with db.engine.begin() as connection:
        user_route_history = connection.execute(
            sqlalchemy.select(db.climbing_table).where(db.climbing_table.c.user_id == user_id)).fetchall()
        
        user_route_history = connection.execute(sqlalchemy.text(
            """
            SELECT routes.location
            FROM routes
            INNER JOIN climbing ON routes.route_id = climbing.route_id
            WHERE climbing.user_ud = :user_id
            ORDER BY routes.French
            """),
            [{
                "user_id": user_id
            }])
        
        for route in user_route_history:
            user_locations.append(route.location)    

        routes = connection.execute(
            sqlalchemy.select(db.routes_table).where(db.routes_table.c.location in user_locations)).fetchall()
    
        for row in routes:            
            route_style = [k for (k, v) in 
                           [("Trad", row.trad), ("Sport", row.sport), ("Other", row.other)] if v is True]

            
            recommended_routes.append(
                {
                "route_id" : row.route_id,
                "name": row.route_name,
                "location": row.location,
                "grade": row.yds,
                "style": route_style,
                "description": row.description
                }
            )
    return recommended_routes
    

@router.post("/add")
def create_route(new_route: Route):
    """
    Create New Climbing Route 
    """
    insert_route_row = """
    INSERT INTO routes (
        route_name, 
        location, 
        yds,
        trad,
        sport,
        other,
        description,
        protection,
        route_lat,
        route_lon
        ) 
    VALUES(
        :name, 
        :location, 
        :yds,
        :trad,
        :sport,
        :other,
        :description,
        :protection,
        :route_lat,
        :route_lon
        )
    RETURNING route_id
    """
    try:
        with db.engine.begin() as connection:
            insert_route_dictionary = {
                                        "name": new_route.route_name, 
                                        "location": new_route.location,
                                        "yds": new_route.yds,
                                        "trad": new_route.trad,
                                        "sport": new_route.sport,
                                        "other": new_route.other,
                                        "description": new_route.description,
                                        "protection": new_route.protection,
                                        "route_lat": new_route.route_lat,
                                        "route_lon": new_route.route_lon
                                        }

            route_id = connection.execute(sqlalchemy.text(insert_route_row), insert_route_dictionary).scalar_one()

        return {"success": True, "route_id": route_id}
    except:
        return {"success": False}