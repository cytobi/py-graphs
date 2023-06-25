import networkx as nx

from window import Window
from graph import Graph

# global variables
current_graph = None

# helper functions
def debug(to_print):
    if __debug__:
        print(to_print)


# main function
def main():
    global current_graph

    debug("Starting...")

    # setup tkinter
    debug("Starting GUI...")
    window = Window("Graph Visualizer", 800, 600)

    # setup graph
    debug("Setting up default graph...")
    default_graph = Graph(nx.complete_graph(5))
    current_graph = default_graph

    # draw graph
    current_graph.draw(window)

    # display tkinter
    debug("Displaying GUI...")
    window.display()


# execute main function
if __name__ == "__main__":
    main()