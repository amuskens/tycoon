"""
Simple Graphical User Interface module for 2D agent simulations

You can only have one of these active, because there is only one Tk instance
that is in charge of all the windows and event handling.

To setup the simulation framework do, once only:

    agentsim.init(init_fn=None, step_fn=None, title="Simulation")

    init_fn() - is a function that is called on simulation start that
        sets up the initial conditions for the simulation.  

    step_fn() - is a function that is called on each time step of the
        simulation.  

    title is the text displayed on the top of the window

The simulation does not begin until you invoke, once only,

     agentsim.start()

The simulation environment consists of a resizable graphics area on which
visualizations of the agents are drawn and manipulated, and some controls
to start, pause, run, or single-step the simulation, along with a rate 
slider that controls the spped of the simulation.

NOTE: typing a q key will cause the simulation to quit without confirmation!

The agents being simulated need access to the state of the simulation room
and maintained by the graphical user interface.  To access the gui singleton, 
you use this global property
    agentsim.gui

To get to the canvas in order to draw additional graphics use
        canvas = agentsim.gui.get_canvas()
which resturns the canvas object, so that, for example, you can 
add additional artifacts:

    agentsim.gui.get_canvas().create_oval(10, 20, 30, 40, fill='black')

To get the dimensions of the canvas use
    (x_size, y_size) = agentsim.gui.get_canvas_size():

To get the actual coordinate space of the canvas use
    (x_min, y_min, x_max, y_max) = agentsim.gui.get_canvas_coords():

Two convenient clipping functions are provided to ensure that points
(x,y) will be clipped to be within the canvas coordinate space
        new_x = agentsim.gui.clip_x(x)
        new_y = agentsim.gui.clip_y(y)

To access the global debug flag, you use
    agentsim.debug
See the documentation for bitflag.  The framework debug flags are
    1 - agentsim related 
    2 - Person or subclass related
    4 - Shape or subclass related
    8 - reserved
   16 - (and above) user defined

BUG ALERT: It is not clear what happens when you resize the canvas during
a simulation.  The positions will eventually get clipped by a move_by, but
that may be after quite some time! 

"""

import random
from tkinter import *
from bitflag import BitFlag


# Singleton GUI instance, only one allowed to be created, remember it for
# global access.
# These are module level variables, on the grounds that the module is the
# singleton instance, the GUI class is just something used to help implement
# the module.

gui = None
debug = BitFlag()

