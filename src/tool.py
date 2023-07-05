from abc import ABC, abstractmethod

from debug import debug

class ToolFactory:
    @staticmethod
    def get_tool(name):
        if name == "drag":
            return DragTool()
        elif name == "select":
            return SelectTool()
        else:
            raise ValueError("Unknown tool name: " + str(name))


class Tool(ABC):
    name = ""
    description = ""

    def __init__(self, name, description, icon):
        self.name = name
        self.description = description
        self.icon = icon

    @abstractmethod
    def handle_node_press(self, window, node, event):
        pass

    @abstractmethod
    def handle_node_release(self, window, node, event):
        pass


class DragTool(Tool):
    drag_start_x = 0
    drag_start_y = 0

    def __init__(self):
        super().__init__("drag", "Drag Tool")

    def handle_node_press(self, window, node, event):
        debug("Starting drag of node " + str(node.name))
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def handle_node_release(self, window, node, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        debug("Ending drag of node " + str(node.name) + " with delta of " + str((dx, dy)))
        tx, ty = window.canvas_to_unitsquare_coords(dx, dy, direction=True)
        node.x += tx
        node.y += ty
        window.update_graph()

class SelectTool(Tool):
    def __init__(self):
        super().__init__("select", "Select Tool")

    def handle_node_press(self, window, node, event):
        pass

    def handle_node_release(self, window, node, event):
        pass
