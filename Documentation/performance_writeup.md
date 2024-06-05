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
| QUERY PLAN                                                                                                                                                                                            
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
| Sort  (cost=73551.72..73687.75 rows=54413 width=80) (actual time=1415.599..1502.417 rows=53720 loops=1)                                                                                               
|   Sort Key: (count(ra.user_id)) DESC, (max(r.yds)) DESC                                                                                                                                               
|   Sort Method: external merge  Disk: 1592kB                                                                                                                                                           
|   ->  Finalize HashAggregate  (cost=65929.42..67855.13 rows=54413 width=80) (actual time=1352.387..1453.317 rows=53720 loops=1)                                                                       
|         Group Key: u.user_id                                                                                                                                                                          
|         Planned Partitions: 4  Batches: 5  Memory Usage: 3505kB  Disk Usage: 3360kB                                                                                                                   
|         ->  Gather  (cost=51314.11..62913.33 rows=54413 width=80) (actual time=1196.082..1392.255 rows=88784 loops=1)                                                                                 
|               Workers Planned: 1                                                                                                                                                                      
|               Workers Launched: 1                                                                                                                                                                     
|               ->  Partial HashAggregate  (cost=50314.11..56472.03 rows=54413 width=80) (actual time=1190.181..1303.167 rows=44392 loops=2)                                                            
|                     Group Key: u.user_id                                                                                                                                                              
|                     Planned Partitions: 4  Batches: 5  Memory Usage: 3889kB  Disk Usage: 11552kB                                                                                                      
|                     Worker 0:  Batches: 5  Memory Usage: 3889kB  Disk Usage: 11512kB                                                                                                                  
|                     ->  Hash Join  (cost=4701.29..36234.73 rows=287426 width=52) (actual time=101.918..840.269 rows=924026 loops=2)                                                                   
|                           Hash Cond: (ra.user_id = u.user_id)                                                                                                                                         
|                           ->  Parallel Hash Join  (cost=2755.99..30300.89 rows=287426 width=12) (actual time=70.957..420.107 rows=924026 loops=2)                                                     
|                                 Hash Cond: (ra.route_id = r.route_id)                                                                                                                                 
|                                 ->  Parallel Seq Scan on ratings ra  (cost=0.00..24667.03 rows=1096303 width=16) (actual time=0.011..88.300 rows=931858 loops=2)                                      
|                                 ->  Parallel Hash  (cost=2404.39..2404.39 rows=28128 width=12) (actual time=70.680..70.681 rows=58656 loops=2)                                                        
|                                       Buckets: 131072 (originally 65536)  Batches: 1 (originally 1)  Memory Usage: 7072kB                                                                             
|                                       ->  Parallel Index Only Scan using **idx_routes_yds_route_id** on routes r  (cost=0.42..2404.39 rows=28128 width=12) (actual time=0.441..51.275 rows=58656 loops=2) |
|                                             Index Cond: (yds IS NOT NULL)                                                                                                                             
|                                             Filter: ((yds <> 'string'::text) AND (yds <> 'v?'::text))                                                                                                 
|                                             Heap Fetches: 1                                                                                                                                           
|                           ->  Hash  (cost=839.13..839.13 rows=54413 width=40) (actual time=30.621..30.621 rows=54413 loops=2)                                                                         
|                                 Buckets: 65536  Batches: 2  Memory Usage: 1584kB                                                                                                                      
|                                 ->  Seq Scan on users u  (cost=0.00..839.13 rows=54413 width=40) (actual time=0.023..18.521 rows=54413 loops=2)                                                       
| Planning Time: 21.864 ms                                                                                                                                                                              
| Execution Time: 1511.504 ms                                                                                                                                                                           

### recommend_route
#### Explain Results:
| QUERY PLAN                                                                                                                                           |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Limit  (cost=55.63..55.67 rows=16 width=369) (actual time=1.094..1.099 rows=30 loops=1)                                                              |
|   ->  Sort  (cost=55.63..55.67 rows=16 width=369) (actual time=1.093..1.096 rows=30 loops=1)                                                         |
|         Sort Key: climbing.created_at DESC                                                                                                           |
|         Sort Method: top-N heapsort  Memory: 69kB                                                                                                    |
|         ->  Nested Loop  (cost=0.71..55.31 rows=16 width=369) (actual time=0.051..0.986 rows=106 loops=1)                                            |
|               ->  Index Scan using climbing_user_id_idx on climbing  (cost=0.29..13.11 rows=16 width=16) (actual time=0.033..0.371 rows=106 loops=1) |
|                     Index Cond: (user_id = 30)                                                                                                       |
|               ->  Index Scan using routes_route_id_key on routes  (cost=0.42..2.64 rows=1 width=369) (actual time=0.005..0.005 rows=1 loops=106)     |
|                     Index Cond: (route_id = climbing.route_id)                                                                                       |
|                     Filter: ((route_lon IS NOT NULL) AND (route_lat IS NOT NULL))                                                                    |
| Planning Time: 1.050 ms                                                                                                                              |
| Execution Time: 1.178 ms                                                                                                                             |

