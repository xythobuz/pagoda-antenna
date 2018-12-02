# You should run this script with Python 3. Python 2 is not supported and will generate incorrect results.
# The following lines of code will trigger a syntax error in Python 2, this is intentional. It avoids confusion for
# users who would otherwise be confronted with a dozen unrelated syntax errors before they understand the actual problem.
def foo():
	a = 0
	def bar():
		"DO NOT RUN THIS WITH PYTHON 2! USE PYTHON 3 INSTEAD! PYTHON 2 WILL GENERATE INCORRECT RESULTS!"; nonlocal a

from pylab import *
import os
import subprocess

import mbpcb

#import imp
#imp.reload(mbpcb)

# simulation: balun-test-v12-l80.hfss
# simulation: balun-test-v12-l80.hfss

# versions:
# "3"  = default version, optimized for use without any protective shell
# "3B" = optimized for use with a 1.0 mm ABS shell (for MenaceRC)

close("all")

oshw_x = array([
	 0.28885504,  0.10469736,  0.13888441,  0.17044261,  0.19877461,  0.22334415,  0.24368615,  0.25941557,
	 0.27023469,  0.27593872,  0.27641969,  0.27166849,  0.26177506,  0.24692667,  0.22740436,  0.20357767,
	 0.17589759,  0.14488807,  0.11113605,  0.07528041,  0.03799984,  0.        , -0.03799984, -0.07528041,
	-0.11113605, -0.14488807, -0.17589759, -0.20357767, -0.22740436, -0.24692667, -0.26177506, -0.27166849,
	-0.27641969, -0.27593872, -0.27023469, -0.25941557, -0.24368615, -0.22334415, -0.19877461, -0.17044261,
	-0.13888441, -0.10469736, -0.28885504, -0.38204406, -0.60348636, -0.79737332, -0.64548688, -0.7265741 ,
	-0.99055738, -0.99055738, -0.7265741 , -0.64548688, -0.79737332, -0.60348636, -0.38204406, -0.1862822 ,
	-0.13709878,  0.13709878,  0.1862822 ,  0.38204406,  0.60348636,  0.79737332,  0.64548688,  0.7265741 ,
	 0.99055738,  0.99055738,  0.7265741 ,  0.64548688,  0.79737332,  0.60348636,  0.38204406,
])
oshw_y = array([
	-0.70711199, -0.25629728, -0.23950146, -0.21817229, -0.19271348, -0.16360692, -0.13140355, -0.09671293,
	-0.0601917 , -0.02253114,  0.01555589,  0.05334848,  0.09013127,  0.12520803,  0.15791481,  0.18763252,
	 0.21379866,  0.23591795,  0.2535717 ,  0.26642577,  0.27423684,  0.27685706,  0.27423684,  0.26642577,
	 0.2535717 ,  0.23591795,  0.21379866,  0.18763252,  0.15791481,  0.12520803,  0.09013127,  0.05334848,
	 0.01555589, -0.02253114, -0.0601917 , -0.09671293, -0.13140355, -0.16360692, -0.19271348, -0.21817229,
	-0.23950146, -0.25629728, -0.70711199, -0.64548688, -0.79737332, -0.60348636, -0.38204406, -0.1862822 ,
	-0.13709878,  0.13709878,  0.1862822 ,  0.38204406,  0.60348636,  0.79737332,  0.64548688,  0.7265741 ,
	 0.99055738,  0.99055738,  0.7265741 ,  0.64548688,  0.79737332,  0.60348636,  0.38204406,  0.1862822 ,
	 0.13709878, -0.13709878, -0.1862822 , -0.38204406, -0.60348636, -0.79737332, -0.64548688,
])

def polygon_arc(shapes, cx, cy, radius, angle):
	res = []
	for shape in shapes:
		if shape["type"] == "polygon":
			r = radius + shape["y"]
			theta = angle * pi / 180 - shape["x"] / radius
			(shape["x"], shape["y"]) = (cx + r * cos(theta), cy + r * sin(theta))

