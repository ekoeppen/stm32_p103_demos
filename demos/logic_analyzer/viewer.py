#!/usr/bin/python

from Tkinter import *

def load():
    return 0

def track_mouse(event):
    canvas.coords(cursor_line, event.x, 0, event.x, 10000)
    cursor_pos.set("Pos: %.3f" % (event.x * scale_factor))

frequency = 72000000
pixel_per_microsecond = 100
scale_factor = (pixel_per_microsecond * 1000000.0) / frequency

root = Tk()
cursor_pos = StringVar()

topframe = Frame(root)
topframe.pack()

scale = Scale(topframe, orient = "horizontal")
cursor_label = Label(topframe, textvariable = cursor_pos)
quit = Button(topframe, text = "Quit", command = quit)
load = Button(topframe, text = "Reload", command = load)
scale.pack(side = LEFT, fill = X, expand = 1)
cursor_label.pack(side = LEFT, padx = 10)
quit.pack(side = RIGHT)
load.pack(side = RIGHT, padx = 5, pady = 5)

canvas = Canvas(root, bg = "gray")
canvas.pack(fill = BOTH, expand = 1)
canvas.bind("<Motion>", track_mouse)
cursor_line = canvas.create_line(10, 0, 10, 10000, fill = "black", dash = (4, 4))

cursor_pos.set("Pos: %.3f" % 0.0)

root.mainloop()