from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from enum import Enum
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

class search_sort_options(str, Enum):
    route_name = "route_name"
    location = "location"
    created_at = "created_at"
    

class search_sort_order(str, Enum):
    asc = "asc"
    desc = "desc"  

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

def getRouteStyle(resultEntry):
    "Trad" if resultEntry.trad else "Sport" if resultEntry.sport else "Other" if resultEntry.other else "N/A"

@router.get("/view")
def get_routes(
    route_name: str = "",
    yds: str = "",
    location: str = "",
    search_page: str = "",
    sort_col: search_sort_options = search_sort_options.timestamp,
    sort_order: search_sort_order = search_sort_order.desc
    ):
    """
    Recommend Climbing Routes for A Specific User
    """

    with db.engine.begin() as connection:        
        metadata_obj = sqlalchemy.MetaData()
        routes = sqlalchemy.Table('routes', metadata_obj, autoload_with= db.engine)
        ratings = sqlalchemy.Table('ratings', metadata_obj, autoload_with= db.engine)

        avgRouteRatings = sqlalchemy.select(
            ratings.route_id,
            sqlalchemy.sql.func.avg(ratings.rating).label('avgRating')
        ).select_from(
            ratings
        ).group_by(
            ratings.route_id
        )

        search_result = sqlalchemy.select(
            routes.c.route_id,
            routes.c.yds,
            routes.c.description,
            routes.c.location,
            routes.c.created_at,
            routes.c.route_name,
            routes.c.route_lat,
            routes.c.route_lon,
            ratings.c.avgRating
        ).select_from(
            routes.join(avgRouteRatings, avgRouteRatings.c.route_id == routes.c.route_id)
        )

        if sort_col is search_sort_options.route_name:
            sort_parameter = search_result.c.route_name
        elif sort_col is search_sort_options.location:
            sort_parameter = search_result.c.location
        elif sort_col is search_sort_options.created_at:
            sort_parameter = search_result.c.created_at
        else:
            raise RuntimeError("No Sort Parameter Passed")
        
        search_values = (
            sqlalchemy.select(
                search_result.c.route_id,
                search_result.c.yds,
                search_result.c.description,
                search_result.c.location,
                search_result.c.created_at,
                search_result.c.route_name,
                search_result.c.route_lat,
                search_result.c.route_lon,
                search_result.c.avgRating
            ).select_from(search_result)
        )

        sorted_values = search_values
        if route_name != "":
            sorted_values = sorted_values.where(
                (search_result.c.route_name.ilike(f"%{route_name}%")))
        if yds != "":
            sorted_values = sorted_values.where(
                (search_result.c.yds.ilike(f"%{yds}%")))
        if location != "":
            sorted_values = sorted_values.where(
                (search_result.c.location.ilike(f"%{location}%")))
        
        if sort_order == search_sort_order.desc: 
            sorted_values = sorted_values.order_by(
                sqlalchemy.desc(sort_parameter) if sort_order == search_sort_order.desc else sqlalchemy.desc(sort_parameter))

        page = 0 if search_page == "" else int(search_page) * 10
        result = connection.execute(search_values.limit(10).offset(page))
        search_return = []
        for row in result:
            search_return.append(
                    {
                        "route_id": row.route_id,
                        "yds": row.yds,
                        "description": row.description,
                        "location": row.location,
                        "created_at": row.created_at,
                        "route_name": row.route_name,
                        "route_lat": row.route_lat,
                        "route_lon": row.route_lon,
                        "avgRating": row.avgRating
                    })
        
        prev_page = f"{int(page/10) - 1}" if int(page/10) >= 1 else ""
        next_page = f"{int(page/10) + 1}" if (connection.execute(search_values).rowcount - (page)) > 0 else ""
    
        return ({
                "previous": prev_page,
                "next": next_page,
                "results": search_return
            })

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
    