# My modules.
import graph as g

# Import for the key press.
import sys
import termios
import tty


# Key values constants.
KEY_ESC		= (27, 113, 81)
KEY_UP		= (ord('W'), ord('w'))
KEY_LEFT	= (ord('A'), ord('a'))
KEY_DOWN	= (ord('S'), ord('s'))
KEY_RIGHT	= (ord('D'), ord('d'))
KEY_ENTER	= (13)
KEY_YES		= (ord('Y'), ord('y'))
KEY_NO		= (ord('N'), ord('n'))
KEY_SPACE	= (32, None) #Hack: None added for using "in KEY_SPACE"
KEY_TAB		= (9)
KEY_HELP	= (ord('H'), ord('h'))
KEY_LEVEL	= (ord('L'), ord('l'))


# Class Game
class Game(object):

	def __init__(self):
		self.is_completed = False
		self.level = Level()
		return


	def run(self):
		while not self.is_completed:
			while not self.level.is_completed:
				self.level.run()
			self.next_level()


	def next_level(self):
		self.level = Level(self.level.floor_no + 1)


# Class Level
class Level(object):

	def __init__(self, n = 1):
		self.is_completed = False
		self.floor_no = n
		self.map_matrix = self.load_map_matrix()


	def load_map_matrix(self):
		return self.load_map_as_dict(self.load_map_file())


	# Loads map as list of strings from file.
	def load_map_file(self):
		try:
			map_file_path = 'maps/' + str(self.floor_no) + '.map'
			map_file = open(map_file_path, 'r')
			m = map_file.readlines()
			map_file.close()
			return m
		except IOError:
			terminate("Game over, you've hit the end of the dungeon!")


	# Loads map as dictionary from list of strings. Dictionary structure: m{(x,y): 'c'}
	def load_map_as_dict(self, lst_lines):
		m_dict = {}

		x = len(lst_lines)
		y = len(lst_lines[0])-1
		
		# print '>DEGUG x,y (lst_lines):', (x,y)
		for xi in range(x):
			for yi in range(y):
				"""
				# TODO:
				x = lst_lines[xi][yi]
				if x in OBJECTS:
					new_obj = Object((xi, yi), x)
					self.objects.append(new_obj);
					matrix_map[xi,yi] = '.' #EMPTY_SPACE
				else:
					matrix_map[xi,yi] = x #char read from file
				"""
				m_dict[xi,yi] = lst_lines[xi][yi]

		return m_dict


	def run(self):
		while not self.is_completed:
			self.render()
			self.tick()
			#self.render()
		

	def render(self):
		# Clears screen, prints status, and prints the map.
		g.clear()
		self.print_status()

		(x,y) = self.map_size()
		for xi in range(x):
			for yi in range(y):
				print self.map_matrix[xi, yi],
			print '\r'


	def print_status(self):
		print 'Dungeon.py v01 \r'
		#print "time......:", time
		print "floor.....:", self.floor_no, '\r'
		print "player....:", self.get_map_position('P'), '\r'
		#print "key.......:", key
		print "map_size..:", self.map_size(), '\r'


	def map_size(self):
		(x,y) = (0,0)
		for (xi, yi) in self.map_matrix:
			if x < xi:
				x = xi
			if y < yi:
				y = yi
		return (x+1,y+1)


	def tick(self):
		# Read and action key:
		key = self.read_key()
		self.action_key(key)

		"""
		# TODO:
		from obj in self.objects:
			obj.run()
		"""


	# Returns int value of key pressed.
	def read_key(self):
		# Config the keyboard as raw to read key press.
		attr = termios.tcgetattr(sys.stdin)
		tty.setraw(sys.stdin)
		k = sys.stdin.read(1)
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, attr)
		return ord(k[0])


	# Action key (i.e. move player, help menu, quit game, etc).
	def action_key(self, k):

		# New (desired) position
		nx, ny = self.new_position(k)

		# Common object positions.
		px, py = self.get_map_position('P')	# Player
		switch = self.get_map_position('s')	# Switch
		exit = self.get_map_position('_')	# Exit
		
		# If ESC, Q, q pressed then terminate:
		if k in KEY_ESC:
			terminate()

		# KEY_SPACE:
		elif k in KEY_SPACE:
			return	# Wait a turn.
	
		# KEY_YES:
		elif k in KEY_YES:
			pass

		# KEY_NO:
		elif k in KEY_NO:
			pass
	
		# KEY_TAB:
		elif k == KEY_TAB:
			terminate('TAB')
			pass

		# KEY_HELP:
		elif k in KEY_HELP:
			print "Help:\r"
			print "[W,A,S,D]...Move player.\r"
			print "[ESC,Q].....Terminate game.\r"
			print "[SPACE].....Wait a turn.\r"
			#print "Press any key to resume game."
			#read_key()

		# KEY_LEVEL	
		elif k in KEY_LEVEL:
			self.next_level()

		# KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
		elif k in KEY_UP or k in  KEY_DOWN or k in KEY_LEFT or k in KEY_RIGHT:
			# If moves towards the exit then enter new level.
			#if (nx, ny) == exit:
			if self.map_matrix[(nx, ny)] == '_':
				self.next_level()
		
			# If moves towards the wall then ring.
			elif self.map_matrix[nx,ny] == 'X':
				print '\a'
	
			# If moves towards hit an empty space
			elif self.map_matrix[(nx, ny)] == '.':
				self.map_matrix[nx, ny] = 'P'
				self.map_matrix[px, py] = '.'

		else:
			self.run()


	# Returns position (x,y) of the valuer on the map matrix.
	def get_map_position(self, value):
		for (k, v) in self.map_matrix.iteritems():
			if v == value:
				return k


	# Return the new (desired) player position after the key pressed.
	def new_position(self, k):
		x, y = self.get_map_position('P')
		if k in KEY_UP:
			return x-1, y
		elif k in KEY_DOWN:
			return x+1, y
		elif k in KEY_LEFT:
			return x, y-1
		elif k in KEY_RIGHT:
			return x, y+1
		else:
			return x, y


	# Mark level as completed.	
	def next_level(self):
		self.is_completed = True




# Terminates game printing a message, 'Game terminated.' by default.
def terminate(str = "Game terminated."):
	print str
	quit()




if __name__ == '__main__':
	game = Game()
	game.run()