@mbpcb.register
def pcb1(pol):
	shapes = []
	shapes += mbpcb.make_circle("board-outline", 0.0, 0.0, pcb_r1)
	
	# coax connection
	shapes += mbpcb.make_circle("drill-plated", 0.0, 0.0, coax_r1 + hole_sp, pad=True)
	shapes += mbpcb.make_circle("copper1-top", 0.0, 0.0, coax_r1 + solder_w)
	shapes += mbpcb.make_circle("copper1-bot", 0.0, 0.0, coax_r3 + solder_w, pad=True)
	shapes += mbpcb.make_circle("copper1-bot", 0.0, 0.0, coax_r2, hole=True, pad=True)
	shapes += mbpcb.make_circle("copper1-bot", 0.0, 0.0, coax_r1 + hole_sp + ring_w, pad=True, order=1)
	shapes += mbpcb.make_circle("mask-top", 0.0, 0.0, coax_r1 + solder_w + mask_sp)
	shapes += mbpcb.make_circle("mask-bot", 0.0, 0.0, coax_r3 + solder_w + mask_sp, pad=True)
	shapes += mbpcb.make_circle("mask-bot", 0.0, 0.0, coax_r2 - mask_sp, hole=True, pad=True)
	shapes += mbpcb.make_circle("mask-bot", 0.0, 0.0, coax_r1 + hole_sp + ring_w + mask_sp, pad=True, order=1)
	
	# ring
	#shapes += mbpcb.make_arc("copper1-top", 0.0, 0.0, (hole_r1 + disk_r1) / 2, 0.0, 360.0, outline=disk_r1 - hole_r1)
	shapes += mbpcb.make_circle("copper1-top", 0.0, 0.0, (hole_r1 + disk_r1) / 2, outline=disk_r1 - hole_r1)
	
	# legs
	for angle in arange(3) * 120 + 90:
		if pol == "LHCP":
			a1 = angle + track_b1 - (track_w2 - track_w1) / 2.0 / track_r1
			a2 = a1 + track_a1
			a3 = angle + track_b1
			a4 = angle + track_b1 + track_c1
		else:
			a1 = angle - track_b1 + (track_w2 - track_w1) / 2.0 / track_r1
			a2 = a1 - track_a1
			a3 = angle - track_b1
			a4 = angle - track_b1 - track_c1
		a5 = angle + 60.0
		shapes += mbpcb.make_arc("copper1-top", 0.0, 0.0, track_r1, a1, a2, outline=track_w1)
		shapes += mbpcb.make_arc("copper1-top", 0.0, 0.0, track_r2, a3, a4, outline=track_w1)
		shapes += mbpcb.make_line("copper1-top",
				track_r1 * cos(a3 * pi/180), track_r1 * sin(a3 * pi/180),
				track_r2 * cos(a3 * pi/180), track_r2 * sin(a3 * pi/180), outline=track_w2)
		shapes += mbpcb.make_line("copper1-top",
				disk_r1  * cos(a4 * pi/180), disk_r1  * sin(a4 * pi/180),
				track_r2 * cos(a4 * pi/180), track_r2 * sin(a4 * pi/180), outline=track_w2)
		shapes += mbpcb.make_line("copper1-top", 0.0, 0.0,
				hole_r1 * cos(a5 * pi/180), hole_r1 * sin(a5 * pi/180), outline=track_w2)
		shapes += mbpcb.make_line("silk-top",
				track_r1 * cos(angle * pi/180), track_r1 * sin(angle * pi/180),
				track_r2 * cos(angle * pi/180), track_r2 * sin(angle * pi/180), outline=0.2)
		shapes += mbpcb.make_line("silk-bot",
				track_r1 * cos(angle * pi/180), track_r1 * sin(angle * pi/180),
				track_r2 * cos(angle * pi/180), track_r2 * sin(angle * pi/180), outline=0.2)
	
	# text
	shapes += mbpcb.make_text("silk-top", "fonts/Salsa.ttf", pol, 1.8,
			0.0, 5.5, align="center", valign="center", spacing=0.05)
	shapes += mbpcb.make_text("silk-top", "fonts/Salsa.ttf", "Pagoda-" + version, fontsize1,
			0.0, 3.0, align="center", valign="center", spacing=0.05)
	shapes += mbpcb.make_text("silk-top", "fonts/Salsa.ttf", "Designed by", 1.8,
			0.0, -2.0, align="center", valign="center", spacing=0.05)
	shapes += mbpcb.make_text("silk-top", "fonts/Salsa.ttf", "Maarten", 1.8,
			0.0, -4.0, align="center", valign="center", spacing=0.05)
	shapes += mbpcb.make_text("silk-top", "fonts/Salsa.ttf", "Baert", 1.8,
			0.0, -6.0, align="center", valign="center", spacing=0.05)
	
	return shapes

