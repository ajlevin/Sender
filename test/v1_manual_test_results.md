# Example Workflow:
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
    curl -X 'GET' 'https://.../climbing/history/1/' -H 'accept: application.json'

2. Response:
    "sessions": [
        {
            "date": "2024-05-06 00:10:17.355155+00",
            "frequency": "1",
            "intensity": "3",
            "grades": ["v3", "v4", "v3"],
            "heart_rate": "85",
            "systolic_pressure": "118",
            "diastolic_pressure": "81"
        }
    ]