# Example Workflows:
###### Note: All testing was done through the VSCode debugger, so requests are simulated commands
###### VSCode Testing Command: /usr/bin/env /home/ajlevin/school/csc365/csc365_final_project/.venv/bin/python /home/ajlevin/.vscode-server/extensions/ms-python.debugpy-2024.6.0-linux-x64/bundled/libs/debugpy/adapter/../../debugpy/launcher 36947 -- -m uvicorn src.api.server:app


##### 1.1. Create New User - /user/create (PUT)
Creates a new user profile with basic information such as name, email, and age.

Response:

```json
{
    "success": "boolean",
    "user_id": "int"
}
```

# Testing Results:
1. Request:
    `curl -X 'PUT' 'https://csc365-final-project.onrender-com/user/create/' -H 'Content-Type application/json' -d '{"name":"Bob", "email":"bob@email.com", "age":24}'`

2. Response:
```json
{
    "success": "True",
    "user_id": 4
}
```

##### 1.2. Update Existing User - /user/{user_id} (POST)
Updates the user's profile information.

Response:

```json
{
    "success": "boolean"
}
```

# Testing Results:
1. Request:
    `curl -X 'POST' 'https://csc365-final-project.onrender-com/user/4/' -H 'Content-Type application/json' -d '{"email":"bob2@email.com"}'`

2. Response:
```json
{
    "success": "True"
}
```

##### 2.1. Log Climbing Session - /climbing/climb_log (POST)
Logs a climbing session with various metrics such as climbing frequency, intensity, grades, heart rate, and blood pressure.

Response:

```json
{
    "success": "boolean"
}
```

# Testing Results:
1. Request:
    `curl -X 'POST' 'https://csc365-final-project.onrender-com/climbing/climb_log/' -H 'Content-Type application/json' \`
    `-d '{"user_id":4, "route_id":646, "frequency":1, "intensity":3, "heart_rate":85, "systolic_pressure":118, "diastolic_pressure":81}'`

2. Response:
```json
{
    "success": "True"
}
```


##### 2.2. Get Climbing History - /climbing/history/{user_id} (GET)
Retrieves the climbing history for a user.

Response:

```json
{
    "sessions": [
        {
            "date": "string",
            "frequency": "integer",
            "intensity": "integer",
            "grades": ["string"],
            "heart_rate": "integer",
            "systolic_pressure": "integer",
            "diastolic_pressure": "integer"
        }
    ]
}
```

# Testing Results:
1. Request:
    `curl -X 'GET' 'https://csc365-final-project.onrender-com/climbing/history/1/' -H 'accept: application.json'`

2. Response:
```json
{
    "sessions": [
        {
            "date": "2024-05-06 00:10:17.355155+00",
            "frequency": 1,
            "intensity": 3,
            "grades": ["v3", "v4", "v3"],
            "heart_rate": 85,
            "systolic_pressure": 118,
            "diastolic_pressure": 81
        }
    ]
}
```

##### 3.1. Recommend New Route - /routes/recommend/ (GET)
Recommends climbing routes based on the user_id's information.

Response:

```json
{
    "routes": [
        {
            "route_id" : "int",
            "name": "string",
            "location": "string",
            "grade": "string",
            "style": "string",
            "description": "string"
        }
    ]
}
```

# Testing Results:
1. Request:
    `curl -X 'GET' 'https://csc365-final-project.onrender-com/climbing/climb_log/' -H 'Content-Type application/json' -d '{"user_id":5'`

2. Response:
```json
{
    "routes": [
        {
            "route_id" : 456,
            "name": "Double Trouble",
            "location": "Columbus, Ohio",
            "grade": "7.B",
            "style": "Sport",
            "description": "Short overhand with some gnarly pinches"
        },
        {
            "route_id" : 37,
            "name": "Left Hand Sam",
            "location": "Columbus, Ohio",
            "grade": "7.B-",
            "style": "Sport",
            "description": "Long Steep limestone face"
        }
    ]
}
```

##### 4.1. Add New Route - /routes/add/ (POST)
Retrieves the climbing history for a user.

Response:

```json
{
    "success": "boolean",
    "route_id": "int"
}
```

# Testing Results:
1. Request:
    `curl -X 'POST' 'https://csc365-final-project.onrender-com/climbing/climb_log/' -H 'Content-Type application/json' \`
    `-d '{"route_name":"Snake Eyes", "location":"Kansas City", "YDS":"V9", "boulder":"True", "fa":"Bob", \`
    `"description":"Dynamic Slab Problem where the eyes are all ya got", \`
    `"protection":"None, though the ground is fairly soft and there's no drops to worry while falling if pads are brought"}'`

2. Response:
```json
{
    "success": "True",
    "route_id": 646
}
```