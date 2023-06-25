import networkx as nx # graph library
from debug import debug

# represents a graph including its layout
class Graph:
    nx_graph = None # networkx graph
    pos = None # layout
    nodes = [] # list of nodes
    edges = [] # list of edges
    properties = {} # properties of the graph to display in the sidebar

    def __init__(self, nx_graph):
        debug("Initializing graph...")
        self.nx_graph = nx_graph
        self.pos = nx.spring_layout(nx_graph) # default layout
        # nodes is a list of Node objects constructed by passing the position of the node in the layout
        self.nodes = []
        for node in nx_graph.nodes():
            self.nodes.append(Node(node, self.pos[node][0], self.pos[node][1]))
        # edges is a list of Edge objects constructed by passing the already created node objects
        self.edges = [] 
        for edge in nx_graph.edges():
            self.edges.append(Edge(self.get_node(edge[0]), self.get_node(edge[1])))

    def get_node(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    
    def get_edge(self, node1, node2):
        for edge in self.edges:
            if (edge.node1 == node1 and edge.node2 == node2) or (edge.node1 == node2 and edge.node2 == node1):
                return edge
        return None
    
    # creates a new spring layout for this graph
    def spring_layout(self):
        self.pos = nx.spring_layout(self.nx_graph)
        for node in self.nodes:
            node.x = self.pos[node.name][0]
            node.y = self.pos[node.name][1]

    def draw(self, window):
        debug("Drawing graph...")
        for edge in self.edges:
            edge.draw(window)
        for node in self.nodes:
            node.draw(window)

    @staticmethod
    def new_complete_graph(n):
        return Graph(nx.complete_graph(n))


# represents a node including its position in a graph layout
class Node:
    name = ""
    x = 0
    y = 0

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def draw(self, window, radius=20):
        canvas_x, canvas_y = window.unitsquare_to_canvas_coords(self.x, self.y)
        circle = window.canvas.create_oval(canvas_x-radius, canvas_y-radius, canvas_x+radius, canvas_y+radius, fill="white")
        window.canvas.tag_bind(circle, "<ButtonPress-1>", self.on_drag_start)
        window.canvas.tag_bind(circle, "<ButtonRelease-1>", lambda event: self.on_drag_end(event, window))
        window.canvas.create_text(canvas_x, canvas_y, text=self.name)

    def on_drag_start(self, event):
        debug("Starting drag...")
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag_end(self, event, window):
        debug("Ending drag...")
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        tx, ty = window.canvas_to_unitsquare_direction(dx, dy)
        self.x += tx
        self.y += ty
        window.update_graph()

# represents an edge between two nodes
class Edge:
    node1 = None
    node2 = None
    weight = None

    def __init__(self, node1, node2, weight=None):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def draw(self, window):
        canvas_x1, canvas_y1 = window.unitsquare_to_canvas_coords(self.node1.x, self.node1.y)
        canvas_x2, canvas_y2 = window.unitsquare_to_canvas_coords(self.node2.x, self.node2.y)
        window.canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2)
        if self.weight is not None:
            window.canvas.create_text((canvas_x1+canvas_x2)/2, (canvas_y1+canvas_y2)/2, text=self.weight)