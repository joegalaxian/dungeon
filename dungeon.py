# My modules.i
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
KEY_LEFT	= (97, 65)
KEY_DOWN	= (115, 83)
KEY_RIGHT	= (100, 68)
KEY_ENTER	= (13)
KEY_YES		= (121, 89)
KEY_NO		= (110, 78)
KEY_SPACE	= (32, None) #Hack: None added for using "in KEY_SPACE"
KEY_TAB		= (9, None)
KEY_HELP	= (104,72)
KEY_LEVEL	= (108,76)


# Class Game
class Game(object):
	def __init__(self):
		self.completed = False
		self.level = Level()
		return

	def run(self):
		while not self.completed:
			self.level.run()

# Class Level
class Level(object):
	def __init__(self, id = 1):
		self.completed = False
		self.id = id
		self.map = self.load_map()
		
		print 'DEBUG g.render_map_dict(self.map)'
		g.render_map_dict(self.map)

	def load_map(self):
		return load_map_as_dict(load_map(self.id))

	def run(self):
		self.loop()
		self.render()

	def loop(self):
		while not self.completed:
			for x,y in self.map:
				bck, obj = map[x,y]
				if obj:
					obj.run()

	def render(self):
		(x,y) = self.map_size(map)
		for xi in range(x+1):
			for yi in range(y+1):
				print self.map[xi, yi]
			print ''

	def map_size(self):
		(x,y) = (0,0)
		for (xi, yi) in self.map:
			if x < xi:
				x = xi
			if y < yi:
				y = yi
		return (x,y)













"""
class Level(object):
	def __init__(self, floor=1):
		self.floor = floor
		m = load_map(floor)
		self.map_dict = load_map_as_dict(m)
		self.player = get_key(self.map_dict, 'P')
		self.switch = get_key(self.map_dict, 's')
		self.completed = False
		self.switch_pressed = False

	def player(self):
		return get_key(self.map_dict, 'P')

	def map_size(self):
		return '(TO,DO)'

	def action_key(self, key):
		action_key(key, self.map_dict)
"""

# Returns int value of key pressed.
def read_key():
	# Config the keyboard as raw to read key press.
	attr = termios.tcgetattr(sys.stdin)
	tty.setraw(sys.stdin)
	c = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, attr)
	return ord(c[0])

def new_position((x,y), k):
	if k in KEY_UP:
		return (x-1,y)
	elif k in KEY_DOWN:
		return (x+1,y)
	elif k in KEY_LEFT:
		return (x,y-1)
	elif k in KEY_RIGHT:
		return (x,y+1)

# Action key (i.e. move player, help menu, quit game, etc).
def action_key(k, m):
	switch = get_key(m, 's')
	px, py = get_key(m, 'P')

	# If ESC, Q, q pressed then terminate:
	if k in KEY_ESC:
		terminate()

	# If hit the wall then ring.
	if k in (KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT):	
		nx, ny = new_position((px,py), k)

		if m[nx,ny] == 'X':
			print '\a'
		elif m[nx,ny] == '_':
			print "Passed!"
		else:
			None

	# If KEY_UP:
	if k in KEY_UP:
		if m[px-1, py] == '.':
			m[px-1, py] = 'P'
			m[px, py] = '.'
	
	# KEY_LEFT:
	if k in KEY_LEFT:
		# If empty space then move there.
		if m[px, py-1] == '.':
			m[px, py-1] = 'P'
			m[px, py] = '.'

	# KEY_DOWN:
	if k in KEY_DOWN:
		# If empty space then move there.
		if m[px+1,py] == '.':
			m[px+1,py] = 'P'
			m[px,py] = '.'	

	# KEY_RIGHT:
	if k in KEY_RIGHT:
		# If empty space then move there.
		if m[px,py+1] == '.':
			m[px,py+1] = 'P'
			m[px,py] = '.'

	# KEY_SPACE:
	if k in KEY_SPACE:
		return	# Wait a turn.

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

	else:
		None

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

# Returns position (x,y) of the player on the dictionary map.
def get_key(dic, value):
	for (k, v) in dic.iteritems():
		if v == value:
			return k

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

"""
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
"""

# Main function.
def main():
	key = None
	time = 0
	floor = 0

	# Game main loop
	while True:

		# Load new level:
		floor += 1
		level = Level(floor)

		# Loop on level.
		while not level.completed:

			# Render game:
			g.clear()
			print "Dungeon.py v01"
			print "time......:", time
			print "floor.....:", level.floor
			print "player....:", get_key(level.map_dict, 'P')
			print "key.......:", key
			#print "map_size..:", level.map_size()
			g.render_map_dict(level.map_dict)
			
			# Read and action key:
			key = read_key()
			#action_key(key, level.map_dict)
			level.action_key(key)
			time += 1
			
			if key in KEY_LEVEL: level.completed = True

if __name__ == '__main__':	
	game = Game()
	game.run()
	main()
