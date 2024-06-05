# Data Mocking
### Data was mocked within using the Faker library within `performanceTestProcessor.py`.

Data mocking was done through half-a-million iterations providing a 500k users and an equivalent 500k routes. For each user and for each route, an range of values is selected to generate logs and ratings for each respectively. This is meant to replicate the realistic setting in which routes and users will have multiple logs and rating respectively during their duration. In addition, having the service scale to an immense amount of users, routes, logs, and ratings is fairly realistic when considering that over time users will continue to make accounts and the service will grow and grow, if but slowly. Climbing is not some fad, but a sport that has remained consistently prevalent for decades. Even if the service grows slowly, consistent growth can be assumed. Not only that, but routes will most likely receive multiple ratings over their lifespan as numerous people climb them, as will a single user accrue a number of logs as they use the service.

# Performance Results
    create_climb_log runtime: ___ms
    get_user_history runtime: ___ms
    recommend_route runtime: ___ms
    get_routes runtime: ___ms
    create_route runtime: ___ms
    create_user runtime: ___ms
    update_user runtime: ___ms

### Slowest three endpoints (from fastest to slowest): 
________ (___ms), ________ (___ms), ________ (___ms)

# Tuning
### Explain Results:
________

### Adding Indexes:
________

### Re-Ran Explain Results:
________

### Performance Results and Usage:
________