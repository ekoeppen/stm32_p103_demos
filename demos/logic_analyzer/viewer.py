#!/usr/bin/python
# coding=iso8859-1

from Tkinter import *

def load_samples():
	global cursor_line
	canvas.delete(ALL)
	cursor_line = canvas.create_line(10, 0, 10, 10000, fill = "black", dash = (4, 4))
	f = open(sys.argv[1])
	plot(f, 0, 50, 0x01, "red")
	f.close()
	f = open(sys.argv[1])
	plot(f, 0, 55, 0x02, "black")
	f.close()

def track_mouse(event):
        canvas.coords(cursor_line, canvas.canvasx(event.x), 0, canvas.canvasx(event.x), 10000)
        cursor_pos.set("Pos: %.0fµs" % ((canvas.canvasx(event.x) * 100 /  pixel_per_microsecond)))

def next_level_change(event):
	edge = canvas.canvasx(0) + root.winfo_width()
	for c in canvas.find_withtag("c"):
		if canvas.itemcget(c, coords).x > edge:
			break
	print("Right edge: %d %.0f, item: %d" % (edge, edge * 100 / pixel_per_microsecond, c))

def update_scale_factor(value):
        global pixel_per_microsecond, scale_factor
        pixel_per_microsecond = float(value)
        scale_factor = frequency / (pixel_per_microsecond * 10000.0)

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
			canvas.create_line(x, y0, x, y, fill=color, tags = "c")

frequency = 72000000.0
update_scale_factor(1)
timer_interval = 0x01000000

root = Tk()
cursor_pos = StringVar()

topframe = Frame(root)
topframe.pack(fill = X)

scale = Scale(topframe, orient = "horizontal", length = 400, from_ = 1, to = 1000)
filler = Label(topframe)
cursor_label = Label(topframe, textvariable = cursor_pos)
quit = Button(topframe, text = "Quit", command = quit)
load = Button(topframe, text = "Reload", command = load_samples)
scale.pack(side = LEFT, fill = X, padx = 10)
cursor_label.pack(side = LEFT, padx = 10)
filler.pack(side = LEFT, expand = 1)
quit.pack(side = LEFT)
load.pack(side = LEFT, padx = 5, pady = 5)

canvas = Canvas(root, bg = "gray", width = 800, height = 480, scrollregion = (0, 0, 800000, 480))
canvas.pack(fill = BOTH, expand = 1)
hbar = Scrollbar(root, orient = HORIZONTAL)
hbar.pack(fill = X)
hbar.config(command = canvas.xview)
canvas.config(xscrollcommand = hbar.set)
canvas.bind("<Motion>", track_mouse)
root.bind("n", next_level_change)

cursor_pos.set("Pos: %.0fµs" % 0.0)
scale.set(pixel_per_microsecond)
scale.config(command = update_scale_factor)

load_samples()

root.mainloop()