| QUERY PLAN                                                                                                                                                            |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Limit  (cost=94497.35..94497.42 rows=30 width=457) (actual time=2004.847..2005.023 rows=30 loops=1)                                                                   |
|   ->  Sort  (cost=94497.35..94497.69 rows=137 width=457) (actual time=2004.845..2005.019 rows=30 loops=1)                                                             |
|         Sort Key: (round((abs(((routes.route_lat)::numeric - 44.31194)) + abs(((routes.route_lon)::numeric - '-68.18919'::numeric))), 1)), (avg(ratings.rating)) DESC |
|         Sort Method: top-N heapsort  Memory: 56kB                                                                                                                     |
|         ->  Hash Join  (cost=82280.78..94493.30 rows=137 width=457) (actual time=1428.319..2000.227 rows=7553 loops=1)                                                |
|               Hash Cond: (routes.route_id = ratings.route_id)                                                                                                         |
|               ->  Seq Scan on routes  (cost=0.00..12206.70 rows=912 width=409) (actual time=0.016..538.906 rows=9060 loops=1)                                         |
|                     Filter: ((route_lon IS NOT NULL) AND (route_lat IS NOT NULL) AND ((yds)::numeric = '5'::numeric))                                                 |
|                     Rows Removed by Filter: 173325                                                                                                                    |
|               ->  Hash  (cost=81939.03..81939.03 rows=27340 width=16) (actual time=1426.984..1427.155 rows=99682 loops=1)                                             |
|                     Buckets: 131072 (originally 32768)  Batches: 2 (originally 1)  Memory Usage: 3366kB                                                               |
|                     ->  Finalize HashAggregate  (cost=80896.69..81665.63 rows=27340 width=16) (actual time=1316.292..1396.913 rows=99682 loops=1)                     |
|                           Group Key: ratings.route_id                                                                                                                 |
|                           Batches: 21  Memory Usage: 4409kB  Disk Usage: 7488kB                                                                                       |
|                           ->  Gather  (cost=65860.64..79743.28 rows=27340 width=40) (actual time=1048.716..1263.429 rows=102614 loops=1)                              |
|                                 Workers Planned: 1                                                                                                                    |
|                                 Workers Launched: 1                                                                                                                   |
|                                 ->  Partial HashAggregate  (cost=64860.64..76009.28 rows=27340 width=40) (actual time=1033.803..1220.309 rows=51307 loops=2)          |
|                                       Group Key: ratings.route_id                                                                                                     |
|                                       Batches: 5  Memory Usage: 4401kB  Disk Usage: 18224kB                                                                           |
|                                       Worker 0:  Batches: 5  Memory Usage: 4401kB  Disk Usage: 19264kB                                                                |
|                                       ->  Parallel Seq Scan on ratings  (cost=0.00..25057.25 rows=1113625 width=12) (actual time=0.347..407.993 rows=946581 loops=2)  |
| Planning Time: 3.475 ms                                                                                                                                               |
| Execution Time: 2008.860 ms                                                                                                                                           |

#### Re-Ran Explain Results:
We were able to increase the speed of recommend_route by creating an index on route_id in ratings which decreased the time of the second query significantly. However, addint an index on route_id in the climbing table seems to have had negligible effects on the first query in the endpoint. 
`CREATE INDEX ON ratings (route_id)`
`CREATE INDEX ON climbing (route_id)`
| QUERY PLAN                                                                                                                                           |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Limit  (cost=55.63..55.67 rows=16 width=369) (actual time=1.397..1.401 rows=30 loops=1)                                                              |
|   ->  Sort  (cost=55.63..55.67 rows=16 width=369) (actual time=1.396..1.398 rows=30 loops=1)                                                         |
|         Sort Key: climbing.created_at DESC                                                                                                           |
|         Sort Method: top-N heapsort  Memory: 69kB                                                                                                    |
|         ->  Nested Loop  (cost=0.71..55.31 rows=16 width=369) (actual time=0.066..1.285 rows=106 loops=1)                                            |
|               ->  Index Scan using climbing_user_id_idx on climbing  (cost=0.29..13.11 rows=16 width=16) (actual time=0.040..0.531 rows=106 loops=1) |
|                     Index Cond: (user_id = 30)                                                                                                       |
|               ->  Index Scan using routes_route_id_key on routes  (cost=0.42..2.64 rows=1 width=369) (actual time=0.007..0.007 rows=1 loops=106)     |
|                     Index Cond: (route_id = climbing.route_id)                                                                                       |
|                     Filter: ((route_lon IS NOT NULL) AND (route_lat IS NOT NULL))                                                                    |
| Planning Time: 1.176 ms                                                                                                                              |
| Execution Time: 1.481 ms                                                                                                                             |

