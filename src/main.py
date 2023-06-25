import networkx as nx

from window import Window
from graph import Graph
from debug import debug


# global variables
current_graph = None


# main function
def main():
    global current_graph

    debug("Starting...")

    # setup window
    window = Window("Graph Visualizer", 800, 600)

    # setup graph
    debug("Setting up default graph...")
    default_graph = Graph(nx.complete_graph(5))
    current_graph = default_graph

    # draw graph
    current_graph.draw(window)

    # display window
    window.display()


# execute main function
if __name__ == "__main__":
    main()