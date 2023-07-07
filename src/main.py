from window import Window
from graph import Graph
from debug import setup_debug, debug


# main function
def main():
    setup_debug()

    debug("Starting...")

    # setup window
    window = Window("Tarvos Graph Visualizer", 800, 600)

    # setup graph
    debug("Setting up default graph...")
    default_graph = Graph.new_complete_graph(5)
    window.set_current_graph(default_graph)

    # draw graph
    window.update_graph()

    # display window
    window.display()


# execute main function
if __name__ == "__main__":
    main()