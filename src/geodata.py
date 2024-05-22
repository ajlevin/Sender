import geopandas as gpd
from shapely.geometry import Point
from src import database as db
import sqlalchemy

# Load state boundaries
states = gpd.read_file('src/tl_2023_us_state.shp')

# Function to get state name from longitude and latitude
def get_state(lon, lat):
    point = Point(lon, lat)
    for _, state in states.iterrows():
        if state['geometry'].contains(point):
            return state['NAME']
    return None


# Fetch routes with longitude and latitude
with db.engine.connect() as connection:
    result = connection.execute(sqlalchemy.text("""SELECT route_id, longitude, latitude 
                                                FROM routes 
                                                WHERE longitude IS NOT NULL AND latitude IS NOT NULL"""))
    routes = result.fetchall()

# Map each route to a state and insert into route_states table
with db.engine.begin() as connection:
    for route in routes:
        state_name = get_state(route.longitude, route.latitude)
        if state_name:
            connection.execute(sqlalchemy.text("""INSERT INTO route_states
                                                (route_id, state_name) 
                                               VALUES (:route_id, :state_name)"""),
                               {"route_id": route.route_id, "state_name": state_name})
