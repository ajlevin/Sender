# Data Mocking
### Data was mocked within using the Faker library within `performanceTestProcessor.py`.

Data mocking was done through half-a-million iterations providing a 500k users and an equivalent 500k routes. For each user and for each route, an range of values is selected to generate logs and ratings for each respectively. This is meant to replicate the realistic setting in which routes and users will have multiple logs and rating respectively during their duration. In addition, having the service scale to an immense amount of users, routes, logs, and ratings is fairly realistic when considering that over time users will continue to make accounts and the service will grow and grow, if but slowly. Climbing is not some fad, but a sport that has remained consistently prevalent for decades. Even if the service grows slowly, consistent growth can be assumed. Not only that, but routes will most likely receive multiple ratings over their lifespan as numerous people climb them, as will a single user accrue a number of logs as they use the service.

# Performance Results
    create_climb_log runtime: 77 ms
    get_user_history runtime: 202 ms
    recommend_route runtime: 3510 ms
    get_routes runtime: 79 ms
    create_route runtime: 107 ms
    create_user runtime: 86 ms
    update_user runtime: 75 ms
    get_leaderboard runtime: 2608 ms

### Slowest three endpoints (from fastest to slowest): 
get_user_history (202 ms), recommend_route (3510 ms), get_leaderboard (2608 ms)

# Tuning

### get_leaderboard
#### Explain Results:
| QUERY PLAN                                                                                                                                                                                            |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sort  (cost=73551.72..73687.75 rows=54413 width=80) (actual time=2557.388..2602.370 rows=53720 loops=1)                                                                                               |
|   Sort Key: (count(ra.user_id)) DESC, (max(r.yds)) DESC                                                                                                                                               |
|   Sort Method: external merge  Disk: 1592kB                                                                                                                                                           |
|   ->  Finalize HashAggregate  (cost=65929.42..67855.13 rows=54413 width=80) (actual time=2489.792..2552.754 rows=53720 loops=1)                                                                       |
|         Group Key: u.user_id                                                                                                                                                                          |
|         Planned Partitions: 4  Batches: 5  Memory Usage: 4273kB  Disk Usage: 3376kB                                                                                                                   |
|         ->  Gather  (cost=51314.11..62913.33 rows=54413 width=80) (actual time=2332.651..2487.589 rows=88591 loops=1)                                                                                 |
|               Workers Planned: 1                                                                                                                                                                      |
|               Workers Launched: 1                                                                                                                                                                     |
|               ->  Partial HashAggregate  (cost=50314.11..56472.03 rows=54413 width=80) (actual time=2334.944..2439.967 rows=44296 loops=2)                                                            |
|                     Group Key: u.user_id                                                                                                                                                              |
|                     Planned Partitions: 4  Batches: 5  Memory Usage: 3889kB  Disk Usage: 11568kB                                                                                                      |
|                     Worker 0:  Batches: 5  Memory Usage: 3889kB  Disk Usage: 11712kB                                                                                                                  |
|                     ->  Hash Join  (cost=4701.29..36234.73 rows=287426 width=52) (actual time=124.377..1988.241 rows=924026 loops=2)                                                                  |
|                           Hash Cond: (ra.user_id = u.user_id)                                                                                                                                         |
|                           ->  Parallel Hash Join  (cost=2755.99..30300.89 rows=287426 width=12) (actual time=108.109..1572.637 rows=924026 loops=2)                                                   |
|                                 Hash Cond: (ra.route_id = r.route_id)                                                                                                                                 |
|                                 ->  Parallel Seq Scan on ratings ra  (cost=0.00..24667.03 rows=1096303 width=16) (actual time=0.011..171.183 rows=931858 loops=2)                                     |
|                                 ->  Parallel Hash  (cost=2404.39..2404.39 rows=28128 width=12) (actual time=107.866..107.867 rows=58656 loops=2)                                                      |
|                                       Buckets: 131072 (originally 65536)  Batches: 1 (originally 1)  Memory Usage: 7072kB                                                                             |
|                                       ->  Parallel Index Only Scan using idx_routes_yds_route_id on routes r  (cost=0.42..2404.39 rows=28128 width=12) (actual time=0.035..85.937 rows=58656 loops=2) |
|                                             Index Cond: (yds IS NOT NULL)                                                                                                                             |
|                                             Filter: ((yds <> 'string'::text) AND (yds <> 'v?'::text))                                                                                                 |
|                                             Heap Fetches: 1                                                                                                                                           |
|                           ->  Hash  (cost=839.13..839.13 rows=54413 width=40) (actual time=15.985..15.986 rows=54413 loops=2)                                                                         |
|                                 Buckets: 65536  Batches: 2  Memory Usage: 1584kB                                                                                                                      |
|                                 ->  Seq Scan on users u  (cost=0.00..839.13 rows=54413 width=40) (actual time=0.017..6.682 rows=54413 loops=2)                                                        |
| Planning Time: 7.077 ms                                                                                                                                                                               |
| Execution Time: 2608.709 ms                                                                                                                                                                           

