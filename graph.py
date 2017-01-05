# Graphic-related code for the Dungeon game.

import os

def clear():
	os.system("clear")

# print(chr(27) + "[2J") #clears screen up to this line

def print_map(m):
	for line in m:
		for c in line:
			print c,
