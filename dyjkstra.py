from digraph import Digraph,compress

# Define a cost testing function
def costTest(e):
    return 1

# Define Dyjkstra's algorithm. G is a digraph, cost is a cost function.
def least_cost_path(G,start,dest,cost):
    """ 
    Tests:
    
    Typical valid path:
    >>> G = Digraph(((1,2),(1,4),(2,3),(3,4),(4,5),(3,5),(2,4),(7,9)))
    >>> least_cost_path(G,1,5,costTest)
    [1, 4, 5]
    >>> least_cost_path(G,3,5,costTest)
    [3, 5]

    Disconnected path:
    >>> least_cost_path(G,1,9,costTest) == None
    True
    >>> least_cost_path(G,3,7,costTest) == None
    True

    Start and end are the same:
    >>> least_cost_path(G,1,1,costTest) == [1]
    True
    >>> least_cost_path(G,2,2,costTest) == [2]
    True

    Start and end don't exist in the graph:
    >>> least_cost_path(G,1000,1024,costTest) == None
    True
    """

    # Check to see if the ID's are valid before proceeding:
    if not start in G.vertices() or not dest in G.vertices():
        return None

    # End early if the start and dest are the same
    if start == dest:
        return [start]

    # todo[v] is the current best estimate of cost to get from start to v 
    todo = { start: 0}

    # v in visited when the vertex v's least cost from start has been determined
    visited = set()

    # parent[v] is the vertex that just precedes v in the path from start to v
    parent = {}

    # Path list
    path = []

    # Cost at the current node.
    c = 0

    while todo:

        # priority queue operation
        # remove smallest estimated cost vertex from todo list
        # this is not the efficient heap form, but it works
        # because it mins on the cost (2nd) field of the tuple of
        # items from the todo dictionary

        (cur,c) = min(todo.items(), key=lambda x: x[1])
        todo.pop(cur)

        # it is now visited, and will never have a smaller cost
        visited.add(cur)

        for n in G.adj_to(cur):
            if n in visited: continue
            if n not in todo or ( c + cost((cur,n)) < todo[n]):
                todo[n] = c + cost((cur,n))
                parent[n] = cur

    # now, if there is a path, extract it.  The graph may be disconnected, so return none if it is
    trace = dest
    breakflag = 0

    # We don't want to try trace back beyond the first element of the list.
    while True:
        path.insert(0,trace)
        if trace == start:
            breakflag = 1
            break
        # If there is a key error, then the path is disconnected.
        if trace in parent.keys():
            trace = parent[trace]
        else:
            break
    
    # Breakflag is true if a valid path is found
    if breakflag:
        return path
    else:
        return None

if __name__ == "__main__":
    import doctest
    doctest.testmod()
