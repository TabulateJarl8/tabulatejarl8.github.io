from plugins.core import *
import math
import statistics
import time
import os
import urllib.request
from tqdm import tqdm
from update_check import *
style=darkStyle

try:
	import plugins.flib
except:
	try:
		os.chdir("plugins")
		url = 'https://raw.githubusercontent.com/TabulateJarl8/calcplugins/master/formulas/flib.py'
		for i in tqdm(range(1), desc="Downloading flib..."):
			path = __file__
			path = path.replace("formulas.py", "flib.py")
			urllib.request.urlretrieve(url, path)
		os.chdir("..")
		import plugins.flib
	except:
		print(style.error + "Couldnt connect to update service. Please connect to the internet and try again to update" + style.normal)
	
#Updater
print("Checking for Updates...")
for i in tqdm(range(1)):
	x = isUpToDate(__file__, "https://raw.githubusercontent.com/TabulateJarl8/calcplugins/master/formulas/formulas.py")
if x == False:
	x = input(style.important + "Update? [Y/n] " + style.normal)
	if x.lower() != 'n':
		print(style.output + "Updating formulas...")
		os.chdir("plugins")
		update(__file__, "https://raw.githubusercontent.com/TabulateJarl8/calcplugins/master/formulas/formulas.py")
		os.chdir("..")
		print("")
		print(style.important + "Formulas Updated. Please Restart the Calculator." + style.normal)
		time.sleep(2)
	
def install():
	dir = os.listdir('plugins/')
	if 'flib.py' in dir:
		print(style.error + "flib is already installed.")
	else:
		os.chdir("plugins")
		url = 'https://raw.githubusercontent.com/TabulateJarl8/calcplugins/master/formulas/flib.py'
		for i in tqdm(range(1), desc="Downloading flib..."):
			path = __file__
			path = path.replace("formulas.py", "flib.py")
			urllib.request.urlretrieve(url, path)
		os.chdir("..")
		import plugins.flib

def areaSquare(l):
	area = l**2
	print(style.answer + str(area))

def areaRectangle(l, w):
	area = w * l
	print(style.answer + str(area))

def areaTriangle(b, h):
	area = b * h
	area = area // 2
	print(style.answer + str(area))

def areaRhombus(D, d):
	area = D * d
	area = area // 2
	print(style.answer + str(area))

def areaTrapezoid(B, b, h):
	area = B * b
	area = area // 2
	area = area * h
	print(style.answer + str(area))

def areaRegularPolygon(P, a):
	area = P // 2
	area = area * a
	print(style.answer + str(area))

def areaCircle(r):
	area = r ** 2
	area = area * math.pi
	print(style.answer + str(area))
	
def areaRegularPentagon(s):
	s = s ** 2
	print(style.answer + str(1.720 * s))
	
def areaRegularHexagon(s):
	s = s ** 2
	print(style.answer + str(2.598 * s))

def areaRegularOctogon(s):
	s = s ** 2
	print(style.answer + str(4.828 * s))

def surfaceAreaCone(r, s):
	area = math.pi * r
	area = area * s
	print(style.answer + str(area))

def surfaceAreaSphere(r):
	area = r ** 2
	area = area * 4
	area = area * math.pi
	print(style.answer + str(area))
	
def surfaceAreaCube(s):
	area = s ** 2
	area *= 6
	print(style.answer + str(area))
	
def surfaceAreaRectangularPrism(a, b, c):
	first = 2 * a * b
	second = 2 * b * c
	third = 2 * a * c
	area = first + second + third
	print(style.answer + str(area))

def volumeCube(s):
	vol = s ** 3
	print(style.answer + str(vol))

def volumeParallelepiped(l, w, h):
	vol = l * w * h
	print(style.answer + str(vol))

def volumeRectangularPrism(b, h):
	vol = b * h
	print(style.answer + str(vol))

def volumeCylinder(r, h):
	vol = r ** 2
	vol = vol * math.pi
	vol = vol * h
	print(style.answer + str(vol))

def volumeCone(b, h):
	third = 1 / 3
	vol = third * b
	vol = vol * h
	print(style.answer + str(vol))

def volumeSphere(r):
	vol = r ** 3
	vol = vol * math.pi
	fraction = 4 / 3
	vol = vol*fraction
	print(style.answer + str(vol))

def perimeterSquare(s):
	per = 4 * s
	print(style.answer + str(per))

def perimeterRectangle(l, w):
	len = 2 * l
	wid = 2 * w
	per = len + wid
	print(style.answer + str(per))

def perimeterCircle(r=0, d=0):
	if r == 0:
		per = math.pi * d
	else:
		per = 2 * math.pi * r
	print(style.answer + str(per))
	
def mean(nums):
	mean = 0
	for i in range (len(nums)):
		mean = mean + nums[i]
	mean = mean // len(nums)
	print(style.answer + str(mean))
	
def median(nums):
	nums.sort()
	if len(nums) % 2 == 0:
		while len(nums) > 2:
			nums = nums[1:]
			nums = nums[:-1]
		median = nums[0] + nums[1]
		median = median // 2
		print(style.answer + str(median))
	else:
		while len(nums) > 1:
			nums = nums[1:]
			nums = nums[:-1]
		print(style.answer + str(nums[0]))