@mbpcb.register
def pcb2(pol):
	shapes = []
	shapes += mbpcb.make_circle("board-outline", 0.0, 0.0, pcb_r1)
	
	# coax connection
	shapes += mbpcb.make_circle("drill-plated", 0.0, 0.0, coax_r3 + hole_sp2, pad=True)
	shapes += mbpcb.make_circle("copper1-top", 0.0, 0.0, coax_r3 + solder_w, pad=True)
	shapes += mbpcb.make_circle("copper1-bot", 0.0, 0.0, coax_r3 + solder_w, pad=True)
	shapes += mbpcb.make_circle("mask-top", 0.0, 0.0, coax_r3 + solder_w + mask_sp, pad=True)
	shapes += mbpcb.make_circle("mask-bot", 0.0, 0.0, coax_r3 + solder_w + mask_sp, pad=True)
	
	# ring
	#shapes += mbpcb.make_arc("copper1-top", 0.0, 0.0, (hole_r2 + disk_r2) / 2, 0.0, 360.0, outline=disk_r2 - hole_r2)
	shapes += mbpcb.make_circle("copper1-top", 0.0, 0.0, (hole_r2 + disk_r2) / 2, outline=disk_r2 - hole_r2)
	
	# legs
	for angle in arange(3) * 120 + 90:
		if pol == "LHCP":
			a1 = angle - track_b1 + (track_w2 - track_w1) / 2.0 / track_r1
			a2 = a1 - track_a1
			a3 = angle - track_b1
			a4 = angle - track_b1 - track_c1
		else:
			a1 = angle + track_b1 - (track_w2 - track_w1) / 2.0 / track_r1
			a2 = a1 + track_a1
			a3 = angle + track_b1
			a4 = angle + track_b1 + track_c1
		a5 = angle + 60.0
		shapes += mbpcb.make_arc("copper1-top", 0.0, 0.0, track_r1, a1, a2, outline=track_w1)
		shapes += mbpcb.make_arc("copper1-top", 0.0, 0.0, track_r2, a3, a4, outline=track_w1)
		shapes += mbpcb.make_line("copper1-top",
				track_r1 * cos(a3 * pi/180), track_r1 * sin(a3 * pi/180),
				track_r2 * cos(a3 * pi/180), track_r2 * sin(a3 * pi/180), outline=track_w2)
		shapes += mbpcb.make_line("copper1-top",
				disk_r2  * cos(a4 * pi/180), disk_r2  * sin(a4 * pi/180),
				track_r2 * cos(a4 * pi/180), track_r2 * sin(a4 * pi/180), outline=track_w2)
		shapes += mbpcb.make_line("copper1-top", 0.0, 0.0,
				hole_r2 * cos(a5 * pi/180), hole_r2 * sin(a5 * pi/180), outline=track_w2)
		shapes += mbpcb.make_line("silk-top",
				track_r1 * cos(angle * pi/180), track_r1 * sin(angle * pi/180),
				track_r2 * cos(angle * pi/180), track_r2 * sin(angle * pi/180), outline=0.2)
		shapes += mbpcb.make_line("silk-bot",
				track_r1 * cos(angle * pi/180), track_r1 * sin(angle * pi/180),
				track_r2 * cos(angle * pi/180), track_r2 * sin(angle * pi/180), outline=0.2)
	
	# OSHW logo
	shapes += mbpcb.make_polygon("silk-bot", 1.8 * oshw_x, 1.8 * oshw_y + 5.8)
	
	# text
	shapes2 = mbpcb.make_text("silk-top", "fonts/Salsa.ttf", "Pagoda-%s · %.1fGHz · %s · CC BY-SA" % (version, freq, pol), fontsize2,
			0.0, 0.0, align="center", valign="center", spacing=0.05)
	polygon_arc(shapes2, 0.0, 0.0, 6.1, -90.0)
	mbpcb.pcb_transform(shapes2, 0.0, 0.0, 0.0, 0.0, 0.0, False, True)
	shapes += shapes2
	
	return shapes

