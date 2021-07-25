# workshop-mixer

## Introduction
Suppose you are organizing a networking event. You have <img src="https://render.githubusercontent.com/render/math?math=n"> Participants 
and decide to break them up into smaller groups, so they can work on some task together. After they are finished with the task they get the next task,
for which different group sizes could be neccessary. At the end of your event you want the number of tasks any two participants solved together to be
as uniform as possible.

## Example
Let's say you have 5 participants, named Albert, Bruno, Claudia, Dennis and Enrico. In your first workshop round you have a task for 3 participants
and another task for 2 participants. In the next round you have a task which 1 participant works on alone and two tasks for 2 participants each.
In the final round of your workshop you have a task for 4 participants and again a task for a single participant.

In our projects notation we write this workshop plan as follows:
```
["___|__",
 "_|__|__", 
 "____|_"]
```
Each string in this array represents a round. The repeated "_" characters mark the groupsize for a task and "|" characters separate the groups.

A solution could now be the following:
```
[['Albert', 'Bruno', 'Claudia'], ['Dennis', 'Enrico']]
[['Albert'], ['Bruno', 'Enrico'], ['Dennis', 'Claudia']]
[['Dennis', 'Bruno', 'Enrico', 'Albert'], ['Claudia']]
```
We can now look how often each participant met another participant in this solution:
```
    A B C D E
A [[0 2 1 1 1]
B  [2 0 1 1 2]
C  [1 1 0 1 0]
D  [1 1 1 0 2]
E  [1 2 0 2 0]]
```
There are two relevant 0 in this matrix (We don't count how many tasks a participant worked on with himself)
Both of them result from the fact, that Claudia and Enrico didn't work together on any task.
Sadly for the current workshop plan it will always be the case, that at least two participant didn't work together.
It will always be the participant which has a solo task in the last round, because the maximum number of participants they can work with is 3.
(2 in the first round and one in the second round).

## Optimality
Regardless how our concrete solution looks in the end the sum of the entries in the matrix will always be the same.
This can be seen by looking at the problem from a graph perspektive. Vertices in this graph are participants and for every two participants we draw a weighted
edge between them, with the weight being the number of tasks they solved together. The matrix we saw in the example is basically the adjacency matrix of this graph.

A round in this setting is a partition of the graph into cliques. When we imagine the initial graph to have all edge weights equal to 0, adding the first round
would increment all edges covered by the chosen cliques by one. As we can calculate the number of edges from the workshop plan, the sum of the matrix is equal no
matter how the participants are put together.

It therefore made sense to us to define the optimality of a solution by using the variance of the entries in the matrix.
The average of the fields in the matrix can by computed and is 1.2 for the example. Using only the variance has the problem of sometimes letting two participants
meet really often and two other participants not meeting at all.
To penalize this we multiply the variance with the difference of the maximum entry and the minimum entry.
Another thing we want to minimize is the number of zeroes in the matrix. If there is a guaranteed pair of zeroes in the matrix the difference doesn't really
enforce to minimize their count. But if it would be possible to have to participants meet under the cost of having a higher variance,
than we would prefer that solution.

The chosen function to minimize is:
`(maximum - minimum) * (variance + zero_count * maximum * maximum * 100)`. We scale the zero count with the square of the maximum,
because the variance is guaranteed to be asymptotically smaller than that. The constant factor of 100 guarantees that any decrease in zero count 
can basically cost as much variance as needed.

## Related work
We suspect, that Dagstuhls Happy Diner Problem (see https://github.com/fpvandoorn/Dagstuhl-tables) can be viewed as a special case of this problem,
but we didn't prove this yet. We also suspect this problem to be NP-hard, but would be happy if someone found a polynomial time exact algorithm for this.
Otherwise a proof for the NP-hardness would be nice.
