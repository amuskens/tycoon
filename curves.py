# curves.py
# Contains classes which represent mathematical equations of curves.
import math

# This class defines a "line equation" object, which represents
# the equation: y = mx + b
# Line equations will be used to represent supply and demand curves
class Linear():
    def __init__(self,m,b):
        # Slope
        self.m = m
        # Y intercept
        self.b = b
    
    # Evaluate the function at a point
    def evaluate(self,x):
        return self.m * x + self.b

    # Returns the angle of the line in radians. Range from -pi to pi radians
    # 0 degrees is east
    def angle(self):
        return math.atan2(self.m,1)

# This function returns the intersection point of two lines
def lines_intersect(line1,line2):
    # How it works:
    # y = m1 x + b1
    # y = m2 x + b2
    # m1 x + b1 = m2 x + b2
    # (m1 - m2) x = b2 - b1
    # x = (b2 - b1) / (m1 - m2)
    
    x = (line2.b - line1.b) / (line1.m - line2.m)
    y = line1.m * x + line1.b

    return (x,y)



# This class represents a quadratic equaion in the form:
# y = ax^2 + bx + c
class Quadratic():
    def __init__(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c

    # Evaluates the equation at a point
    def evaluate(self,x):
        return (self.a * x **2 + self.b * 2 + self.c)

    # This function returns the coordinates of the vertex of the function
    def vertex(self):
        """
        How it works:
        
        y = ax^2 + bx + c
        dy/dx = 2ax + b
        0 = 2ax + b
        -b / (2a) = x

        """

        x = -self.b / (2 * self.a)
        y = self.a * x**2 + self.b * x + self.c

        return (x,y)

    # This function returns the roots of the quadratic
    def roots(self):
        """
        How it works:

        x = (-b +/- sqrt(b^2 - 4ac)) / (2a)

        """

        # Test for complex roots. We don't want to deal with these
        if (self.b**2 - 4 * self.a * self.c) < 0:
            return None
            

        root1 = (-self.b + math.sqrt(self.b**2 - 4 * self.a * self.c)) / (self.a * 2)
        root2 = (-self.b - math.sqrt(self.b**2 - 4 * self.a * self.c)) / (self.a * 2)

        return (root1, root2)

# Returns the point of intersection between a quadratic and a line
def quad_line_intersect(quad,line):
    """
    How it works:

    mx + b1 = ax ^ 2 + bx + c
    0 = ax^2 + (b - m) x + c - B1

    Then define a new quadratic, and find the roots

    TESTS:
    >>> a = Quadratic(1,0,0)
    >>> b = Linear(0,0)
    >>> {(0, 0)} == quad_line_intersect(a,b)
    True
    """

    temp_quad = Quadratic(quad.a,quad.b - line.m,quad.c - line.b)
    roots = temp_quad.roots()

    # Just got a list of either 0, 1, or 2  roots
    int_pts = set()
    for root in roots:
        int_pts.add((root,quad.evaluate(root)))

    return int_pts

if __name__ == "__main__":
        import doctest
        doctest.testmod()
