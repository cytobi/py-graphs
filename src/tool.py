from abc import ABC, abstractmethod
import math

from debug import debug

class ToolFactory:
    @staticmethod
    def get_tool(name):
        if name == "drag":
            return DragTool()
        elif name == "select":
            return SelectTool()
        elif name == "add":
            return AddTool()
        else:
            raise ValueError("Unknown tool name: " + str(name))


class Tool(ABC):
    name = ""
    description = ""

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def handle_node_press(self, window, node, event):
        pass

    @abstractmethod
    def handle_node_release(self, window, node, event):
        pass

    @abstractmethod
    def handle_canvas_press(self, window, event):
        pass

    @abstractmethod
    def handle_canvas_release(self, window, event):
        pass


class DragTool(Tool):
    node_drag_start_x = 0
    node_drag_start_y = 0

    drag_canvas = False
    canvas_drag_start_x = 0
    canvas_drag_start_y = 0

    def __init__(self):
        super().__init__("drag", "Drag Tool")

    def handle_node_press(self, window, node, event):
        debug("Starting drag of node " + str(node.name))
        self.node_drag_start_x = event.x
        self.node_drag_start_y = event.y

    def handle_node_release(self, window, node, event):
        dx = event.x - self.node_drag_start_x
        dy = event.y - self.node_drag_start_y
        debug("Ending drag of node " + str(node.name) + " with delta of " + str((dx, dy)))
        tx, ty = window.canvas_to_unitsquare_coords(dx, dy, direction=True)
        node.x += tx
        node.y += ty
        window.update_graph()

    def handle_canvas_press(self, window, event):
        # check if a node was clicked
        drag_canvas = True
        for node in window.current_graph.nodes:
            canvas_x, canvas_y = window.unitsquare_to_canvas_coords(node.x, node.y)
            if math.dist((canvas_x, canvas_y), (event.x, event.y)) < node.radius:
                drag_canvas = False
                break
        self.drag_canvas = drag_canvas
        if self.drag_canvas:
            debug("Starting canvas drag...")
            self.canvas_drag_start_x = event.x
            self.canvas_drag_start_y = event.y

    def handle_canvas_release(self, window, event):
        if not self.drag_canvas:
            return
        dx = event.x - self.canvas_drag_start_x
        dy = event.y - self.canvas_drag_start_y
        debug("Ending canvas drag with delta of " + str((dx, dy)))
        tx, ty = window.canvas_to_unitsquare_coords(dx, dy, direction=True)
        # move nodes instead of canvas
        for node in window.current_graph.nodes:
            node.x += tx
            node.y += ty
        window.update_graph()
        self.drag_canvas = False

class SelectTool(Tool):
    def __init__(self):
        super().__init__("select", "Select Tool")

    def handle_node_press(self, window, node, event):
        debug("Selecting/Unselecting node " + str(node.name))
        node.selected = not node.selected
        window.update_graph()

    def handle_node_release(self, window, node, event):
        pass

    def handle_canvas_press(self, window, event):
        pass

    def handle_canvas_release(self, window, event):
        pass

class AddTool(Tool):
    start_node = None

    def __init__(self):
        super().__init__("add", "Add Tool")

    def handle_node_press(self, window, node, event):
        if self.start_node is None:
            self.start_node = node
            node.selected = True
            window.update_graph()
        else:
            if window.current_graph.has_edge(self.start_node, node):
                debug("Error: edge already exists between " + str(self.start_node.name) + " and " + str(node.name))
            else:
                debug("Adding edge between " + str(self.start_node.name) + " and " + str(node.name))
                window.current_graph.add_edge(self.start_node, node)
            self.start_node.selected = False
            self.start_node = None
            window.update_graph()

    def handle_node_release(self, window, node, event):
        pass

    def handle_canvas_press(self, window, event):
        pass

    def handle_canvas_release(self, window, event):
        pass
