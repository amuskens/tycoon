import agentsim 
class Shape():
    """
    Shape base class for simulation framework

    The visualization of the simulation uses shapes moving about on the 
    canvas panel. Each shape is a collection of artifacts on the graphics
    canvas that are manipulated as a whole.  The canvas has the coordinate
    system of the top right quadrant of the Cartesian plane. (0,0) is the
    lower left corner.

    Each Shape has a position which must lie inside the dimensions of the
    canvas. Some parts of the shape can extend outside the canvas area, and
    are clipped.

    get_xpos, set_xpos, get_xpos, set_ypos are accessors to the position.
    Set will clip the position to lie within the canvas dimensions.

    Each shape has a graphics _gstate:
      DRAWN means that the components of the shape have been rendered on the
        canvas and are visible
      ERASED means that the components of the shape have been deleted from the
        canvas.
      We do not yet support HIDDEN which would be DRAWN but not visible

    The Shape base class implements the following operations on Shape s:

    s.draw() - render the graphics artifacts associated with the shape onto
        the canvas and set the state to DRAWN.

    s.erase() - remove all graphics artifacts from the canvas and set state
        to ERASED

    s.move_by(delta_x, delta_y) - move the position of the shape on the 
        canvas by relative amounts delta_x, delta_y

    The base class move_by makes sure that positions are updated and properly
    clipped.  The derived class move_by needs to do the actual action on the 
    drawn graphic object.

    """

    # global ERASED, DRAWN
    ERASED = 0
    DRAWN = 1

    def __init__(self, 
        xpos = 0,
        ypos = 0,
        ):

        # instantiate the vars and clip
        self.set_xpos(xpos)
        self.set_ypos(ypos)

        self._gstate = Shape.ERASED

    def draw(self):
        if self._gstate != Shape.DRAWN:
            self._gstate = Shape.DRAWN
        return self

    def erase(self):
        if self._gstate != Shape.ERASED:
            self._gstate = Shape.ERASED
        return self

    # The base class move_by makes sure that positions are updated.  The
    # derived class move needs to do the actual action on the drawn
    # graphic object.

    def move_by(self, delta_x, delta_y):
        if agentsim.debug.get(4):
            print("Shape:move_by", delta_x, delta_y)

        self.set_xpos(self.get_xpos() + delta_x)
        self.set_ypos(self.get_ypos() + delta_y)
        return self

    # accessors
    def get_xpos(self):
        return self._xpos

    def get_ypos(self):
        return self._ypos

    def set_xpos(self, x):
        self._xpos = agentsim.gui.clip_x(x)
        return self._xpos

    def set_ypos(self, y):
        self._ypos = agentsim.gui.clip_y(y)
        return self._ypos
