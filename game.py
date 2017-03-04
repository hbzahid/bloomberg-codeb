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

	def brake(self):
		return self.run("BRAKE")

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
				t.append((float(mines[3*i + 1]),float(mines[3*i + 2])))
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
		self.position=(float(status[0]),float(status[1]))
		self.velocity=(float(status[2]),float(status[3]))
		statusDict = {'MINES': mines, 'PLAYERS': players, 'BOMBS': bombs, 'x': status[0], 'y': status[1],
						'dx': status[2], 'dy': status[3]}
		return statusDict

	def score(self):
		return self.run("SCOREBOARD")

	def goTo(self, final):
	    # finding direction
	    i = 0
	    while (i < 50): 
	    	self.brake()
	    	i += 1
	    direction = [final[0] - self.position[0],final[1] - self.position[1]]
	    normalized = math.sqrt(math.pow(direction[0], 2) + math.pow(direction[1], 2))
	    direction[0] = direction[0]/normalized
	    direction[1] = direction[1]/normalized

	    #normalizing current velocity
	    normalized = math.sqrt(math.pow(self.velocity[0], 2) + math.pow(self.velocity[1], 2))
	    velocity_normalized = [self.velocity[0], self.velocity[1]]
	    velocity_normalized[0] = velocity_normalized[0]/normalized
	    velocity_normalized[1] = velocity_normalized[1]/normalized

	    #finding acceleration to reach point <x1, y1> from <x,y>
	    # V + A = nd ; we need to find A
	    n = 3
	    acceleration = [n * direction[0] - velocity_normalized[0], n * direction[1] - velocity_normalized[1]]
	    normalized = math.sqrt( math.pow(acceleration[0], 2) + math.pow(acceleration[1], 2))
	    acc_rads = math.atan2(acceleration[0]/normalized, acceleration[1]/normalized)
	    acc_rads = acc_rads + (math.pi * 2) if acc_rads < 0 else acc_rads
	    print(acc_rads)
	    #acceleration[0] = math.atan2(acceleration[0]/normalized)
	    #acceleration[1] = math.atan2(acceleration[1]/normalized)
	    var1 = math.sqrt(math.pow(self.position[0] - final[0], 2) + math.pow(self.position[1] - final[1], 2))
	    while var1 >= 2:
	    	print "looping"
	    	self.accelerate(acc_rads, 1)
		#self.accelerate(radians, 1)
		#var = math.sqrt(((self.position[0] - final[0])**2) +((self.position[1] - final[1])**2))

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
			p.goTo(i)

		print(d)
		print(mineSet)

		# print(p.score())
		#print(p.game.config)

# I don't want to mess with your code, but I think that you should run each of the commands, and see what happens, to some extent, this does look like an AI contest
# But there's a bunch of things that you would wnat to do first.
