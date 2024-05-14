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
    YDS: str
    Font: str
    French: str
    Ewbanks: str
    UIAA: str
    ZA: str
    British: str
    yds_aid: str
    boulder: bool
    tr: bool
    ice: bool
    trad: bool
    sport: bool
    aid: bool
    mixed: bool
    snow: bool
    alpine: bool
    fa: str
    description: str
    protection: str
    
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
                           [("Boulder", row.boulder), ("TD", row.td), ("Ice", row.ice), ("Trad", row.trad), ("Sport", row.sport), 
                            ("Aid", row.aid), ("Mixed", row.mixed), ("Snow", row.snow), ("Alpine", row.alpine)] if v is True]

            
            recommended_routes.append(
                {
                "route_id" : row.route_id,
                "name": row.route_name,
                "location": row.location,
                "grade": row.French,
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
        route_id,
        route_name, 
        location, 
        YDS,
        Font,
        French,
        Ewbanks,
        UIAA,
        ZA,
        British,
        yds_aid,
        boulder,
        tr,
        ice,
        trad,
        sport,
        aid,
        mixed,
        snow,
        alpine,
        fa,
        description,
        protection
        ) 
    VALUES(
        :route_id,
        :name, 
        :location, 
        :YDS,
        :Font,
        :French,
        :Ewbanks,
        :UIAA,
        :ZA,
        :British,
        :yds_aid,
        :boulder,
        :tr,
        :ice,
        :trad,
        :sport,
        :aid,
        :mixed,
        :snow,
        :alpine,
        :fa,
        :description,
        :protection
        )
    """

    get_max_route_id_query = """
    SELECT MAX(route_id) AS max_route_id FROM routes
    """


    try:
        with db.engine.begin() as connection:
            max_route_id = connection.execute(sqlalchemy.text(get_max_route_id_query)).fetchone()
            route_id = max_route_id.max_route_id

            new_route = connection.execute(sqlalchemy.text(insert_route_row), 
                                        {
                                        "route_id": route_id + 1,
                                        "name": new_route.route_name, 
                                        "location": new_route.location,
                                        "YDS": new_route.YDS,
                                        "Font": new_route.Font,
                                        "French": new_route.French,
                                        "Ewbanks": new_route.Ewbanks,
                                        "UIAA": new_route.UIAA,
                                        "ZA": new_route.ZA,
                                        "British": new_route.British,
                                        "yds_aid": new_route.yds_aid,
                                        "boulder": new_route.boulder,
                                        "tr": new_route.tr,
                                        "ice": new_route.ice,
                                        "trad": new_route.trad,
                                        "sport": new_route.sport,
                                        "aid": new_route.aid,
                                        "mixed": new_route.mixed,
                                        "snow": new_route.snow,
                                        "alpine": new_route.alpine,
                                        "fa": new_route.fa,
                                        "description": new_route.description,
                                        "protection": new_route.protection
                                        })
        return {
            "success": True,
            "route_id": route_id + 1
            }
    
    except Exception as e:
        return {"success": False, "error_message": str(e)}