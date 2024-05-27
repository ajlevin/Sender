from fastapi import APIRouter, Depends
import sqlalchemy
import os
import dotenv
from faker import Faker
import numpy as np
from timeit import timeit
from src.api.climbing import *
from src.api.routes import *
from src.api.user import *
from src.api.leaderboard import *

def database_connection_url():
    dotenv.load_dotenv()
    return os.environ.get("POSTGRES_URI")

engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

def main():
    print("Select Request Type:\n"
        "| Reset tables [RESET]\n" +
        "| Reset tables and generate data [GENERATE]\n" +
        "| Run metrics [METRICS]\n" +
        "| Reset tables and generate data and run metrics [FULL]\n")
    request = input("Please enter the code within brackets that corresponds to your desired request: ")
    match request:
        case "RESET":
            print("Resetting tables...")
            resetTables()
        case "GENERATE":
            print("Populating test data...")
            populateTestData()
        case "METRICS":
            print("Running metrics...")
            runMetrics()
        case "FULL":
            print("Running full suite request...")
            print("Populating test data...")
            populateTestData()
            print("Running metrics...")
            runMetrics()
        case _:
            print("Invalid input... EXITING.")
            exit()

def populateTestData():
    # Create new DB engine based on connection string
    grades = ["5.0", "5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8", "5.9", "5.10a", "5.10b", "5.10c", 
            "5.10d", "5.11a", "5.11b", "5.11c",  "5.11d", "5.12a", "5.12b", "5.12c", "5.12d", "5.13a", "5.13b", 
            "5.13c",  "5.13d",  "5.14a",  "5.14b", "5.14c", "5.14d", "5.15a", "5.15b", "5.15c", "5.15d"]
    
    resetTables()
    generateData(grades=grades)


### WARNING: This does drop tables, so ensure this is using a LOCAL test database before running.
def resetTables(bypass_confirmation = False):
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

def generateData(grades, bypass_confirmation = False, iters = 500000):
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
        # Clears storage files (and creates them if they don't already exist)
        with open("testUserIds.txt", "a+") as f:
            f.truncate()
        with open("testUserIds.txt", "a+") as f:
            f.truncate()
        
        print("Faking data...")
        logs = []
        ratings = []
        user_ids = []
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
            user_ids.append(user_id)

            isTrad = fake.boolean(50)
            route_id = conn.execute(sqlalchemy.text(
                """
                INSERT INTO routes (yds, sport, trad, description, location, protection, created_at, route_name, route_lat, route_lon, state_name) 
                VALUES (:yds, :sport, :trad, :description, :location, :protection, :created_at, :route_name, :route_lat, :route_lon, :state_name) RETURNING route_id;
                """), 
            {"yds": yds_sample_distribution[i].item(), 
             "trad": isTrad, 
             "sport": not isTrad,
             "description": fake.text(), 
             "location": fake.place_name(),
             "protection": fake.sentence(), 
             "created_at": fake.date_time_between(start_date='-8y', end_date='now', tzinfo=None),
             "route_name": fake.name(), 
             "route_lat": str(fake.latitude()), 
             "route_lon": str(fake.longitude()), 
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
                    "heart_rate": fake.pyint(60, 180),
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

        with open("testUserIds.txt", "a+") as f:
            for id in user_ids:
                f.write(str(id) + "\n")
            print("Test user IDs saved to testUserIds.txt")

        with open("testUserIds.txt", "a+") as f:
            for id in route_ids:
                f.write(str(id) + "\n")
            print("Test route IDs saved to testRouteIds.txt")
        
        print("total logs: ", total_logs)
        print("total ratings: ", total_ratings)

def runMetrics():
    mocked = mockParams()
    ccl = timeit(create_climb_log(mocked.get("ccl")))
    guh = timeit(get_user_history(mocked.get("guh")))
    rr = timeit(recommend_route(mocked.get("rr")))
    gr = timeit(get_routes(mocked.get("gr")))
    cr = timeit(create_route(mocked.get("cr")))
    cu = timeit(create_user(mocked.get("cu")))
    uu = timeit(update_user(mocked.get("uu")))
    gl = timeit(get_leaderboard(mocked.get("gl")))

    print(f"create_climb_log runtime: {ccl:.3f}")
    print(f"get_user_history runtime: {guh:.3f}")
    print(f"recommend_route runtime: {rr:.3f}")
    print(f"get_routes runtime: {gr:.3f}")
    print(f"create_route runtime: {cr:.3f}")
    print(f"create_user runtime: {cu:.3f}")
    print(f"update_user runtime: {uu:.3f}")
    print(f"get_leaderboard runtime: {gl:.3f}")
    pass

def mockParams():
    testUserIds = []
    testRouteIds = []
    try:
        with open("testUserIds.txt", "r") as f:
            testUserIds = f.readlines()
        with open("testUserIds.txt", "r") as f:
            testRouteIds = f.readlines()
    except IOError:
        print("Test ID files do not exist. Please rerun a generation request.")
        exit()
    
    fake = Faker()
    paramDict = {
        "ccl" : None,
        "guh" : None,
        "rr" : None,
        "gr" : None,
        "cr" : None,
        "cu" : None,
        "uu" : None,
        "gl" : None,
    }

    ### Mocked for create_climb_log
    paramDict["ccl"] = Climb(
        user_id=int(testUserIds[fake.pyint(0, len(testUserIds) - 1)]),
        route_id=int(testRouteIds[fake.pyint(0, len(testRouteIds) - 1)]),
        frequency=fake.pyint(0, 10),
        intensity=fake.pyint(0, 100),
        heart_rate=fake.pyint(60, 180),
        systolic_pressure=fake.pyint(60, 140),
        diastolic_pressure=fake.pyint(20, 90)
    )

    ### Mocked for get_user_history
    paramDict["guh"] = int(testUserIds[fake.pyint(0, len(testUserIds) - 1)])

    ### Mocked for recommend_route
    paramDict["rr"] = int(testUserIds[fake.pyint(0, len(testUserIds) - 1)])

    ### Mocked for get_routes
    paramDict["gr"] = ("5.11c", str(fake.pyint(0, 5)))

    ### Mocked for create_route
    isTrad = fake.boolean(50)
    paramDict["cr"] = Route(
        route_name=fake.name(),
        location=fake.place_name(),
        yds="5.11c",
        trad=isTrad,
        sport=not isTrad,
        other=False,
        description=fake.text(),
        protection=fake.sentence(),
        route_lat=str(fake.latitude()),
        route_lon=str(fake.longitude())
    )

    ### Mocked for create_user
    cuProfile = fake.profile()
    paramDict["cu"] = User(
        name=cuProfile["name"],
        email=cuProfile["mail"],
        age=fake.pyint(18, 75)
    )

    ### Mocked for update_user
    uuProfile = fake.profile()
    paramDict["uu"] = (
        int(testUserIds[fake.pyint(0, len(testUserIds) - 1)]), 
        User(
            name=uuProfile["name"],
            email=uuProfile["mail"],
            age=fake.pyint(18, 75)))
    
    paramDict["gl"] = LeaderboardQueryParams(SortOptions.total_climbs)

    return paramDict

if __name__ == "__main__":
    main()