@mbpcb.register
def pcb3():
	shapes = []
	shapes += mbpcb.make_circle("board-outline", 0.0, 0.0, pcb_r3)
	
	# coax connection
	shapes += mbpcb.make_circle("drill-plated", 0.0, 0.0, coax_r3 + hole_sp2, pad=True)
	shapes += mbpcb.make_circle("copper1-top", 0.0, 0.0, coax_r3 + solder_w, pad=True)
	shapes += mbpcb.make_circle("copper1-bot", 0.0, 0.0, coax_r3 + solder_w, pad=True)
	shapes += mbpcb.make_circle("mask-top", 0.0, 0.0, coax_r3 + solder_w + mask_sp, pad=True)
	shapes += mbpcb.make_circle("mask-bot", 0.0, 0.0, coax_r3 + solder_w + mask_sp, pad=True)
	
	# disk
	shapes += mbpcb.make_circle("copper1-bot", 0.0, 0.0, disk_r3)
	
	# text
	shapes2 = mbpcb.make_text("silk-top", "fonts/Salsa.ttf", "Pagoda-%s · OSHW · CC BY-SA" % (version), fontsize3,
			0.0, 0.0, align="center", valign="center", spacing=0.05)
	polygon_arc(shapes2, 0.0, 0.0, 4.25, -90.0)
	shapes3 = mbpcb.make_text("silk-top", "fonts/Salsa.ttf", "·", fontsize3,
			0.0, 0.0, align="center", valign="center", spacing=0.05)
	polygon_arc(shapes3, 0.0, 0.0, 4.25, 90.0)
	mbpcb.pcb_transform(shapes2, 0.0, 0.0, 0.0, 0.0, 0.0, False, True)
	mbpcb.pcb_transform(shapes3, 0.0, 0.0, 0.0, 0.0, 0.0, False, True)
	shapes += shapes2 + shapes3
	
	return shapes

@mbpcb.register
def jig1():
	
	r = 0.5
	d = 15.0
	t = 0.1
	
	py1 = d - disk_d1 - pcb_th
	py2 = d - disk_d1
	py3 = d
	py4 = d + pcb_th
	py5 = d + disk_d2 - pcb_th
	py6 = d + disk_d2
	
	x1 = 1.7
	x2 = 4.0
	x3 = 16.0
	x4 = 17.5
	x5 = 9.75
	x6 = 4.65
	
	y1 = 0.0
	y2 = 3.0
	y3 = py1 - 4.0
	y4 = py4 + 4.0
	y5 = py5 - 4.0
	y6 = py6 + 4.0
	y7 = 35.0
	y8 = 38.0
	
	shapes = []
	shapes += mbpcb.make_polygon("board-outline",
		[x2, x3, x3, x4, x4, x3, x3, x2, x2, x1, x1, x6-r, x6  , x6 , x6+0.5, x6+1.4, x6+1.4, x6+0.5, x6 , x6, x6-r, x1, x1, x5-r, x5,
			x5 , x5+0.5, x5+1.4, x5+1.4, x5+0.5, x5 ,
			x5 , x5+0.5, x5+1.4, x5+1.4, x5+0.5, x5 ,
			x5, x5-r, x1, x1, x2],
		[y1, y1, y2, y2, y7, y7, y8, y8, y7, y7, y6, y6  , y6-r, py6, py6-t , py6-t , py5+t , py5+t , py5, y5+r, y5, y5, y4, y4, y4-r,
			py4, py4-t , py4-t , py3+t , py3+t , py3,
			py2, py2-t , py2-t , py1+t , py1+t , py1,
			y3+r, y3, y3, y2, y2])
	
	#shapes += mbpcb.make_rectangle("board-outline", 0.0, (py1 + py2) / 2, pcb_r1 * 2, py2 - py1)
	#shapes += mbpcb.make_rectangle("board-outline", 0.0, (py3 + py4) / 2, pcb_r2 * 2, py4 - py3)
	#shapes += mbpcb.make_rectangle("board-outline", 0.0, (py5 + py6) / 2, pcb_r3 * 2, py6 - py5)
	
	#cy1 = d - disk_d1
	#cy2 = y8 + 4.0
	#shapes += mbpcb.make_rectangle("board-outline", 0.0, (cy1 + cy2) / 2, coax_r3 * 2, cy2 - cy1)
	
	return shapes

