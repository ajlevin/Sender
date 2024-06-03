from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
import os
import dotenv
from faker import Faker
import numpy as np

router = APIRouter(
    prefix="/testing",
    tags=["testing"],
    dependencies=[Depends(auth.get_api_key)],
)

def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

def populateTestData():
    # Create new DB engine based on connection string
    engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)
    grades = ["5.0", "5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8", "5.9", "5.10a", "5.10b", "5.10c", 
            "5.10d", "5.11a", "5.11b", "5.11c",  "5.11d", "5.12a", "5.12b", "5.12c", "5.12d", "5.13a", "5.13b", 
            "5.13c",  "5.13d",  "5.14a",  "5.14b", "5.14c", "5.14d", "5.15a", "5.15b", "5.15c", "5.15d"]
    
    resetTables(engine=engine)
    generateData(engine=engine, grades=grades)

### WARNING: This does drop tables, so ensure this is using a LOCAL test database before running.
def resetTables(engine, bypass_confirmation = False):
    # A user inputted confirmation is prompted unless bypassed by `bypass_confirmation`
    if not bypass_confirmation:
        confirmation = input(
            """
            This call is inteded to COMPLETELY RESET all tables for testing on a local database.\n
            If this is expected and you would like to continue with the test, please enter RUN_RESET: 
            """)
        if confirmation != "RUN_RESET":
            print("Cancelling reset request.")
            exit()
        else:
            print("Beginning reset request.")
    
    with engine.begin() as conn:
        conn.execute(sqlalchemy.text("""
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS routes;
        DROP TABLE IF EXISTS climbing;
        DROP TABLE IF EXISTS ratings;

        create table
            public.users (
                user_id bigint generated by default as identity,
                name text null,
                email text null,
                age integer null,
                created_at timestamp with time zone not null default now(),
                constraint users_pkey primary key (user_id),
                constraint users_user_id_key unique (user_id)
            ) tablespace pg_default;

        create table
            public.routes (
                route_id bigint generated by default as identity,
                yds text null,
                trad boolean null default false,
                sport boolean null default false,
                description text null,
                location text null,
                protection text null,
                created_at timestamp with time zone not null default now(),
                route_name text null,
                route_lat text null,
                route_lon text null,
                other boolean null default false,
                state_name text null,
                constraint routes_pkey primary key (route_id),
                constraint routes_route_id_key unique (route_id)
            ) tablespace pg_default;

            create index if not exists max_yds_idx on public.routes using btree (yds) tablespace pg_default;

        create table
            public.climbing (
                climbing_id bigint generated by default as identity,
                user_id bigint null,
                frequency integer null,
                intensity integer null,
                route_id bigint null,
                heart_rate integer null,
                systolic_pressure integer null,
                diastolic_pressure integer null,
                created_at timestamp with time zone not null default now(),
                constraint climbing_pkey primary key (climbing_id),
                constraint climbing_route_id_fkey foreign key (route_id) references routes (route_id) on update cascade on delete cascade,
                constraint climbing_user_id_fkey foreign key (user_id) references users (user_id) on update cascade on delete cascade
            ) tablespace pg_default;

        create table
            public.ratings (
                user_id bigint not null,
                route_id bigint not null,
                rating real null,
                created_at timestamp with time zone null,
                rating_id bigint not null,
                constraint ratings_pkey primary key (rating_id),
                constraint ratings_route_id_fkey foreign key (route_id) references routes (route_id) on update cascade on delete cascade,
                constraint ratings_user_id_fkey foreign key (user_id) references users (user_id) on update cascade on delete cascade
            ) tablespace pg_default;
        """))

def generateData(engine, grades, bypass_confirmation = False, iters = 1000000):
    # A user inputted confirmation is prompted unless bypassed by `bypass_confirmation`
    if not bypass_confirmation:
        confirmation = input(
            """
            This call is inteded fill tables with over 1 million entries for testing on a local database.\n
            If this is expected and you would like to continue with the test, please enter RUN_GENERATE: 
            """)
        if confirmation != "RUN_GENERATE":
            print("Cancelling generate request.")
            exit()
        else:
            print("Beginning generate request.")

    fake = Faker()
    total_logs = 0
    total_ratings = 0
    logs_sample_distribution = np.random.default_rng().negative_binomial(0.04, 0.01, iters)
    ratings_sample_distribution = np.random.default_rng().negative_binomial(0.05, 0.02, iters)
    yds_sample_distribution = np.random.choice(grades, iters, p = np.random.dirichlet(np.ones(34),size=1)[0])

    with engine.begin() as conn:
        print("Faking data...")
        logs = []
        ratings = []
        route_ids = []
        for i in range(iters):
            if (i % 100 == 0):
                print(f"iteration: %d/%d", i, iters)
            
            profile = fake.profile()
            user_id = conn.execute(sqlalchemy.text(
                """
                INSERT INTO users (name, email, age, created_at) VALUES (:name, :email, :age, :created_at) RETURNING user_id;
                """), 
            {"name": profile['name'], 
             "email": profile['mail'], 
             "age": fake.pyint(18, 75), 
             "created_at": fake.date_time_between(start_date='-8y', end_date='-2y', tzinfo=None)}).scalar_one()

            route_id = conn.execute(sqlalchemy.text(
                """
                INSERT INTO routes (yds, sport, trad, description, location, protection, created_at, route_name, route_lat, route_lon, state_name) 
                VALUES (:yds, :sport, :trad, :description, :location, :protection, :created_at, :route_name, :route_lat, :route_lon, :state_name) RETURNING route_id;
                """), 
            {"yds": yds_sample_distribution[i].item(), 
             "trad": fake.boolean(50), 
             "sport": fake.boolean(50),
             "description": fake.text(), 
             "location": fake.location_on_land(),
             "protection": fake.sentence(), 
             "created_at": fake.date_time_between(start_date='-8y', end_date='now', tzinfo=None),
             "route_name": fake.name(), 
             "route_lat": fake.latitude(), 
             "route_lon": fake.longitude(), 
             "state_name": fake.state()}).scalar_one()   
            route_ids.append(route_id)         

            num_logs = logs_sample_distribution[i]
            num_ratings = ratings_sample_distribution[i]
            for j in range(num_logs):
                total_logs += 1
                logs.append({
                    "user_id": user_id,
                    "frequency": 3,
                    "intensity": fake.pyint(0, 100),
                    "route_id": route_ids[fake.pyint(0, len(route_ids) - 1)],
                    "heart_rate": fake.pyint(),
                    "systolic_pressure": fake.pyint(60, 140),
                    "diastolic_pressure": fake.pyint(20, 90),
                    "created_at": fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None),
                })

            for j in range(num_ratings):
                total_ratings += 1
                ratings.append({
                    "user_id": user_id,
                    "route_id": route_ids[fake.pyint(0, len(route_ids) - 1)],
                    "rating": fake.pyint(0, 10),
                    "created_at": fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None),
                })

        if logs:
            conn.execute(sqlalchemy.text("""
            INSERT INTO climbing (user_id, frequency, intensity, route_id, heart_rate, systolic_pressure, diastolic_pressure, created_at) 
            VALUES (:user_id, :frequency, :intensity, :route_id, :heart_rate, :systolic_pressure, :diastolic_pressure, :created_at);
            """), logs)
        if ratings:
            conn.execute(sqlalchemy.text("""
            INSERT INTO ratings (user_id, route_id, rating, created_at) VALUES (:user_id, :route_id, :rating, :created_at);
            """), logs)

        print("total logs: ", total_logs)
        print("total ratings: ", total_ratings)