| QUERY PLAN                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Limit  (cost=60698.11..60698.19 rows=30 width=457) (actual time=1577.403..1600.922 rows=30 loops=1)                                                                                         |
|   ->  Sort  (cost=60698.11..60698.45 rows=137 width=457) (actual time=1577.401..1600.918 rows=30 loops=1)                                                                                   |
|         Sort Key: (round((abs(((routes.route_lat)::numeric - 44.31194)) + abs(((routes.route_lon)::numeric - '-68.18919'::numeric))), 1)), (avg(ratings.rating)) DESC                       |
|         Sort Method: top-N heapsort  Memory: 49kB                                                                                                                                           |
|         ->  Hash Join  (cost=12995.51..60694.06 rows=137 width=457) (actual time=581.312..1595.317 rows=7553 loops=1)                                                                       |
|               Hash Cond: (ratings.route_id = routes.route_id)                                                                                                                               |
|               ->  Finalize GroupAggregate  (cost=1000.44..48350.40 rows=27340 width=16) (actual time=10.821..987.479 rows=99682 loops=1)                                                    |
|                     Group Key: ratings.route_id                                                                                                                                             |
|                     ->  Gather Merge  (cost=1000.44..47871.95 rows=27340 width=40) (actual time=10.797..946.204 rows=99727 loops=1)                                                         |
|                           Workers Planned: 1                                                                                                                                                |
|                           Workers Launched: 1                                                                                                                                               |
|                           ->  Partial GroupAggregate  (cost=0.43..43796.19 rows=27340 width=40) (actual time=0.503..602.551 rows=49864 loops=2)                                             |
|                                 Group Key: ratings.route_id                                                                                                                                 |
|                                 ->  Parallel Index Scan using ratings_route_id_idx on ratings  (cost=0.43..37954.66 rows=1113625 width=12) (actual time=0.482..467.761 rows=946581 loops=2) |
|               ->  Hash  (cost=11983.67..11983.67 rows=912 width=409) (actual time=569.786..569.857 rows=9060 loops=1)                                                                       |
|                     Buckets: 16384 (originally 1024)  Batches: 1 (originally 1)  Memory Usage: 3894kB                                                                                       |
|                     ->  Gather  (cost=1000.00..11983.67 rows=912 width=409) (actual time=1.068..554.729 rows=9060 loops=1)                                                                  |
|                           Workers Planned: 1                                                                                                                                                |
|                           Workers Launched: 1                                                                                                                                               |
|                           ->  Parallel Seq Scan on routes  (cost=0.00..10892.47 rows=536 width=409) (actual time=0.976..556.107 rows=4530 loops=2)                                          |
|                                 Filter: ((route_lon IS NOT NULL) AND (route_lat IS NOT NULL) AND ((yds)::numeric = '5'::numeric))                                                           |
|                                 Rows Removed by Filter: 86662                                                                                                                               |
| Planning Time: 5.427 ms                                                                                                                                                                     |
| Execution Time: 1603.135 ms                                                                                                                                                                 |

### get_user_history
#### Explain Results:
| QUERY PLAN                                                                                               |
| -------------------------------------------------------------------------------------------------------- |
| Seq Scan on climbing  (cost=0.00..2084.01 rows=16 width=52) (actual time=0.021..39.035 rows=106 loops=1) |
|   Filter: (user_id = 30)                                                                                 |
|   Rows Removed by Filter: 99895                                                                          |
| Planning Time: 0.306 ms                                                                                  |
| Execution Time: 39.107 ms                                                                                |

#### Re-Ran Explain Results:
We were able to increase the speed of get_user_history ever by creating an index on user_id which decreased the time of the query notably
`CREATE INDEX ON climbing (user_id)`
| QUERY PLAN                                                                                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------- |
| Index Scan using climbing_user_id_idx on climbing  (cost=0.29..13.11 rows=16 width=52) (actual time=0.786..1.118 rows=106 loops=1) |
|   Index Cond: (user_id = 30)                                                                                                       |
| Planning Time: 0.382 ms                                                                                                            |
| Execution Time: 1.198 ms                                                                                                           |

### Performance Results and Usage:
#### get_leaderboard
For get_leaderboard it did more than we expected as we didn't think a query with count(*) in it could be made faster by this capacity. Indexes help to sort quickly sort out values needless to the quuery, but since the leaderboard needs to scan through every single entry regardless, there is little in the way of improvement that can be made in terms of efficiency.

#### recommend_route
For recommend_route the added index for the second query by almost half a second, which is a huge improvement for simply adding one line of code. Adding the route_id index to ratings allows the query to parse through the massive ratings table much faster, yielding a faster execution time. 

#### get_user_history
For get_user_history, there's little to optimize as it's simply a scan by user_id. Indexing by user_id helps to optimize it in selection, but there's little else to be done as it's a collective get from the database.