@mbpcb.register
def jig2():
	
	x2 = 4.0
	x3 = 16.0
	
	shapes = []
	shapes += mbpcb.make_circle("board-outline", 0.0, 0.0, 20.0)
	for angle in arange(3) * 120:
		shapes2 = mbpcb.make_rectangle("board-outline", (x2 + x3) / 2, 0.0, x3 - x2, 3.0, hole=True)
		mbpcb.pcb_transform(shapes2, 0.0, 0.0, 0.0, 0.0, angle, False, False)
		shapes += shapes2
	shapes += mbpcb.make_circle("board-outline", 0.0, 0.0, 2.5, hole=True)
	
	return shapes

@mbpcb.register
def jig3():
	
	x2 = 4.0
	x3 = 16.0
	
	shapes = []
	for angle in arange(3) * 120:
		shapes2 = mbpcb.make_rectangle("board-outline", (x2 + x3) / 2, 0.0, x3 - x2 + 6.0, 9.0)
		shapes2 += mbpcb.make_rectangle("board-outline", (x2 + x3) / 2, 0.0, x3 - x2, 3.0, hole=True)
		mbpcb.pcb_transform(shapes2, 0.0, 0.0, 0.0, 0.0, angle, False, False)
		shapes += shapes2
	shapes += mbpcb.make_circle("board-outline", 0.0, 0.0, 2.5, hole=True)
	
	return shapes

def par(val1, val2, freq):
	freq1 = 5.8
	freq2 = 5.5
	return val1 + (val2 - val1) * (freq - freq1) / (freq2 - freq1)

