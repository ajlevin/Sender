import os
import dotenv
import sqlalchemy
from src import database as db
from sqlalchemy import create_engine

def database_connection_url():
    dotenv.load_dotenv()

    return os.environ.get("POSTGRES_URI")

engine = create_engine(database_connection_url(), pool_pre_ping=True)

metadata_obj = sqlalchemy.MetaData()
profile_table = sqlalchemy.Table("profile", metadata_obj, autoload_with= db.engine)
climbing_table = sqlalchemy.Table("climbing", metadata_obj, autoload_with= db.engine)
routes_table = sqlalchemy.Table("routes", metadata_obj, autoload_with= db.engine)