#### Re-Ran Explain Results:
We were able to increase the speed of get_leaderboard very slightly by creating an index on both yds and route_id which decreased the time of the query
`CREATE INDEX ON routes (yds)`
`CREATE INDEX ON routes (route_id)`
| QUERY PLAN                                                                                                                                                                                            |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sort  (cost=73551.72..73687.75 rows=54413 width=80) (actual time=1415.599..1502.417 rows=53720 loops=1)                                                                                               |
|   Sort Key: (count(ra.user_id)) DESC, (max(r.yds)) DESC                                                                                                                                               |
|   Sort Method: external merge  Disk: 1592kB                                                                                                                                                           |
|   ->  Finalize HashAggregate  (cost=65929.42..67855.13 rows=54413 width=80) (actual time=1352.387..1453.317 rows=53720 loops=1)                                                                       |
|         Group Key: u.user_id                                                                                                                                                                          |
|         Planned Partitions: 4  Batches: 5  Memory Usage: 3505kB  Disk Usage: 3360kB                                                                                                                   |
|         ->  Gather  (cost=51314.11..62913.33 rows=54413 width=80) (actual time=1196.082..1392.255 rows=88784 loops=1)                                                                                 |
|               Workers Planned: 1                                                                                                                                                                      |
|               Workers Launched: 1                                                                                                                                                                     |
|               ->  Partial HashAggregate  (cost=50314.11..56472.03 rows=54413 width=80) (actual time=1190.181..1303.167 rows=44392 loops=2)                                                            |
|                     Group Key: u.user_id                                                                                                                                                              |
|                     Planned Partitions: 4  Batches: 5  Memory Usage: 3889kB  Disk Usage: 11552kB                                                                                                      |
|                     Worker 0:  Batches: 5  Memory Usage: 3889kB  Disk Usage: 11512kB                                                                                                                  |
|                     ->  Hash Join  (cost=4701.29..36234.73 rows=287426 width=52) (actual time=101.918..840.269 rows=924026 loops=2)                                                                   |
|                           Hash Cond: (ra.user_id = u.user_id)                                                                                                                                         |
|                           ->  Parallel Hash Join  (cost=2755.99..30300.89 rows=287426 width=12) (actual time=70.957..420.107 rows=924026 loops=2)                                                     |
|                                 Hash Cond: (ra.route_id = r.route_id)                                                                                                                                 |
|                                 ->  Parallel Seq Scan on ratings ra  (cost=0.00..24667.03 rows=1096303 width=16) (actual time=0.011..88.300 rows=931858 loops=2)                                      |
|                                 ->  Parallel Hash  (cost=2404.39..2404.39 rows=28128 width=12) (actual time=70.680..70.681 rows=58656 loops=2)                                                        |
|                                       Buckets: 131072 (originally 65536)  Batches: 1 (originally 1)  Memory Usage: 7072kB                                                                             |
|                                       ->  Parallel Index Only Scan using **idx_routes_yds_route_id** on routes r  (cost=0.42..2404.39 rows=28128 width=12) (actual time=0.441..51.275 rows=58656 loops=2) |
|                                             Index Cond: (yds IS NOT NULL)                                                                                                                             |
|                                             Filter: ((yds <> 'string'::text) AND (yds <> 'v?'::text))                                                                                                 |
|                                             Heap Fetches: 1                                                                                                                                           |
|                           ->  Hash  (cost=839.13..839.13 rows=54413 width=40) (actual time=30.621..30.621 rows=54413 loops=2)                                                                         |
|                                 Buckets: 65536  Batches: 2  Memory Usage: 1584kB                                                                                                                      |
|                                 ->  Seq Scan on users u  (cost=0.00..839.13 rows=54413 width=40) (actual time=0.023..18.521 rows=54413 loops=2)                                                       |
| Planning Time: 21.864 ms                                                                                                                                                                              |
| Execution Time: 1511.504 ms                                                                                                                                                                           |

### recommend_route
#### Explain Results:
#### Re-Ran Explain Results:
We were able to increase the speed of recommend_route by creating an index on ______ which decreased the time of the query
`CREATE INDEX ON ------- (----)`

### get_user_history
#### Explain Results:

#### Re-Ran Explain Results:
We were able to increase the speed of get_user_history ever so slightly by creating an index on user_id which decreased the time of the query by a fraction
`CREATE INDEX ON climbing (user_id)`

### Performance Results and Usage:
#### get_leaderboard
For get_leaderboard it did more than we expected as we didn't think a query with count(*) in it could be made faster by this capacity. Indexes help to sort quickly sort out values needless to the quuery, but since the leaderboard needs to scan through every single entry regardless, there is little in the way of improvement that can be made in terms of efficiency.

#### recommend_route
For recommend_route...

#### get_user_history
For get_user_history, there's little to optimize as it's simply a scan by user_id. Indexing by user_id helps to optimize it slightly in seleciton, but there's little else to be done as it's a collective get from the database.
