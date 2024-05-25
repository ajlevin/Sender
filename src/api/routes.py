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
    last_lat = None
    last_lon = None

    with db.engine.begin() as connection:
        recent_user_routes = connection.execute(sqlalchemy.text(
            """
            SELECT routes.route_lat, routes.route_lon
            FROM routes
            INNER JOIN climbing ON routes.route_id = climbing.route_id
            WHERE climbing.user_id = :user_id
            ORDER BY climbing.created_at DESC
            LIMIT 1
            """),
            [{
                "user_id": user_id
            }])

        for route in recent_user_routes:
            last_lat = route.route_lan
            last_lon = route.route_lon

        if last_lat is None or last_lon is None:
            return recommended_routes

        suggested_routes = connection.execute(
            sqlalchemy.text(
                """
                SELECT *
                FROM routes
                ORDER BY ABS(route_lat - :last_lat) + ABS(route_lon - :last_lon) ASC
                LIMIT 30
                """),
                [{
                    "last_lat": last_lat,
                    "last_lon": last_lon,
                }])

        for row in suggested_routes:            
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