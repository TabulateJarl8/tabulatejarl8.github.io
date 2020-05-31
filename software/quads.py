from plugins.core import *
import re
from math import *
style = darkStyle

#Quadratic Word Problems
def quadWord():
	a = input(style.input + "A Value: ")
	b = input("B Value: ")
	c = input("C Value: ")
	a = int(a)
	b = int(b)
	c = int(c)
	upsideDown = False
	if a < 0:
		upsideDown = True
	yInt = "(0, " + str(c) + ")"
	negB = "-" + str(b)
	if negB[0] == "-":
		if negB[1] == "-":
			negB = re.sub("--", "", negB)
	negB = int(negB)
	doublea = a * 2
	aOs = float((negB)/doublea)
	first = (a * (aOs ** 2))
	second = int(b * aOs)
	equ = str(first) + "+" + str(second) + "+" + str(c)
	equ = re.sub("\+-|\-+", "-", equ)
	equ = eval(equ)
	vertex = "(" + str(aOs) + ", " + str(equ) + ")"
	print("")
	print(style.output + "Vertex: " + str(vertex))
	print("AOS: " + str(aOs))
	print("Y-Int: " + str(yInt))
	if upsideDown == True:
		print("Parabola is Upside Down")
	print("")
	
	#Show Work
	print(style.important + "Work:")
	equStr = str(a) + "*" + str(aOs) + "^2+" + str(b) + "*" + str(aOs) + "+" + str(c)
	equStr = re.sub("\+-|\-+", "-", equStr)
	print(style.output + equStr)
	equBefore = str(first) + "+" + str(second) + "+" + str(c)
	equBefore = re.sub("\+-|\-+", "-", equBefore)
	print(equBefore)
	print(equ)
	print("")
	print(str(negB) + "/2(" + str(a) + ")")
	print(aOs)	
	
def help():
	print(style.output + "quadWord() - Find Parabolla from Quadratic Equation")