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
    
@router.post("/")
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