import tkinter as tk
import webbrowser

from debug import debug

class Window:
    root = None
    canvas = None
    menu = None
    sidebar = None
    canvas_padding = 20

    def __init__(self, title, width, height, canvas_padding=25):
        debug("Creating window...")
        self.canvas_padding = canvas_padding

        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(str(width) + "x" + str(height))

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.create_menu()
        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.canvas.pack()

        self.root.update()

    def create_menu(self):
        self.menu.add_command(label="About", command=self.about)
        self.menu.add_command(label="Exit", command=self.root.quit)

    def about(self):
        webbrowser.open("https://github.com/cytobi/py-graphs")
        

    def display(self):
        debug("Displaying window...")
        self.root.mainloop()

    def unitcircle_to_canvas_coords(self, x, y):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        smaller_dimension = min(canvas_width, canvas_height)
        sd_without_padding = smaller_dimension - 2*self.canvas_padding
        return canvas_width/2 + x*sd_without_padding/2, canvas_height/2 - y*sd_without_padding/2