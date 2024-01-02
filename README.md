### Background
According to the `Six Degrees of Kevin Bacon` game, anyone in the Hollywood film industry can be connected to Kevin Bacon within six steps, where each step consists of finding a film that two actors both starred in.


### Objective
- In this problem, we’re interested in comparing the times(of different algorithms) to get the shortest path between any two actors by choosing a sequence of movies that connects them. 
- For example, the shortest path between Jennifer Lawrence and Tom Hanks is 2: Jennifer Lawrence is connected to Kevin Bacon by both starring in “X-Men: First Class,” and Kevin Bacon is connected to Tom Hanks by both starring in “Apollo 13.”


### Algorithms Considered
- BFS
- Djikstra
- Bellman-Ford
- Floyd-Warshall

### Overview of Procedure
- We are framing this as a Search Problem. 
- Our initial state and goal state are defined by the two people we’re trying to connect. 
- Implement the shortest path in each of the algorithms.
- Compare the timings to execute those algorithm.
- Write notes on the timings and the general guidelines on which algorithm to choose.
