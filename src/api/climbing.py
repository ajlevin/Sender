from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/climbing",
    tags=["climbing"],
    dependencies=[Depends(auth.get_api_key)],
)

class Climb(BaseModel):
    user_id: int
    route_id: int
    frequency: int 
    intensity: int
    heart_rate: int
    systolic_pressure: int
    diastolic_pressure: int


@router.post("/climb_log")
def create_climb_log(log_entry: Climb):
    """
    Create New Climb Log Entry For A User
    """

    insert_climb_row = """
    INSERT INTO climbing (user_id, route_id, frequency, intensity, heart_rate, systolic_pressure, diastolic_pressure) 
    VALUES(:user_id, :route_id, :frequency, :intensity, :heart_rate, :systolic_pressure, :diastolic_pressure)
    """
    try:
        climb_row_dictionary =      {
                                        "user_id": log_entry.user_id, 
                                        "route_id": log_entry.route_id,
                                        "frequency": log_entry.frequency,
                                        "intensity": log_entry.intensity, 
                                        "heart_rate": log_entry.heart_rate,
                                        "systolic_pressure": log_entry.systolic_pressure,
                                        "diastolic_pressure": log_entry.diastolic_pressure
                                    }

        with db.engine.begin() as connection:
            connection.execute(sqlalchemy.text(insert_climb_row), climb_row_dictionary)

        return {"success": True}
    except:
        return {"success": False}
    

@router.get("/history/{user_id}")
def get_user_history(user_id: int):
    """
    Returns All Previous Climbs Performed By User
    """

    All_Climbs = []

    with db.engine.begin() as connection:
        # Select All Appropriate Rows
        result = connection.execute(
        sqlalchemy.select(db.climbing_table).where(db.climbing_table.c.user_id == user_id)
        ).fetchall()

        for row in result:
            user_climb =  {
                            'date': row.created_at,
                            'route_id': row.route_id,
                            'frequency': row.frequency,
                            'intensity': row.intensity,
                            'heart_rate': row.heart_rate,
                            'systolic_pressure': row.systolic_pressure,
                            'diastolic_pressure': row.diastolic_pressure
                            }

            All_Climbs.append(user_climb)
            
    return All_Climbs