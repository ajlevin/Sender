### API Specification

#### 1. User Profile Management

##### 1.1. Create User Profile - `/user/create` (POST)

Creates a new user profile with basic information such as name, email, and age.

**Request**:

```json
{
  "name": "string",
  "email": "string",
  "age": "integer"
}
```
Response:

```json
{
    "success": "boolean",
    "user_id": "string"
}
```

##### 1.2. Update User Profile - /user/{user_id} (PUT)
Updates the user's profile information.

Request:

```json
{
  "name": "string",
  "email": "string",
  "age": "integer"
}
```
Response:

```json
{
    "success": "boolean"
}
```

#### 2. Climbing Metrics Tracking

##### 2.1. Log Climbing Session - /climbing/log (POST)
Logs a climbing session with various metrics such as climbing frequency, intensity, grades, heart rate, and blood pressure.

Request:

```json
{
  "user_id": "integer",
  "route_id": "integer",
  "frequency": "integer",
  "intensity": "integer",
  "heart_rate": "integer",
  "systolic_pressure": "integer",
  "diastolic_pressure": "integer"
}
```
Response:

```json
{
    "success": "boolean"
}
```

##### 2.2. Get Climbing History - /climbing/history/{user_id} (GET)
Retrieves the climbing history for a user.

Response:

```json
{
   [
        {
        "user_id": "integer",
        "route_id": "integer",
        "frequency": "integer",
        "intensity": "integer",
        "heart_rate": "integer",
        "systolic_pressure": "integer",
        "diastolic_pressure": "integer"
        }
    ]
}
```

#### 3. Climbing Routes Management

##### 3.1. Search Climbing Routes - /routes/search/{user_id} (GET)
Searches and recommends climbing routes based on the user_id's information and sorts by
relevance

Request:

```json
{
    "user_id": "int"
}
```

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
#### 4. Route Setting

##### 4.1. Add New Route - /routes/add (POST)
Adds a new climbing route to the database.

Request:

```json
{
  "route_name": "string",
  "location": "string",
  "YDS": "string",
  "Font": "string",
  "French": "string",
  "Ewbanks": "string",
  "UIAA": "string",
  "ZA": "string",
  "British": "string",
  "yds_aid": "string",
  "boulder": "boolean",
  "tr": "boolean",
  "ice": "boolean",
  "trad": "boolean",
  "sport": "boolean",
  "aid": "boolean",
  "mixed": "boolean",
  "snow": "boolean",
  "alpine": "boolean",
  "fa": "str",
  "description": "string",
  "protection": "string"
}
```

Response:

```json
{
    "success": "boolean",
    "route_id": "int"
}
```

Example Flows

##### User Management Example FLow

John, an avid climber, wants to track his climbing metrics. He starts by creating a user profile:

John calls the endpoint /profile/create with his name, email, and age.
He receives a response indicating the success of the operation and his assigned user ID.
Next, John logs a climbing session:

John calls the endpoint /climbing/log with his user ID, climbing frequency, intensity, grades climbed, heart rate, and blood pressure.
He receives a success response indicating that his climbing session has been logged successfully.

##### Climber Tracking Metrics Example Flow

Jasper, an intermediate climber, wants to monitor their improvement over time as they're getting back into climbing after some time off.

They first updates their profile with a new email after their time away, calling the endpoint /profile/jasperClimbz to swap emails.
They receive back a successful response indiciating the update has been saved and applied to the acocunt.

They then take a look at their old climbing data, calling /climbing/history/jasperClimbz to see where their baseline stands.
They receive back a successful response containing a list of metrics from their prior saved climbs.

##### Route Setting Example Flow
Sarah, a route setter at a climbing gym, wants to add a new climbing route to the database:

Sarah calls the endpoint /routes/add with the details of the new route, including its name, location, difficulty level, style, and gear requirements.
She receives a success response indicating that the new route has been added to the database.