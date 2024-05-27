from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/routes",
    tags=["routes"],
    dependencies=[Depends(auth.get_api_key)],
)

GRADE_CONVERSION = {
    "5.0" : 0,
    "5.1" : 1,
    "5.2" : 1,
    "5.3" : 2,
    "5.4" : 2,
    "5.5" : 3,
    "5.6" : 4,
    "5.7" : 5,
    "5.8" : 6,
    "5.9" : 7,
    "5.10a" : 8,
    "5.10b" : 9,
    "5.10c" : 10,
    "5.10d" : 11,
    "5.11a" : 12,
    "5.11b" : 13,
    "5.11c" : 14,
    "5.11d" : 15,
    "5.12a" : 16,
    "5.12b" : 17,
    "5.12c" : 18,
    "5.12d" : 19,
    "5.13a" : 20,
    "5.13b" : 21,
    "5.13c" : 22,
    "5.13d" : 23,
    "5.14a" : 24,
    "5.14b" : 25,
    "5.14c" : 26,
    "5.14d" : 27,
    "5.15a" : 28,
    "5.15b" : 29,
    "5.15c" : 30,
    "5.15d" : 31,
}

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

    def fromCursorObject(cursorParams):
        return Route(
            route_name = cursorParams.name,
            location = cursorParams.location,
            yds = cursorParams.difficulty_level,
            trad = cursorParams.trad,
            sport = cursorParams.sport,
            other = cursorParams.other,
            description = cursorParams.description,
            protection = cursorParams.protection,
            route_lat = cursorParams.route_lat,
            route_lon = cursorParams.route_lon)


@router.get("/recommend")
def recommend_route(user_id: int):
    """
    Recommend Climbing Routes for A Specific User
    """
    recommended_routes = []
    user_route_record = []
    last_lat = None
    last_lon = None

    with db.engine.begin() as connection:
        recent_user_routes = connection.execute(sqlalchemy.text(
            """
            SELECT routes.route_lat, routes.route_lon, routes.trad, routes.sport, routes.other, routes.yds
            FROM routes
            INNER JOIN climbing ON routes.route_id = climbing.route_id
            WHERE climbing.user_id = :user_id
            ORDER BY climbing.created_at DESC
            LIMIT 30
            """),
            [{
                "user_id": user_id
            }])

        for route in recent_user_routes:            
            user_route_record.append(Route.fromCursorObject(route))

        if len(user_route_record) == 0:
            return recommended_routes  
        last_lat = user_route_record[0].route_lat
        last_lat = user_route_record[0].route_lat   

        suggested_routes = connection.execute(
            sqlalchemy.text(
                """
                WITH avgRouteRating AS (
                    SELECT route_id, AVG(rating) AS avgRating
                    FROM ratings
                    GROUP BY route_id
                    )
                SELECT *
                FROM routes
                INNER JOIN avgRouteRating ON avgRouteRating.route_id = routes.route_id
                WHERE routes.yds IN :user_grades
                ORDER BY ROUND(ABS(routes.route_lat - :last_lat) + ABS(routes.route_lon - :last_lon), 1) ASC, 
                    avgRouteRating.avgRating DESC
                LIMIT 30
                """),
                [{
                    "last_lat": last_lat,
                    "last_lon": last_lon,
                    "user_grades": (r.yds for r in user_route_record)
                }])

        for row in suggested_routes:            
            route_style = getRouteStyle(row)
            
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
    
def getRouteStyle(resultEntry):
    "Trad" if resultEntry.trad else "Sport" if resultEntry.sport else "Other" if resultEntry.other else "N/A"