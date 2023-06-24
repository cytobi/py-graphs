import networkx as nx
import tkinter as tk
import random

# global variables
current_graph = None
canvas = None

# helper functions
def debug(to_print):
    if __debug__:
        print(to_print)

def setup_graph(G):
    debug("Setting up graph...")
    pos = nx.spring_layout(G, scale=250, center=(400, 300))
    return pos

def draw_graph(G, pos, canvas):
    debug("Drawing graph...")
    for edge in G.edges():
        x1, y1 = pos[edge[0]]
        x2, y2 = pos[edge[1]]
        canvas.create_line(x1, y1, x2, y2)

    for node in pos:
        x, y = pos[node]
        canvas.create_oval(x-20, y-20, x+20, y+20, fill="white")
        canvas.create_text(x, y, text=node)

def new_complete_graph():
    global current_graph, canvas

    debug("Clearing canvas...")
    canvas.delete("all")

    debug("Creating new complete graph...")
    current_graph = nx.complete_graph(random.randint(2, 10))
    pos = setup_graph(current_graph)
    draw_graph(current_graph, pos, canvas)


# main function
def main():
    global current_graph, canvas

    debug("Starting...")

    # setup tkinter
    debug("Starting GUI...")
    root = tk.Tk()
    root.title("Graph Visualizer")
    root.geometry("800x600")

    menu = tk.Menu(root)
    root.config(menu=menu)
    menu.add_command(label="New", command=new_complete_graph)
    menu.add_command(label="Exit", command=root.quit)

    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack()

    # setup graph
    debug("Setting up default graph...")
    default_graph = nx.complete_graph(5)
    current_graph = default_graph
    pos = setup_graph(current_graph)

    # draw graph
    draw_graph(current_graph, pos, canvas)

    # display tkinter
    debug("Displaying GUI...")
    root.mainloop()


# execute main function
if __name__ == "__main__":
    main()