for version in ["3", "3B"]:
	for freq in linspace(5.3, 6.0, 8):
		
		if version == "3":
			coax_r1 = 0.46
			coax_r2 = 1.5
			coax_r3 = 1.8
			disk_r1 = par(5.1539, 5.2220, freq)
			disk_r2 = par(7.5056, 7.8335, freq)
			disk_r3 = par(5.6459, 5.8238, freq)
			disk_d1 = par(3.6526, 4.0952, freq) # pcb1 bot -> pcb2 top
			disk_d2 = par(12.4514, 13.1610, freq) # pcb2 top -> pcb3 bot
			pcb_th = 1.0 # fr4 core only, not including copper or solder mask
			track_w1 = 1.0
			track_w2 = 1.0
			track_a1 = par(71.7938, 71.0801, freq)
			track_c1 = par(17.49, 16.7242, freq)
			track_r1 = par(10.2313, 10.8369, freq)
			track_r2 = par(8.6079, 9.0174, freq)
			solder_w = 0.6
			ring_w = 0.25 # via_w in simulation
			hole_sp = 0.05 # for coax core
			hole_sp2 = 0.1 # for coax shield, larger because more variation here
			mask_sp = 0.1
			hole_r1 = par(2.3863, 2.5204, freq)
			hole_r2 = par(5.2364, 5.5135, freq)
			fontsize1 = 3.0
			fontsize2 = 1.8
			fontsize3 = 1.8
		
		if version == "3B":
			coax_r1 = 0.46
			coax_r2 = 1.5
			coax_r3 = 1.8
			disk_r1 = par(5.5849, 5.9331, freq)
			disk_r2 = par(7.6025, 7.6993, freq)
			disk_r3 = par(5.6459, 5.8238, freq)
			disk_d1 = par(3.6526, 4.0952, freq) # pcb1 bot -> pcb2 top
			disk_d2 = par(12.4514, 13.1610, freq) # pcb2 top -> pcb3 bot
			pcb_th = 1.0 # fr4 core only, not including copper or solder mask
			track_w1 = 1.0
			track_w2 = 1.0
			track_a1 = par(69.1855, 66.9806, freq)
			track_c1 = par(19.1231, 16.3271, freq)
			track_r1 = par(10.2313, 10.8369, freq)
			track_r2 = (track_r1 + disk_r2 - track_w1 / 2) / 2
			solder_w = 0.6
			ring_w = 0.25 # via_w in simulation
			hole_sp = 0.05 # for coax core
			hole_sp2 = 0.1 # for coax shield, larger because more variation here
			mask_sp = 0.1
			hole_r1 = par(2.4297, 2.1754, freq)
			hole_r2 = par(4.7274, 5.0440, freq)
			fontsize1 = 2.8
			fontsize2 = 1.74
			fontsize3 = 1.73
		
		pcb_r1 = track_r1 + track_w1 / 2 + 0.5
		pcb_r2 = track_r1 + track_w1 / 2 + 0.5
		pcb_r3 = disk_r3 + 0.5
		track_b1 = -track_c1/2
		
		# plot combined
		if False:
			shapes = []
			shapes += mbpcb.place("pcb1", -12.5,  12.5, 0.0, False, False, pol="LHCP")
			shapes += mbpcb.place("pcb1",  12.5,  12.5, 0.0, False, False, pol="RHCP")
			shapes += mbpcb.place("pcb2", -12.5, -12.5, 0.0, False, False, pol="LHCP")
			shapes += mbpcb.place("pcb2",  12.5, -12.5, 0.0, False, False, pol="RHCP")
			shapes += mbpcb.place("pcb3",  0.0, 0.0, 0.0, False, False)
			
			mbpcb.pcb_plot("Pagoda %s %.1fGHz" % (version, freq), shapes)
			#mbpcb.pcb_plot("Pagoda Top " + version, shapes, layers=[l for l in mbpcb.layerstack if not l.endswith("-bot")])
			#mbpcb.pcb_plot("Pagoda Bot " + version, shapes, layers=[l for l in mbpcb.layerstack if not l.endswith("-top")])
		
		# export gerber
		if True:
			basepath = os.path.dirname(os.path.realpath(__file__)) + "/output/pcb_pagoda_%s_%.1fghz/gerber" % (version, freq)
			if not os.path.exists(basepath):
				os.makedirs(basepath)
			
			shapes = mbpcb.place("pcb1", 0.0, 0.0, 0.0, False, False, pol="LHCP")
			mbpcb.pcb_export(shapes, basepath, "pcb_pagoda_%s_%.1fghz_part1_lhcp" % (version, freq), delete_dir=True)
			
			shapes = mbpcb.place("pcb1", 0.0, 0.0, 0.0, False, False, pol="RHCP")
			mbpcb.pcb_export(shapes, basepath, "pcb_pagoda_%s_%.1fghz_part1_rhcp" % (version, freq), delete_dir=True)
			
			shapes = mbpcb.place("pcb2", 0.0, 0.0, 0.0, False, False, pol="LHCP")
			mbpcb.pcb_export(shapes, basepath, "pcb_pagoda_%s_%.1fghz_part2_lhcp" % (version, freq), delete_dir=True)
			
			shapes = mbpcb.place("pcb2", 0.0, 0.0, 0.0, False, False, pol="RHCP")
			mbpcb.pcb_export(shapes, basepath, "pcb_pagoda_%s_%.1fghz_part2_rhcp" % (version, freq), delete_dir=True)
			
			shapes = mbpcb.place("pcb3", 0.0, 0.0, 0.0, False, False)
			mbpcb.pcb_export(shapes, basepath, "pcb_pagoda_%s_%.1fghz_part3" % (version, freq), delete_dir=True)
		
		# export svg
		if True:
			basepath = os.path.dirname(os.path.realpath(__file__)) + "/output/pcb_pagoda_%s_%.1fghz/svg" % (version, freq)
			if not os.path.exists(basepath):
				os.makedirs(basepath)
			
			for pol in ["LHCP", "RHCP"]:
				shapes = []
				shapes += mbpcb.place("pcb1", -30.0, 0.0, 0.0, False, False, pol=pol)
				shapes += mbpcb.place("pcb2",   0.0, 0.0, 0.0, False, False, pol=pol)
				shapes += mbpcb.place("pcb3",  30.0, 0.0, 0.0, False, False)
				shapes += mbpcb.make_text("silk-top", "fonts/Salsa.ttf", "Pagoda-%s · %.1fGHz · %s · OSHW · CC BY-SA · Designed by Maarten Baert" % (version, freq, pol), 2.5,
						0.0, 20.0, align="center", valign="center", spacing=0.05)
				#mbpcb.pcb_plot("Pagoda %s %.1fGHz %s" % (version, freq, pol), shapes, flat=True)
				mbpcb.pcb_export_svg(shapes, basepath + "/pcb_pagoda_%s_%.1fghz_%s.svg" % (version, freq, pol.lower()), xmin=-50, xmax=50, ymin=-20, ymax=25)
		
		# export dxf
		if True:
			basepath = os.path.dirname(os.path.realpath(__file__)) + "/output/pcb_pagoda_%s_%.1fghz/dxf" % (version, freq)
			if not os.path.exists(basepath):
				os.makedirs(basepath)
			
			shapes = mbpcb.place("pcb1", 0.0, 0.0, 0.0, False, False, pol="LHCP")
			mbpcb.pcb_export_dxf(shapes, basepath + "/pcb_pagoda_%s_%.1fghz_part1_lhcp.dxf" % (version, freq))
			
			shapes = mbpcb.place("pcb1", 0.0, 0.0, 0.0, False, False, pol="RHCP")
			mbpcb.pcb_export_dxf(shapes, basepath + "/pcb_pagoda_%s_%.1fghz_part1_rhcp.dxf" % (version, freq))
			
			shapes = mbpcb.place("pcb2", 0.0, 0.0, 0.0, False, False, pol="LHCP")
			mbpcb.pcb_export_dxf(shapes, basepath + "/pcb_pagoda_%s_%.1fghz_part2_lhcp.dxf" % (version, freq))
			
			shapes = mbpcb.place("pcb2", 0.0, 0.0, 0.0, False, False, pol="RHCP")
			mbpcb.pcb_export_dxf(shapes, basepath + "/pcb_pagoda_%s_%.1fghz_part2_rhcp.dxf" % (version, freq))
			
			shapes = mbpcb.place("pcb3", 0.0, 0.0, 0.0, False, False)
			mbpcb.pcb_export_dxf(shapes, basepath + "/pcb_pagoda_%s_%.1fghz_part3.dxf" % (version, freq))
		
		# (jig) export svg and dxf
		if True and version == "3":
			basepath1 = os.path.dirname(os.path.realpath(__file__)) + "/output/jig_pagoda_%s_%.1fghz/svg" % (version, freq)
			if not os.path.exists(basepath1):
				os.makedirs(basepath1)
			basepath2 = os.path.dirname(os.path.realpath(__file__)) + "/output/jig_pagoda_%s_%.1fghz/dxf" % (version, freq)
			if not os.path.exists(basepath2):
				os.makedirs(basepath2)
			
			shapes = []
			shapes += mbpcb.place("jig1",  0.0, 1.0, 0.0, False, False)
			shapes += mbpcb.place("jig1", 20.0, 1.0, 0.0, False, False)
			shapes += mbpcb.place("jig1", 40.0, 1.0, 0.0, False, False)
			shapes += mbpcb.place("jig2", 82.0, 20.0, 0.0, False, False)
			shapes += mbpcb.place("jig3", 115.0, 20.0, 0.0, False, False)
			
			#mbpcb.pcb_plot("JIG Pagoda %s %.1fGHz" % (version, freq), shapes)
			mbpcb.pcb_export_svg(shapes, basepath1 + "/jig_pagoda_%s_%.1fghz.svg" % (version, freq))
			mbpcb.pcb_export_dxf(shapes, basepath2 + "/jig_pagoda_%s_%.1fghz.dxf" % (version, freq))
		
		# create zip file
		if True:
			basepath = os.path.dirname(os.path.realpath(__file__)) + "/output/pcb_pagoda_%s_%.1fghz" % (version, freq)
			if os.path.isfile(basepath + ".zip"):
				os.remove(basepath + ".zip")
			subprocess.call(["zip", "-r", os.path.basename(basepath) + ".zip", os.path.basename(basepath)], cwd=os.path.dirname(basepath))
		
		# (jig) create zip file
		if True and version == "3":
			basepath = os.path.dirname(os.path.realpath(__file__)) + "/output/jig_pagoda_%s_%.1fghz" % (version, freq)
			if os.path.isfile(basepath + ".zip"):
				os.remove(basepath + ".zip")
			subprocess.call(["zip", "-r", os.path.basename(basepath) + ".zip", os.path.basename(basepath)], cwd=os.path.dirname(basepath))
