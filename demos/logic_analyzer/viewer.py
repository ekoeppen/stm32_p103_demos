#!/usr/bin/python
# coding=iso8859-1

from Tkinter import *

def load():
        return 0

def track_mouse(event):
        canvas.coords(cursor_line, event.x, 0, event.x, 10000)
        cursor_pos.set("Pos: %.3fµs" % (event.x /  pixel_per_microsecond))

def update_scale_factor(value):
        global pixel_per_microsecond, scale_factor
        pixel_per_microsecond = float(value)
        scale_factor = frequency / (pixel_per_microsecond * 1000000.0)

def plot(f, x_offset, y_offset, mask, color):
	global canvas, timer_interval, scale_factor
	t = 0
	x = x_offset
	y = y_offset
	for line in f:
		what = (int(line, 16) >> 24) & 0xff
		timestamp = timer_interval - (int(line, 16) & 0x00ffffff)
		if what & 0x80:
			t += timer_interval
		else:
			x0 = x
			y0 = y
			if what & mask:
				y = y_offset
			else:
				y = y_offset + 50
			if t == 0:
				t = -timestamp
			x = (t + timestamp) / scale_factor + x_offset
			canvas.create_line(x0, y0, x, y0, fill=color)
			canvas.create_line(x, y0, x, y, fill=color)

frequency = 72000000.0
update_scale_factor(10)
timer_interval = 0x01000000

root = Tk()
cursor_pos = StringVar()

topframe = Frame(root)
topframe.pack()

scale = Scale(topframe, orient = "horizontal", length = 400, resolution = 10, from_ = 10, to = 500)
cursor_label = Label(topframe, textvariable = cursor_pos)
quit = Button(topframe, text = "Quit", command = quit)
load = Button(topframe, text = "Reload", command = load)
scale.pack(side = LEFT, fill = X, expand = 1)
cursor_label.pack(side = LEFT, padx = 10)
quit.pack(side = RIGHT)
load.pack(side = RIGHT, padx = 5, pady = 5)

canvas = Canvas(root, bg = "gray", width = 800, height = 480, scrollregion = (0, 0, 800000, 480))
canvas.pack(fill = BOTH, expand = 1)
hbar = Scrollbar(root, orient = HORIZONTAL)
hbar.pack(fill = X)
hbar.config(command = canvas.xview)
canvas.config(xscrollcommand = hbar.set)
canvas.bind("<Motion>", track_mouse)

cursor_line = canvas.create_line(10, 0, 10, 10000, fill = "black", dash = (4, 4))

cursor_pos.set("Pos: %.3fµs" % 0.0)
scale.set(pixel_per_microsecond)
scale.config(command = update_scale_factor)

f = open(sys.argv[1])
plot(f, 0, 50, 0x01, "red")
f.close()

f = open(sys.argv[1])
plot(f, 0, 55, 0x02, "black")
f.close()

root.mainloop()
