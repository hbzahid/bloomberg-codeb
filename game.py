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
		t2={}
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
				#t2.append(mines[3*i])
				t2[mines[3*i]]=(float(mines[3*i + 1]),float(mines[3*i + 2]))
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
		statusDict = {'MINES': mines, 'MINEPLAYER':t2 , 'PLAYERS': players, 'BOMBS': bombs, 'x': status[0], 'y': status[1],
						'dx': status[2], 'dy': status[3]}
		return statusDict

	def parseScan(self,x, y):
		scan = self.scan(x, y).split(" ")[1:-1]
		print(scan)
		print("GOOOO\n\n")
		i = 0
		mines = []
		t2={}
		while (i<len(scan) and scan[i] != 'MINES'):
			i += 1
		i += 1
		while (i<len(scan) and scan[i] != 'PLAYERS'):
			mines.append(scan[i])
			i += 1
		i += 1
		if(len(mines)==1):
			mines=[]
		else:
			mines=mines[1:]
			t=[]
			for i in range(len(mines)/3):
				#t2.append(mines[3*i])
				t2[mines[3*i]]=(float(mines[3*i + 1]),float(mines[3*i + 2]))
				t.append((float(mines[3*i + 1]),float(mines[3*i + 2])))
			mines=t[:]
		players = []
		while (i<len(scan) and scan[i] != 'BOMBS'):
			players.append(scan[i])
			i += 1
		i += 1
		bombs = []
		while (i < len(scan)):
			bombs.append(scan[i])
			i += 1
		print(scan[0])
		print(scan[0])
		print(scan[0])
		scanDict = {'MINEPLAYER':t2 }
		return scanDict

	def score(self):
		return self.run("SCOREBOARD")
	def bomb(self, x, y, t=None):
		if t is not None:
			return self.run("BOMB %f %f %d"%(x, y, t))
		else:
			return self.run("BOMB %f %f"%(x, y))
	def scan(self,x, y):
		return run("SCAN %f %f"%(x, y))

	def goTo(self, final):
	    # finding direction
	    i = 0
	    while (i < 30):
	    	self.brake()
	    	i += 1
	    d = self.parseStatus()
	    direction = [final[0] - self.position[0],self.position[1] - final[1]]
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
	    acceleration = [direction[0]-velocity_normalized[0],  velocity_normalized[1] - direction[1]]
	    normalized = math.sqrt( math.pow(acceleration[0], 2) + math.pow(acceleration[1], 2))
	    #print(direction[0])
	    #print(self.position[0])
	    #print(final[0])
	    #print(direction[1])
	    #print(self.position[1])
	    #print(final[1])
	    acc_rads = math.atan2(acceleration[1]/normalized,acceleration[0]/normalized)
	    print(math.degrees(acc_rads))
	    acc_rads =  (0 - acc_rads) if acc_rads < 0 else (3.14 * 2) - acc_rads

	    #acceleration[0] = math.atan2(acceleration[0]/normalized)
	    #acceleration[1] = math.atan2(acceleration[1]/normalized)

	    stuck_counter = 0
	    while True:
	    	print "looping"
	    	d = self.parseStatus()
	    	acc_rads = self.updateAcc_Rads(final)
	    	self.accelerate(acc_rads, 1)#min(30.0,(self.position[0]-final[0])**2 + (self.position[1]-final[1])**2)/60.0)
	    	distance = math.sqrt((self.position[0]-final[0])**2 + (self.position[1]-final[1])**2)
	    	print(distance)
	    	if (distance >= 8) and (distance <= 43):
	    		stuck_counter += 1
	    	if (stuck_counter > 20):
	    		break
	    	if(distance > 700):
	    		self.bomb(self.position[0] - 2, self.position[1] - 2, 60)
	    		break
	    	if "jmv" in d.get("MINEPLAYER"):
	    		self.bomb(self.position[0] - 1, self.position[1] - 2, 60)
	    		break;

		#self.accelerate(radians, 1)
		#var = math.sqrt(((self.position[0] - final[0])**2) +((self.position[1] - final[1])**2))
	def updateAcc_RadsS(self, final):
		distance = math.sqrt((self.position[0]-final[0])**2 + (self.position[1]-final[1])**2)
		if(distance <= 300):#700 before
			for i in range(5):
				self.brake()
		direction = [final[0] - self.position[0],self.position[1] - final[1]]
		normalized = math.sqrt(math.pow(direction[0], 2) + math.pow(direction[1], 2))
		direction[0] = direction[0]/normalized
		direction[1] = direction[1]/normalized
		acc_rads = math.atan2(direction[1],direction[0])
		acc_rads =  0 - acc_rads if acc_rads < 0 else 3.14 * 2 - acc_rads
		return acc_rads
	def updateAcc_Rads(self, final):
		distance = math.sqrt((self.position[0]-final[0])**2 + (self.position[1]-final[1])**2)
		if(distance <= 700):#700 before
			for i in range(5):
				self.brake()
		direction = [final[0] - self.position[0],self.position[1] - final[1]]
		normalized = math.sqrt(math.pow(direction[0], 2) + math.pow(direction[1], 2))
		direction[0] = direction[0]/normalized
		direction[1] = direction[1]/normalized
		acc_rads = math.atan2(direction[1],direction[0])
		acc_rads =  0 - acc_rads if acc_rads < 0 else 3.14 * 2 - acc_rads
		return acc_rads

	def goToS(self, final):
	    # finding direction
	    i = 0
	    while (i < 8):
	    	self.brake()
	    	i += 1
	    d = self.parseStatus()
	    direction = [final[0] - self.position[0],self.position[1] - final[1]]
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
	    acceleration = [direction[0]-velocity_normalized[0],  velocity_normalized[1] - direction[1]]
	    normalized = math.sqrt( math.pow(acceleration[0], 2) + math.pow(acceleration[1], 2))
	    #print(direction[0])
	    #print(self.position[0])
	    #print(final[0])
	    #print(direction[1])
	    #print(self.position[1])
	    #print(final[1])
	    acc_rads = math.atan2(acceleration[1]/normalized,acceleration[0]/normalized)
	    print(math.degrees(acc_rads))
	    acc_rads =  (0 - acc_rads) if acc_rads < 0 else (3.14 * 2) - acc_rads

	    #acceleration[0] = math.atan2(acceleration[0]/normalized)
	    #acceleration[1] = math.atan2(acceleration[1]/normalized)

	    stuck_counter = 0
	    while True:
	    	print "looping"
	    	d = self.parseStatus()
	    	acc_rads = self.updateAcc_RadsS(final)
	    	self.accelerate(acc_rads, 1)#min(30.0,(self.position[0]-final[0])**2 + (self.position[1]-final[1])**2)/60.0)
	    	distance = math.sqrt((self.position[0]-final[0])**2 + (self.position[1]-final[1])**2)
	    	print(distance)
	    	if (distance >= 8) and (distance <= 40):
	    		stuck_counter += 1
	    	if (stuck_counter > 20):
	    		break
	    	if "jmv" in d.get("MINEPLAYER"):
	    		self.bomb(self.position[0] - 1, self.position[1] - 1, 60)
	    		break;

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
	radians=math.atan(2*1100.0/10000.0)#400 instead of 150?
	mineSet=set()
	while True:
		p.accelerate(radians, 1)
		#print(p.parseStatus())
		d=p.parseStatus()
		#p.bomb(p.position[0] + 4, p.position[1] + 4,30)
		mines=d.get("MINES")
		minenames=d.get("MINEPLAYER")
		#for i in rangemines:
			#if i not in mineSet:
				#p.goTo(i)
				#mineSet.add(i)

		for i in minenames:
			if i != 'jmv':
				p.goTo(minenames[i])
				mineSet.add(minenames[i])
		print(d)
		print(mineSet)
		for i in mineSet:
			if (math.sqrt((p.position[0]-i[0])**2 + (p.position[1]-i[1])**2)<=1500):
				s=p.parseScan(i[0],i[1])
				t1=s.get("MINEPLAYER")
				if i in t1:
					if i!="jmv":
						p.goToS(minenames[i])



		# print(p.score())
		#print(p.game.config)

# I don't want to mess with your code, but I think that you should run each of the commands, and see what happens, to some extent, this does look like an AI contest
# But there's a bunch of things that you would wnat to do first.
