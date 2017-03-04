import clientpy2 as cp
from collections import defaultdict
import math

class Game:
	def __init__(self):
		self.config = self.initGame()

	def run(self, command):
		return cp.run("jmv", "mrgoose", command)

	def initGame(self):
		conf = self.config().split(" ")
		state = defaultdict(str)
		i = 1
		while i < len(conf) - 1:
			state[conf[i]] = conf[i+1].strip("\r\n")
			i += 2
		return state

	def config(self):
		return self.run("CONFIGURATIONS")

	def status(self):
		return self.run("STATUS")


class Player():
	def __init__(self, acc=0, position=0, velocity=0, gmines=0, enemies=0, bombs=0, mineIndex=0):
		self.game = Game()
		self.acc = acc
		self.position = position
		self.velocity = velocity
		self.gmines = gmines
		self.enemies = enemies
		self.bombs = bombs
		self.mineIndex = mineIndex

	def accelerate(self, radians=0, accel=1):
		return self.run("ACCELERATE %f %f"%(radians,accel))

	def run(self, command):
		return cp.run("jmv", "mrgoose", command)

	def status(self):
		st = self.run("STATUS")
		return st


	def parseStatus(self):
		status = self.status().split(" ")[1:-1]
		i = 0
		mines = []
		while (status[i] != 'MINES'):
			i += 1
		i += 1
		while (status[i] != 'PLAYERS'):
			mines.append(status[i])
			i += 1
		i += 1
		if(len(mines)==1):
			mines=[]
		else:
			mines=mines[1:]
			t=[]
			for i in range(len(mines)/3):
				t.append((mines[3*i + 1],mines[3*i + 2]))
			mines=t[:]
		players = []
		while (status[i] != 'BOMBS'):
			players.append(status[i])
			i += 1
		i += 1
		bombs = []
		while (i < len(status)):
			bombs.append(status[i])
			i += 1
		statusDict = {'MINES': mines, 'PLAYERS': players, 'BOMBS': bombs, 'x': status[0], 'y': status[1],
						'dx': status[2], 'dy': status[3]}
		return statusDict

	def score(self):
		return self.run("SCOREBOARD")


import time

def run(command):
	return cp.run("jmv", "mrgoose", command)

def status():
    return run("STATUS")


def brake():
    return run("BRAKE")

def bomb(x, y, t=None):
	if t is not None:
		return run("BOMB %f %f %f", (x, y, t))
	else:
		return run("BOMB %f %f", (x, y))

def scan(x, y):
	return run("SCAN %f %f", (x, y))


if __name__ == '__main__':
	p = Player()
	radians=math.atan(2*150.0/10000.0)
	mineSet=set()
	while True:
		p.accelerate(radians, 1)
		#print(p.parseStatus())
		d=p.parseStatus()
		mines=d.get("MINES")
		for i in mines:
			mineSet.add(i)
		print(d)
		print(mineSet)

		# print(p.score())
		#print(p.game.config)

# I don't want to mess with your code, but I think that you should run each of the commands, and see what happens, to some extent, this does look like an AI contest
# But there's a bunch of things that you would wnat to do first.
