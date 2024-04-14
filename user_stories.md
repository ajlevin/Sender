# User Stories:
1 As a consistent climber, I want to track my climbing frequency, intensity, and grades climbed, so that I can monitor my progress over time and set new goals for improvement.

2 As an older climber, I want to input and monitor my blood pressure and heart rate, so that I can ensure I'm maintaining optimal health for climbing.

3 As an experienced climber, I want to explore new climbing locations and styles, so that I can broaden my skills and experience different types of climbing challenges.

# Exceptions:
1 bad user input for health metrics
If a user inputs invalid data for weight, height, blood pressure, or age, the system will display an error message prompting the user to input valid data. Related to data type (string value for weight etc)

2 DB connection failure
If there is a failure in connecting to the database containing user data, the system will display a message informing the user of the technical issue and advise them to try again later. (Making sure that users data will eventually be tracked and not lost)

3 not enough data for feedback
If there is not enough data available to provide feedback after climbing, the system will notify the user and suggest completing their profile or provide more information for better feedback accuracy.


