# My modules.
import graph as g

# Import for chararray.
# import numpy as np

# Import for the key press.
import sys
import termios
import tty

# Key values constants.
KEY_ESC		= (27, 113, 81)
KEY_UP		= (119, 87)
KEY_LEFT	= (115, 83)
KEY_DOWN	= (100, 68)
KEY_RIGHT	= (100, 68)
KEY_ENTER	= (13)
KEY_YES		= (121, 89)
KEY_NO		= (110, 78)
KEY_SPACE	= (32)
KEY_TAB		= (9)
KEY_HELP	= (104,72)

# Returns int value of key pressed.
def read_key():
	# Config the keyboard as raw to read key press.
	attr = termios.tcgetattr(sys.stdin)
	tty.setraw(sys.stdin)
	c = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, attr)
	return ord(c[0])

# Action key (i.e. move player, help menu, quit game, etc).
def action_key(k, m, p):
	# If ESC, Q, q pressed then terminate:
	if k in KEY_ESC:
		terminate()

	# If KEY_UP:
	if k in KEY_UP:
		px, py = p
		if m[px-1][py] == '.':
			new_x = px-1
			new_y = py
			p = (new_x, new_y)
			#print p
			#terminate()
			#m[px][py] = '.'
			#m[new_x][new_y] = 'P'

	# KEY_LEFT:
	# KEY_DOWN:

	# KEY_RIGHT:

	# KEY_SPACE:
		# Wait a turn.

	# KEY_YES:

	# KEY_NO:

	# KEY_TAB:

	# KEY_HELP:
	if k in KEY_HELP:
		print "Help:"
		print "Move player with W, A, S, D."
		print "Terminate the game with ESC, Q, q."
		print "Wait a turn with SPACE."
		#print "Press any key to resume game."
		#read_key()

# Terminates game printing a message, 'Game terminated.' by default.
def terminate(str = "Game terminated."):
	print str
	quit()

# Returns position (x,y) of the player on the map.
def locate_player(m):
	for x in range(len(m)):
		for y in range(len(m[0])):
			if m[x][y] == 'P':
				return (x,y)

"""
# UNUSED
def chararray_map(m):
	mx = len(m[0])-1-1
	my = len(m)-1
	print m
	print (mx,my)
	cm = np.chararray(mx, my)
	cm[:] = 'X'
	print cm
	for x in range(mx):
		for y in range(my):
			print (mx,my)
			cm[x][y] = m[mx][my]
			read_key()
	return cm
"""

# Loads map as list of strings from file.
def load_map(level):
	map_file_path = 'maps/' + str(level) + '.map'
	map_file = open(map_file_path, 'r')
	m = map_file.readlines()
	map_file.close()
	return m

# Loads map as dictionary from list of strings. Dictionary structure: m{(x,y): 'c'}
def load_map_as_dict(m):
	m_dict = {}
	mx = len(m)
	my = len(m[0])
	#print 'DEBUG mx,my: ', mx, my
	for x in range(len(m)):
		for y in range(len(m[0])-1):
			m_dict[(x,y)] = m[x][y]
	#print 'DEBUG %r' % m_dict
	return m_dict

# Todo: move this to grahp.py
def render_map_dict(m_dict):
	(x,y) = (0,0)
	#x = 0
	#y = 0
	for (xi,yi) in m_dict:	
		if x < xi:
			x = xi
		if y < yi:
			y = yi
	for xi in range(x+1):
		for yi in range(y+1):
			print m_dict[(xi,yi)],
		print ''

# Main function.
def main():
	key = None
	level = 0
	time = 0

	# Game main loop
	while True:

		# Load new level:
		level += 1
		level_completed = False
		
		# Read map from file.
		map = load_map(level)
		map_dict = load_map_as_dict(map)

		# Map dimensions.
		map_x = len(map[0])-1-1
		map_y = len(map)-1

		# Locate player on map.
		player = locate_player(map)

		# Loop on level.
		while not level_completed:

			# Render game:
			g.clear()
			print "Dungeon.py v01"
			print "level.....:", level
			print "map_size..:", (map_x, map_y)
			print "key.......:", key
			print "player....:", player
			print "time......:", time
			#g.print_map(map)
			render_map_dict(map_dict)
			
			# Read and action key:
			action_key(key, map, player)
			key = read_key()
			time += 1

if __name__ == '__main__':	
	main()
