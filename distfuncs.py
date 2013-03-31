import math

# Defines a Cartesian distance function. Takes two tuples in form (lat,long)
def dist(x1,y1,x2,y2):
    """
    Tests:
    >>> dist(1,1,1,2) == 1
    True
    >>> dist(3,0,0,4) == 5
    True
    >>> dist(1,1,1,1) == 0
    True
    """
    dist = math.sqrt(pow(x2-x1,2) + pow (y2-y1,2))
    return dist

if __name__ == "__main__":
    import doctest
    doctest.testmod()
