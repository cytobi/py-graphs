import tkinter as tk # gui library
import webbrowser # open links in browser
import random

from debug import debug
from graph import Graph


class Window:
    root = None # root window
    canvas = None # canvas to draw on
    menu = None # menu bar
    sidebar = None # sidebar to display properties of the graph
    current_graph = None
    canvas_padding = 20 # padding around the canvas

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
        # create canvas
        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.canvas.pack()
        # update root window
        self.root.update()

    # definition of the menu bar
    def create_menu(self):
        new_graph_menu = tk.Menu(self.menu)
        new_graph_menu.add_command(label="Complete Graph", command=self.new_complete_graph)

        self.menu.add_cascade(label="New", menu=new_graph_menu)
        self.menu.add_command(label="Reset", command=self.reset_graph)
        self.menu.add_command(label="About", command=self.about)
        self.menu.add_command(label="Exit", command=self.root.quit)

    def about(self):
        webbrowser.open("https://github.com/cytobi/py-graphs")

    def set_current_graph(self, graph):
        self.current_graph = graph

    def update_graph(self):
        self.canvas.delete("all")
        self.current_graph.draw(self)

    def reset_graph(self):
        debug("Resetting graph...")
        self.current_graph.spring_layout()
        self.update_graph()

    # displays the window, must be called at the end of the main function
    def display(self):
        debug("Displaying window...")
        self.root.mainloop()

    def new_complete_graph(self):
        debug("Creating new complete graph...")
        self.current_graph = Graph.new_complete_graph(random.randint(3, 10))
        self.update_graph()

    # helper to convert coordinates from the unit square to the canvas of this window
    def unitsquare_to_canvas_coords(self, x, y):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        smaller_dimension = min(canvas_width, canvas_height)
        sd_without_padding = smaller_dimension - 2*self.canvas_padding
        return canvas_width/2 + x*sd_without_padding/2, canvas_height/2 + y*sd_without_padding/2
    
    # helper to convert coordinates from the canvas of this window to the unit square
    def canvas_to_unitsquare_coords(self, x, y):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        smaller_dimension = min(canvas_width, canvas_height)
        sd_without_padding = smaller_dimension - 2*self.canvas_padding
        return (x - canvas_width/2)/(sd_without_padding/2), (y - canvas_height/2)/(sd_without_padding/2)
    
    # helper to convert directions from the unit square to the canvas of this window
    def unitsquare_to_canvas_direction(self, x, y):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        smaller_dimension = min(canvas_width, canvas_height)
        sd_without_padding = smaller_dimension - 2*self.canvas_padding
        return x*sd_without_padding/2, y*sd_without_padding/2
    
    # helper to convert directions from the canvas of this window to the unit square
    def canvas_to_unitsquare_direction(self, x, y):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        smaller_dimension = min(canvas_width, canvas_height)
        sd_without_padding = smaller_dimension - 2*self.canvas_padding
        return x/(sd_without_padding/2), y/(sd_without_padding/2)
