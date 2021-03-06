# Things that need doing

- [x] For a day: save in .txt all the requests with origin and
destination, like the demands.txt attached. Also store in another file
the # taxis.

- [x] Compute N stations (N=100 initially, later N=1000) and store them in
two files, one with positions and the other one with travel times,
like distances.txt and stationLUT.txt

- [x] In C++, function that given a position p = (lat,lon) and a station K
outputs the approximate travel time p->K given by: V *
dist(p,closest_station) + travel_time(closest station, p), where
closest_station is queried from KD-tree.

- [x] Compute from several days the predicted requests (origin ->
destination) for 15 minutes intervals of a day. Store it in a file.

- [x] In C++, function that given (N, time) outputs N sampled requests
from the distribution above.

- [x] Determine the expected number of requests for a given time interval

- [x] Record the expected number of requests in a day

- [x] Determine the number of taxis and save to file or something like that

- [x] Query travel times and trajectories between all of the stations

- [x] Grid of a small part of Manhattan below central part between 100 and
1000 corners. We need a graph with travel times between the corners.

- [x] A-star to search this graph in Python

- [x] Make a graph of Manhattan from 40th to 80th and 1st to Ave of the
Americas

- [x] Compute all pairs travel times and save to file

- [ ] Compute all pairs paths and save to file

- [ ] Verify that the sampling works properly

## Next
A visualization, given all the requests, positions of the
vehicles, pickups and dropoffs through out a day, visualize them on
top of a map.

# Folder name decoder
- v-[number of vehicles]-c-[capacity]-w-[waiting time]-p-[number of samples]-[day]-[week]-[year]-[date at which folder is created]
- They are in another folder that has the name until day and then organized
