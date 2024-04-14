# User Stories:
1. As a consistent climber, I want to track my climbing frequency, intensity, and grades climbed, so that I can monitor my progress over time and set new goals for improvement.

2. As an older climber, I want to input and monitor my blood pressure and heart rate, so that I can ensure I'm maintaining optimal health for climbing.

3. As an experienced climber, I want to explore new climbing locations and styles, so that I can broaden my skills and experience different types of climbing challenges.

4. As a new climber looking to integrate climbing into a regular workout routine, I'd like to monitor the changes over short and long term changes it has on my body.

5. As a climber recovering from a heart-arythmia, I want to ensure that my heart rate is kept at safe levels for me during climbing sessions

6. As a speed climber, I'd like to be able to set intervals to monitor and comapare health metrics over short and long periods of time

# Exceptions:
1. Bad user input for health metrics
* If a user inputs invalid data for weight, height, blood pressure, age, or other biometrics, the system will display an error message prompting the user to input valid data depending on the field that errored.

2. DB connection failure
* If there is a failure in connecting to the database containing user data, the system will display a message informing the user of the a desync from the cloud, and that all data will be stored locally and displayed based on that until connection is made again.

3. Not enough data for feedback
* If there is not enough data available to provide feedback after climbing, the system will notify the user and suggest completing their profile or provide more information for better feedback accuracy.

4. Login failure
* If the user enters the incorrect login information, it will simply prompt the user to reenter or reset their details.

5. Conflicting Data Sycnhronization
* If for whatever reason, the data stored locally conflicts with the data in the cloud, the user will be prompted to select which data to continue with.

6. Improper time logging
* Should the user enter start and end times to sessions where the start time comes after the end time, the user is prompted to adjust their time to a valid entry accordingly