def mode(nums):
	print(style.answer + str(statistics.mode(nums)))
	
def range(nums):
	nums.sort()
	print(style.answer + str(nums[-1] - nums[0]))

def midpoint(x1, y1, x2, y2):
	x = x1 + x2
	x = x // 2
	y = y1 + y2
	y = y // 2
	print(style.answer + "(" + str(x) + ", " + str(y) + ")")
	
def distance(x1, y1, x2, y2):
	x = x2 - x1
	x = x ** 2
	y = y2 - y1
	y = y ** 2
	distance = x + y
	distance = math.sqrt(distance)
	print(distance)
	
def slope(x1, y1, x2, y2):
	y = y2 - y1
	x = x2 - x1
	slope = y / x
	slope = str(slope)
	if slope[-1] == "0" and slope[-2] == ".":
		i = 1
		while i < 3:
			slope = slope[:-1]
			i += 1
		print(slope)
	else:
		print(y)
		print(u"\u2014\u2014\u2014")
		print(x)

def distance(s, t):
	dis = s * t
	print("Traveled " + str(dis) + " u")

def speed(d, t):
	print(str(d//t) + " u/t")
	
def time(d, s):
	print(str(d//s) + " u")
	
def work(f, d):
	print(str(f * d) + " n-distanceUnit")
	
def force(m, a):
	print(str(m * a) + " newtons")
	
def mass(d, v):
	print(str(d * v) + " grams")
	
def density(m, v):
	print(str(m//v))
	
def quadForm(a, b, c):
	if 'flib.py' in os.listdir("plugins/"):
		plugins.flib.quadForm(a, b, c)
	else:
		print(style.error + "This feature is disabled. Please type formulas.install() to enable this feature.")
	

def help():
	if not 'flib.py' in os.listdir("plugins"):
		print(style.important + "Please type formulas.install() to install needed libraries")
		print("")
	print(style.output + "Type formulas.calcs() to get a list of supported calculations and syntaxes or formulas.abbrList() to get a list of abbreviations. You can also inpuy values out of order by directly specifying their values. Eg: quadForm(b=3, a=9, c=10)")

def abbrList():
	print(style.output + "l - Length")
	print("w - Width")
	print("h - Height")
	print("b - Base/Small Side")
	print("D - Large Diagonal")
	print("d - Small Diagonal/Diameter/Distance/Density")
	print("B - Large Side")
	print("P - Perimeter")
	print("a - apothem/Acceleration")
	print("r - Radius/Rate")
	print("s - Slant Height/Side")
	print("t - Time")
	print("u - units")
	print("f - Force")
	print("m - Mass")
	print("v - Volume")

def calcs():
	print(style.important + "Area")
	print(style.output + "areaSquare(<length>)")
	print("areaRectangle(<length>, <width>)")
	print("areaTriangle(<base>, <height>)")
	print("areaRhombus(<Large Diagonal>, <Small Diagonal>)")
	print("areaTrapezoid(<Large Side>, <Small Side>, <Height>)")
	print("areaRegularPolygon(<perimeter>, <apothem>)")
	print("areaRegularPentagon(<side>)")
	print("areaRegularHexagon(<side>)")
	print("areaRegularOctogon(<side>)")
	print("areaCircle(<radius>)")
	print("")
	print(style.important + "Surface Area")
	print(style.output + "surfaceAreaCone(<radius>, <Slant Height>)")
	print("surfaceAreaSphere(<radius>)")
	print("surfaceAreaCube(<side>)")
	print("surfaceAreaRectangularPrism(<side 1>, <side 2>, <side 3>)")
	print("")
	print(style.important + "Volume")
	print(style.output + "volumeCube(<side>)")
	print("volumeParallelepiped(<length>, <width>, <height>)")
	print("volumeRectangularPrism(<base>, <height>)")
	print("volumeCylinder(<radius>, <height>)")
	print("volumeCone(<base>, <height>)")
	print("volumeSphere(<radius>)")
	print("")
	print(style.important + "Perimeter")
	print(style.output + "perimeterSquare(<side>)")
	print("perimeterRectangle(<length>, <width>)")
	print("perimeterCircle(<radius>)")
	print("perimeterCircle(<diamter>)")
	print("")
	print(style.important + "Data")
	print(style.output + "mean([n1, n2, n3...])")
	print("median([n1, n2, n3...])")
	print("mode([n1, n2, n3...])")
	print("range([n1, n2, n3...])")
	print("")
	print(style.important + "Graphing between 2 points")
	print(style.output + "midpoint(x1, y1, x2, y2)")
	print("distance(x1, y1, x2, y2)")
	print("slope(x1, y1, x2, y2) ")
	print("")
	print(style.important + "Travel/Work")
	print(style.output + "distance(<speed>, <time>")
	print("speed(<distance, <time>)")
	print("time(<distance>, <speed>)")
	print("work(<force>, <distance>)")
	print("force(<mass>, <acceleration>)")
	print("mass(<density>, <volume>)")
	print("density(<mass>, <volume>)")
	print("")
	print(style.important + "Numerical Formulas")
	print(style.output + "quadForm(<a>, <b>, <c>)")
	