class GUI():
    """

    Constructor:

    GUI(init_fn=None, step_fn=None, title="Simulation"):

    The GUI constructor  will raise an exception if you try to create 
    more than one instance.
    
    init_fn() - is a function that is called on simulation start that
        sets up the initial conditions for the simulation.  

    step_fn() - is a function that is called on each time step of the
        simulation.  

    title is the text displayed on the top of the window

    The simulation does not begin until you invoke agentsim.gui.start()

    To get to the canvas in order to draw additional graphics use
        canvas = agentsim.gui.get_canvas()
    which resturns the canvas object, so that, for example, you can 
    add additional artifacts:

    agentsim.gui.get_canvas().create_oval(10, 20, 30, 40, fill='black')

    To get the dimensions of the canvas use
        (x_size, y_size) = agentsim.gui.get_canvas_size():

    To get the actual coordinate space of the canvas use
        (x_min, y_min, x_max, y_max) = agentsim.gui.get_canvas_coords():

    Two convenient clipping functions are provided to ensure that points
    (x,y) will be clipped to be within the canvas coordinate space
        new_x = agentsim.gui.clip_x(x)
        new_y = agentsim.gui.clip_y(y)

    """

    # there can only be one instance of this class
    num_instances = 0

    def __init__(self, init_fn=None, step_fn=None, title="Simulation"):
        if GUI.num_instances != 0:
            raise Exception("GUI: can only have one instance of a simulation")
        GUI.num_instances = 1

        self._canvas_x_size = 500
        self._canvas_y_size = 500

        # if canvas is resized, the corners will change
        self._canvas_x_min = 0
        self._canvas_y_min = 0
        self._canvas_x_max = self._canvas_x_size
        self._canvas_y_max = self._canvas_y_size

        # simulation function hooks
        self._init_fn = init_fn
        self._step_fn = step_fn

        # simulation state
        self._running = 0

        self._title = title

        self._root = Tk()

        self._root.wm_title(title)
        self._root.wm_geometry("+100+80")
        self._root.bind("<Key-q>", self._do_shutdown)

        # create a frame on the left to hold our controls
        self._frame = Frame(self._root, relief='groove', borderwidth=2)
        self._frame.pack(side='left', fill='y')

        # Add set of buttons bound to specific actions
        #   Reset       pause and then reset the simulation by invoking init_fn
        #   One Step    do one step of the simulation by invoking step_fn
        #   Run         start a continuous simulation
        #   Pause       pause the simulation

        self._b1 = Button(self._frame,
            text='Reset',
            command=self._do_reset
            )

        self._b1.pack(anchor='w', fill='x')

        self._b2 = Button(self._frame,
            text='One Step',
            command=self._do_onestep
            )

        self._b2.pack(anchor='w', fill='x')

        self._b3 = Button(self._frame,
            text='Run',
            command=self._do_run
            )

        self._b3.pack(anchor='w', fill='x')

        self._b4 = Button(self._frame,
            text='Pause',
            command=self._do_pause
            )

        self._b4.pack(anchor='w', fill='x')

        def on_speed_change(v):
            self._speed = int(v)

        self._speed = 1
        self._speedscale = Scale(self._frame,
            from_=1, to=100, label='Speed', command=on_speed_change)
        self._speedscale.pack(side='right', fill='both', expand=1)

        self._cf = Frame(self._root)

        self._cf.pack(side='right', fill='both', expand=1)

        self._cf.grid_rowconfigure(0, weight=1)
        self._cf.grid_columnconfigure(0, weight=1)

        self._hscroll = Scrollbar(self._cf,
            orient='horizontal',
            )
        self._hscroll.grid(row=1, column=0, sticky='ew')

        self._vscroll = Scrollbar(self._cf,
            orient='vertical', 
            )

        self._vscroll.grid(row=0, column=1, sticky='ns')

        self._canvas = Canvas(self._cf,
            width=self._canvas_x_size,
            height=self._canvas_y_size,
            scrollregion=(0, 0, self._canvas_x_size, self._canvas_y_size),
            highlightthickness=0,
            borderwidth=0,
            yscrollcommand=self._vscroll.set,
            xscrollcommand=self._hscroll.set,
            )

        self._canvas.grid(column=0, row=0, sticky='nwes')

        self._hscroll.configure( command=self._canvas.xview )
        self._vscroll.configure( command=self._canvas.yview )

        def _do_resize(ev):
            self._canvas_resize(ev.width, ev.height)

        self._canvas.bind( "<Configure>", _do_resize)

    # public method to start the simulation
    def start(self):
        if self._init_fn != None: 
            self._init_fn()
        self._root.mainloop()

    # actions attached to buttons are prefixed with _do_
    def _do_shutdown(self, ev):
        print("Simulation terminated.")
        quit()

    def _do_reset(self):
        self._running = 0
        self._cancel_next_simulation()
        if self._init_fn != None:
            self._init_fn()

    def _do_onestep(self):
        self._cancel_next_simulation()
        self._running = 0
        if self._step_fn != None:
            self._step_fn()

    def _do_pause(self):
        self._running = 0
        self._cancel_next_simulation()

    def _do_run(self):
        if not self._running:
            self._running = 1
            self._run()

    # needs to be own function, not part of _do_run, 
    # because it reschedules itself
    def _run(self):
        if self._running:
            if self._step_fn != None:
                self._step_fn()
                # queue a new event to be executed after some time
                id = self._root.after(150 - self._speed, self._run)

    def _cancel_next_simulation(self):
        """ 
        remove next simulation events from the queue
        """

        data = self._root.tk.call('after', 'info')
        scripts = self._root.tk.splitlist(data)
        # In Tk 8.3, splitlist returns: (script, type)
        # In Tk 8.4, splitlist may return (script, type) or (script,)
        for id in scripts:
            self._root.after_cancel(id)
        return

    def get_canvas(self):
        return self._canvas

    def get_canvas_size(self):
        return (self._canvas_x_size, self._canvas_y_size)

    def get_canvas_coords(self):
        return (self._canvas_x_min, self._canvas_y_min,
                self._canvas_x_max, self._canvas_y_max)

    def clip_x(self, x):
        return max(self._canvas_x_min, min(self._canvas_x_max, x))

    def clip_y(self, y):
        return max(self._canvas_y_min, min(self._canvas_y_max, y))

    def _canvas_resize(self, new_x_size, new_y_size):
        """
        It is not clear what happens when you resize the canvas during
        a simulation.  The positions will eventually get clipped by a
        move_by, but that may be after quite sime time!
        """
        # don't let x get smaller than 400 or y smaller than 250

        if debug.get(1):
            print('canvas resize', new_x_size, new_y_size)

        # x only needs to be adjusted to increase
        self._canvas_x_max = max(400, new_x_size)
        self._canvas_x_size = self._canvas_x_max - self._canvas_x_min

        # y min needs to go negative since drawing axis is flipped from model 
        # axis
        self._canvas_y_max = max(250, new_y_size)
        self._canvas_y_size = self._canvas_y_max - self._canvas_y_min

        # adjust the actual size to match the model.  Thus we actually never
        # get the scrollbars enabled unless we make the canvas smaller than
        # the scroll region
        self._canvas.configure(
          scrollregion=(0, 0, self._canvas_x_size, self._canvas_y_size),
          )

        # now we also have to move all the objects that are off the canvas
        # into it, or they are in lala land.



# Agent simulation main methods


def init(init_fn=None, step_fn=None, title="Simulation"):
    # let us modify the value of the global gui variable
    global gui
    gui = GUI(init_fn=init_fn, step_fn=step_fn, title=title)


def start():
    gui.start()


def rgb_to_color(r, g, b):
    """
    Utility to generate a Tk color rgb string from  integer r, g, b, 
    where 0 <= r, g, b <= 1

    Use as in
        agentsim.gui.get_canvas().create_oval(10, 20, 30, 40, 
            fill=agentsim.rgb_to_color(.8, .8, 0) )
    """

    return '#{0:02x}{1:02x}{2:02x}'.format(
        int((r * 255) % 256), int((g * 255) % 256), int((b * 255) % 256), )
