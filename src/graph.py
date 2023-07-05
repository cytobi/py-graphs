import networkx as nx # graph library
import math
from debug import debug

# represents a graph including its layout
class Graph:
    nx_graph = None # networkx graph
    nodes = [] # list of nodes
    edges = [] # list of edges
    properties = {} # properties of the graph to display in the sidebar

    def __init__(self, nx_graph):
        debug("Initializing graph: " + str(self))
        self.nx_graph = nx_graph
        pos = nx.spring_layout(nx_graph) # default layout
        # nodes is a list of Node objects constructed by passing the position of the node in the layout
        self.nodes = []
        for node in nx_graph.nodes():
            self.nodes.append(Node(node, pos[node][0], pos[node][1]))
        # edges is a list of Edge objects constructed by passing the already created node objects
        self.edges = [] 
        for edge in nx_graph.edges():
            self.edges.append(Edge(self.get_node(edge[0]), self.get_node(edge[1])))
        # properties is a dictionary of properties to display in the sidebar
        self.calculate_properties()

    def get_node(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    
    def add_node(self, x, y, name=None):
        if name is None:
            name = str(len(self.nx_graph.nodes()))
        self.nx_graph.add_node(name)
        self.nodes.append(Node(name, x, y))
    
    def get_edge(self, node1, node2):
        for edge in self.edges: # get edge between node1 and node2 or node2 and node1 if undirected
            if (edge.node1 == node1 and edge.node2 == node2) or (edge.node1 == node2 and edge.node2 == node1 and not edge.directed):
                return edge
        return None
    
    def has_edge(self, node1, node2):
        return self.get_edge(node1, node2) is not None
    
    def add_edge(self, node1, node2, weight=None, color="black", directed=False):
        self.nx_graph.add_edge(node1.name, node2.name)
        self.edges.append(Edge(node1, node2, weight, color, directed))
    
    # creates a new spring layout for this graph
    def spring_layout(self):
        pos = nx.spring_layout(self.nx_graph)
        for node in self.nodes:
            node.x = pos[node.name][0]
            node.y = pos[node.name][1]

    def calculate_properties(self):
        debug("Calculating properties of graph: " + str(self))
        self.properties = {"nodes": len(self.nx_graph.nodes()),
                           "edges": len(self.nx_graph.edges()),
                           "density": nx.density(self.nx_graph),
                           "planar": nx.is_planar(self.nx_graph),
                           "empty": nx.is_empty(self.nx_graph),
                           "connected": nx.is_connected(self.nx_graph),
                           "directed": nx.is_directed(self.nx_graph),
                           "bipartite": nx.is_bipartite(self.nx_graph),
                           "tree": nx.is_tree(self.nx_graph),
                           "forest": nx.is_forest(self.nx_graph),
                           "eulerian": nx.is_eulerian(self.nx_graph),
                           "regular": nx.is_regular(self.nx_graph),
                           }

    def draw(self, window):
        debug("Drawing graph: " + str(self.nx_graph))
        for edge in self.edges:
            edge.draw(window)
        for node in self.nodes:
            node.draw(window)
        window.update_properties()

    @staticmethod
    def new_complete_graph(n):
        return Graph(nx.complete_graph(n))


# represents a node including its position in a graph layout
class Node:
    name = ""
    x = 0
    y = 0
    radius = 20 # last radius used to draw the node
    color = "white"
    selected = False # whether the node is currently selected

    def __init__(self, name, x, y, color="white"):
        self.name = name
        self.x = x
        self.y = y
        self.color = color

    def draw(self, window, radius=20):
        self.radius = radius
        outline = "black"
        outline_width = 1
        if self.selected:
            outline = "blue"
            outline_width = 3
        canvas_x, canvas_y = window.unitsquare_to_canvas_coords(self.x, self.y)
        circle = window.canvas.create_oval(canvas_x-radius, canvas_y-radius, canvas_x+radius, canvas_y+radius, fill=self.color, outline=outline, width=outline_width)
        self.bind_actions(window, circle)
        label = window.canvas.create_text(canvas_x, canvas_y, text=self.name)
        self.bind_actions(window, label) # bind actions to label as well

    # bindings to handle events on node
    def bind_actions(self, window, bind_to):
        window.canvas.tag_bind(bind_to, "<ButtonPress-1>", lambda event: self.handle_press(event, window))
        window.canvas.tag_bind(bind_to, "<ButtonRelease-1>", lambda event: self.handle_release(event, window))

    def handle_press(self, event, window):
        debug("Node " + str(self.name) + " pressed")
        window.current_tool.handle_node_press(window, self, event)

    def handle_release(self, event, window):
        debug("Node " + str(self.name) + " released")
        window.current_tool.handle_node_release(window, self, event)

    def on_drag_start(self, event):
        debug("Starting drag of node " + str(self.name))
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag_end(self, event, window):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        debug("Ending drag of node " + str(self.name) + " with delta of " + str((dx, dy)))
        tx, ty = window.canvas_to_unitsquare_coords(dx, dy, direction=True)
        self.x += tx
        self.y += ty
        window.update_graph()

# represents an edge between two nodes
class Edge:
    node1 = None
    node2 = None
    weight = None
    directed = False

    color = "black"

    def __init__(self, node1, node2, weight=None, color="black", directed=False):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
        self.color = color
        self.directed = directed

    def draw(self, window):
        canvas_x1, canvas_y1 = window.unitsquare_to_canvas_coords(self.node1.x, self.node1.y)
        canvas_x2, canvas_y2 = window.unitsquare_to_canvas_coords(self.node2.x, self.node2.y)
        if self.directed: # create two lines to draw arrow markings at halfway point
            window.canvas.create_line(canvas_x1, canvas_y1, (canvas_x1+canvas_x2)/2, (canvas_y1+canvas_y2)/2, arrow="last", fill=self.color)
            window.canvas.create_line((canvas_x1+canvas_x2)/2, (canvas_y1+canvas_y2)/2, canvas_x2, canvas_y2, fill=self.color)
        else:
            window.canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill=self.color)
        if self.weight is not None:
            vector = (canvas_x2-canvas_x1, canvas_y2-canvas_y1) # vector from node1 to node2
            length = math.sqrt(vector[0]**2 + vector[1]**2) # length of vector
            vector = (vector[0]/length, vector[1]/length) # normalize vector
            rotated = (vector[0]*math.cos(math.pi/2)-vector[1]*math.sin(math.pi/2), vector[0]*math.sin(math.pi/2)+vector[1]*math.cos(math.pi/2)) # rotate vector by 90 degrees
            # calculate label position
            label_x = (canvas_x1+canvas_x2)/2 + rotated[0]*15 
            label_y = (canvas_y1+canvas_y2)/2 + rotated[1]*15
            window.canvas.create_text(label_x, label_y, text=self.weight)