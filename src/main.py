import tkinter as tk


window = tk.Tk()
window.title("tkinter test")
window.geometry("800x600")

menu = tk.Menu(window)
window.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New")
file_menu.add_command(label="Open")

button = tk.Button(window, text="Click me!")
button.pack()

window.mainloop()