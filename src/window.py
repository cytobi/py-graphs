import tkinter as tk # gui library
import tkinter.simpledialog # for dialogs
import webbrowser # open links in browser
import random
import math

from debug import debug
from graph import Graph
from tool import Tool, ToolFactory
from algorithm import Algorithm, TestAlgorithm


class Window:
    root = None # root window
    canvas = None # canvas to draw on
    menu = None # menu bar
    sidebar = None # sidebar to display properties of the graph

    canvas_padding = 20 # padding around the canvas
    zoom = 1 # zoom factor

    current_graph = None
    current_tool = ToolFactory.get_tool("drag")
    current_algorithm = None

    drag_canvas = False # whether the canvas is being dragged (and not a node)
    drag_start_x = 0 # x coordinate of the start of a canvas drag
    drag_start_y = 0 # y coordinate of the start of a canvas drag


    def __init__(self, title, width, height, canvas_padding=25):
        debug("Creating window...")
        self.canvas_padding = canvas_padding
        # create root window
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(str(width) + "x" + str(height))
        # create menu bar
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.create_menu()
        # create sidebar
        self.sidebar = tk.Frame(self.root, width=200, height=height, borderwidth=2, relief=tk.RAISED)
        self.sidebar.pack(side=tk.LEFT, fill=tk.BOTH)
        self.sidebar.pack_propagate(False)
        self.create_sidebar()
        # create canvas
        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        # register event handlers
        self.root.bind("<<UpdateGraph>>", lambda event: self.update_graph())
        self.root.bind_all("<MouseWheel>", self.zoom_canvas) # windows zoom
        self.root.bind_all("<Button-4>", self.zoom_canvas) # linux zoom
        self.root.bind_all("<Button-5>", lambda event: self.zoom_canvas(event, invert=True)) # linux zoom
        self.canvas.bind("<ButtonPress-1>", self.handle_canvas_press)
        self.canvas.bind("<ButtonRelease-1>", self.handle_canvas_release)
        # update root window
        self.root.update()

    # definition of the menu bar
    def create_menu(self):
        new_graph_menu = tk.Menu(self.menu)
        new_graph_menu.add_command(label="Complete Graph", command=self.new_complete_graph)

        self.menu.add_cascade(label="New", menu=new_graph_menu)
        self.menu.add_command(label="Reset", command=self.reset_graph)
        self.menu.add_command(label="Algorithm", command=self.run_algorithm)
        self.menu.add_command(label="Step", command=self.step_algorithm)
        self.menu.add_command(label="About", command=self.about)
        self.menu.add_command(label="Exit", command=self.exit)

    # definition of the sidebar
    def create_sidebar(self):
        # tool frame
        tools_height = 40
        tools = tk.Frame(self.sidebar, width=200, height=tools_height)
        tools.pack(side=tk.TOP, fill=tk.BOTH)
        tools.pack_propagate(False)
        # divider below tools
        self.divider(tools, width=200, horizontal=True)
        # buttons for tools
        drag_image = tk.PhotoImage(file="assets/drag.png").subsample(22, 22)
        drag_button = tk.Button(tools, image=drag_image, command=lambda: self.set_current_tool("drag"))
        drag_button.image = drag_image # prevent garbage collection by keeping a reference
        drag_button.pack(side=tk.LEFT, padx=5, pady=5)
        select_image = tk.PhotoImage(file="assets/select.png").subsample(25, 25)
        select_button = tk.Button(tools, image=select_image, command=lambda: self.set_current_tool("select"))
        select_button.image = select_image # prevent garbage collection by keeping a reference
        select_button.pack(side=tk.LEFT, padx=0, pady=5)
        add_button = tk.Button(tools, text="+", command=lambda: self.set_current_tool("add"))
        add_button.pack(side=tk.LEFT, padx=5, pady=5)
        # draw properties text field
        properties = tk.Text(self.sidebar, yscrollcommand=True)
        properties.pack(side=tk.BOTTOM, fill=tk.BOTH)
        properties.insert(tk.END, "Properties of the graph will be displayed here.")
        self.sidebar.properties = properties # make text field accessible from outside

    def about(self):
        webbrowser.open("https://github.com/cytobi/py-graphs")

    def exit(self):
        debug("Exiting...")
        if self.current_algorithm is not None:
            self.current_algorithm.kill()
        self.root.quit()


    # graph handling
    def set_current_graph(self, graph):
        self.current_graph = graph

    def update_graph(self):
        self.canvas.delete("all")
        self.current_graph.calculate_properties()
        self.current_graph.draw(self)

    def reset_graph(self):
        debug("Resetting graph: " + str(self.current_graph))
        self.zoom = 1 # reset zoom
        self.current_graph.spring_layout()
        self.update_graph()

    # all things that need to be cleaned up when a new graph is created
    def clean_up_old_graph(self):
        if self.current_algorithm is not None:
            self.current_algorithm.kill()


    def update_properties(self):
        debug("Updating properties in sidebar...")
        properties = self.current_graph.properties
        text = ""
        for key in properties:
            text += key + ": " + str(properties[key]) + "\n"
        self.sidebar.properties.delete("1.0", tk.END)
        self.sidebar.properties.insert(tk.END, text)

    def set_current_tool(self, tool):
        debug("Setting current tool to " + str(tool))
        self.current_tool = ToolFactory.get_tool(tool)

    # displays the window, must be called at the end of the main function
    def display(self):
        debug("Displaying window: " + str(self))
        self.root.mainloop()


    # new graphs
    def new_complete_graph(self):
        n = tk.simpledialog.askinteger("New Complete Graph", "Enter number of nodes:", parent=self.root)
        if n is None:
            return
        if n < 1:
            debug("Invalid number of nodes: " + str(n))
            return
        debug("Creating new complete graph with " + str(n) + " nodes")
        self.clean_up_old_graph()
        self.current_graph = Graph.new_complete_graph(n)
        self.update_graph()


    # algorithms
    def run_algorithm(self):
        self.current_algorithm = TestAlgorithm(self)
        self.current_algorithm.start(self.current_graph)

    def step_algorithm(self):
        if self.current_algorithm is None:
            debug("No algorithm initialized")
            return
        self.current_algorithm.step()


    # event handlers
    # event handler for zooming the canvas
    def zoom_canvas(self, event, invert=False):
        if (event.delta > 0) is invert:
            self.zoom *= 1.1
        else:
            self.zoom /= 1.1
        debug("Zooming canvas to " + str(self.zoom))
        self.update_graph()

    # event handlers for grabbing the canvas
    def handle_canvas_press(self, event):
        self.current_tool.handle_canvas_press(self, event)

    def handle_canvas_release(self, event):
        self.current_tool.handle_canvas_release(self, event)


    # helpers
    # helper to convert coordinates and directions from the unit square to the canvas of this window
    def unitsquare_to_canvas_coords(self, x, y, direction=False):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        smaller_dimension = min(canvas_width, canvas_height)
        sd_without_padding = smaller_dimension - 2*self.canvas_padding
        zoomed_half = sd_without_padding/2*self.zoom
        if direction:
            return x*zoomed_half, y*zoomed_half
        else:
            return canvas_width/2 + x*zoomed_half, canvas_height/2 + y*zoomed_half
    
    # helper to convert coordinates and directions from the canvas of this window to the unit square
    def canvas_to_unitsquare_coords(self, x, y, direction=False):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        smaller_dimension = min(canvas_width, canvas_height)
        sd_without_padding = smaller_dimension - 2*self.canvas_padding
        zoomed_half = sd_without_padding/2*self.zoom
        if direction:
            return x/zoomed_half, y/zoomed_half
        else:
            return (x - canvas_width/2)/zoomed_half, (y - canvas_height/2)/zoomed_half
        
    # helper for creating a divider with tkinter, divider is placed on right/bottom of parent and should be the first element
    def divider(self, parent, height=2, width=2, horizontal=True):
        canvas = tk.Canvas(parent, width=width, height=height)
        if horizontal:
            canvas.create_line(0, height/2, width, height/2)
            canvas.pack(side=tk.BOTTOM, fill=tk.BOTH)
        else:
            canvas.create_line(width/2, 0, width/2, height)
            canvas.pack(side=tk.RIGHT, fill=tk.BOTH)
