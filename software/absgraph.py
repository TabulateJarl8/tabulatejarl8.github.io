import re
from plugins.core import *
style = darkStyle
def absGraph(x, y, slope, upsidedown=False):
	equ = "y="
	if upsidedown == True:
		equ = equ + "-"
	equ = equ + str(slope) + "|x-" + str(x) + "|+" + str(y)
	equ = re.sub("\--", "+", equ)
	equ = re.sub("\+-|\-+", "-", equ)
	equ = re.sub("\-0", "", equ)
	equ = re.sub("\+0", "", equ)
	if equ[2] == "1":
		equ = equ.replace("1", "", 1)
	print(equ)
def help():
	print(style.output + "ABSGraph Help")
	print("")
	print(style.output + "Syntax")
	print(style.output + "absGraph(Vertex X, Vertex Y, Slope, Is Graph Upside Down [True/(False)])")