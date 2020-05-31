from plugins.core import *
style = darkStyle

def countOdds(startnum, endnum, showNums=False):
	even = []
	odd = []
	i = startnum
	while i <= endnum:
		if (i % 2) == 0:
			even.append(i)
		else:
			odd.append(i)
		i += 1
	print(style.output + "There are " + style.important + str(len(odd)) + style.output + " odds and " + style.important + str(len(even)) + style.output + " evens")
	if showNums == True:
		print("Odds: ")
		print(odd)
		print("Evens:")
		print(even)
def help():
	print(style.output + "Odds Help")
	print("")
	print("Syntax")
	print("countOdds(Start Number, End Number, Show Lists of Numbers [True/(False)])")