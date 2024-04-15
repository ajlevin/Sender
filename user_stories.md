# User Stories:
1. As a consistent climber, I want to track my climbing frequency, intensity, and grades climbed, so that I can monitor my progress over time and set new goals for improvement.

2. As an older climber, I want to input and monitor my blood pressure and heart rate, so that I can ensure I'm maintaining optimal health for climbing.

3. As an experienced climber, I want to explore new climbing locations and styles, so that I can broaden my skills and experience different types of climbing challenges.

4. As a new climber looking to integrate climbing into a regular workout routine, I'd like to monitor the changes over short and long term changes it has on my body.

5. As a climber recovering from a heart-arythmia, I want to ensure that my heart rate is kept at safe levels for me during climbing sessions

6. As a speed climber, I'd like to be able to set intervals to monitor and comapare health metrics over short and long periods of time\

7. As an outdoor climbing enthusiast, I want to discover nearby climbing routes and access information on difficulty level, and any special gear requirements, so that I can plan my climbing trips more effectively.

8. As a route setter at a climbing gym, I want to document and share my new routes with the climbing community, including details such as route grade, type of holds, and any specific techniques required, so that climbers can enjoy fresh challenges.

9. As a climber traveling to new areas, I want to connect with local climbers, so that I can have a more social and collaborative climbing experience.

10. As a climber with dietary restrictions, I want to find information on climbing-friendly meal plans and nutrition tips to support my training and recovery, so that I can optimize my performance on and off the wall.

11. As a competitive climber, I want to track my performance in climbing competitions, including rankings, scores, and progress over time, so that I can assess my strengths and weaknesses and improve my skills for future competitions.

12. As a parent bringing my child to a climbing gym, I want to find kid-friendly climbing routes and safety information tailored to their age and experience level, so that they can have a safe and enjoyable climbing experience.


# Exceptions:
1. Bad user input for health metrics
* If a user inputs invalid data for weight, height, blood pressure, age, or other biometrics, the system will display an error message prompting the user to input valid data depending on the field that errored.

2. Incomplete health metrics input
* If the user submits incomplete health metrics data (e.g., missing weight, height, or blood pressure), the system will display an error message indicating the missing fields and prompt the user to complete all required information before proceeding.

3. DB connection failure
* If there is a failure in connecting to the database containing user data, the system will display a message informing the user of the a desync from the cloud, and that all data will be stored locally and displayed based on that until connection is made again.

4. Not enough data for feedback
* If there is not enough data available to provide feedback after climbing, the system will notify the user and suggest completing their profile or provide more information for better feedback accuracy.

5. Login failure
* If the user enters the incorrect login information, it will simply prompt the user to reenter or reset their details.

6. Conflicting Data Sycnhronization
* If for whatever reason, the data stored locally conflicts with the data in the cloud, the user will be prompted to select which data to continue with.

7. Improper time logging
* Should the user enter start and end times to sessions where the start time comes after the end time, the user is prompted to adjust their time to a valid entry accordingly

8. Server maintenance or outage
* If the server hosting the climbing app is undergoing maintenance or experiences an outage, the system will display a message informing the user of the issue and advise them to try again later. Additionally, any unsynced data will be stored locally and synced once the server is back online.

9. Duplicate account creation attempt
* If a user tries to create a new account using an email address that is already associated with an existing account, the system will display an error message indicating that the email address is already in use and prompt the user to log in or use a different email address to create a new account.

10. Payment processing failure for premium features (if a paid version is implemented)
* If a user tries to purchase premium features within the app but the payment processing fails (e.g., due to expired credit card or insufficient funds), the system will prompt the user to update their payment information or try a different payment method.

11. Device compatibility issue with app features
* If a user's device does not meet the necessary specifications or compatibility requirements to use certain app features (e.g., GPS tracking for route recording), the system will display a message informing the user of the compatibility issue and suggest alternative methods or devices to access the desired features.

12. Missing route information in database
* If a user searches for a specific climbing route and it is not found in the app's database, the system will display a message indicating that the route may not be available. The user will be prompted to provide additional details or suggest the route for inclusion in future updates.
