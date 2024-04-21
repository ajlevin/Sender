### API Specification

#### 1. User Profile Management

##### 1.1. Create User Profile - `/profile/create` (POST)

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

##### 1.2. Update User Profile - /profile/{user_id} (PUT)
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
  "user_id": "string",
  "frequency": "integer",
  "intensity": "integer",
  "grades": ["string"],
  "heart_rate": "integer",
  "blood_pressure": {
    "systolic": "integer",
    "diastolic": "integer"
  }
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
    "sessions": [
        {
            "date": "string",
            "frequency": "integer",
            "intensity": "integer",
            "grades": ["string"],
            "heart_rate": "integer",
            "blood_pressure": {
                "systolic": "integer",
                "diastolic": "integer"
            }
        }
    ]
}
```

#### 3. Climbing Routes Management

##### 3.1. Search Climbing Routes - /routes/search/{user_id} (GET)
Searches and recommends climbing routes based on the user_id's information and sorts by
relevance

```json
{
    "routes": [
        {
            "name": "string",
            "location": "string",
            "difficulty_level": "string",
            "style": "string",
            "gear_requirements": ["string"]
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
  "name": "string",
  "location": "string",
  "difficulty_level": "string",
  "style": "string",
  "gear_requirements": ["string"]
}
```

Response:

```json
{
    "success": "boolean"
}
```

Example Flows
##### Climber Tracking Metrics Example Flow

John, an avid climber, wants to track his climbing metrics. He starts by creating a user profile:

John calls the endpoint /profile/create with his name, email, and age.
He receives a response indicating the success of the operation and his assigned user ID.
Next, John logs a climbing session:

John calls the endpoint /climbing/log with his user ID, climbing frequency, intensity, grades climbed, heart rate, and blood pressure.
He receives a success response indicating that his climbing session has been logged successfully.

##### Route Setting Example Flow
Sarah, a route setter at a climbing gym, wants to add a new climbing route to the database:

Sarah calls the endpoint /routes/add with the details of the new route, including its name, location, difficulty level, style, and gear requirements.
She receives a success response indicating that the new route has been added to the database.
