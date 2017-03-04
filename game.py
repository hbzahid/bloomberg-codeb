import time
import os
import seaborn as sns
import pandas as pd
import logging
import clientpy2 as cp
from collections import defaultdict

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
		while status[i] != 'MINES':
			i += 1
		i += 1
		while status[i] != 'PLAYERS':
			mines.append(status[i])
			i += 1
		i += 1
		players = []
		while status[i] != 'BOMBS':
			players.append(status[i])
			i += 1
		i += 1
		bombs = []
		while i < len(status):
			bombs.append(status[i])
			i += 1
		statusDict = {'MINES': mines, 'PLAYERS': players, 'BOMBS': bombs, 'x': status[0], 'y': status[1],
						'dx': status[2], 'dy': status[3]}
		return statusDict

	def score(self):
		return self.run("SCOREBOARD")


class Strategy(object):
    def __init__(self):
        self.refined_options = None
        self.json_struct = [{"time": "", "mines": [{"x": "", "y": ""}], "bombs": [{"x": "", "y": ""}],
                             "info": ""}]
        # self.params = time, mines [mines_locations], players: , bombs [bombs_locations]: , info:

    def _refine(self, status_dict):
        logging.warn("Tuning the refinement params")


    def create_data(curr_json, curr_data):
        curr_json.append(curr_data)  # It's a little more complicated than this, but you get the idea
        # you want to update a json object to use
        return self.json_struct





class DataVizualize(object):
    def __init__(self, type, data):
        self.type = type

    def draw(self):
        if self.type = "distplot":
            sns.distplot(x=data['x'], data=data)
        elif self.type = "barplot":
            sns.barplot(x=data['x'], y=data['y'], data=data)
        else:
            logging.warn "unknown type, please add a type for this exception"




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
	while True:
		p.accelerate(3.14, 1)
		print(p.parseStatus())



'''
simple example of seaborn's functionality
x = pd.Series([1,2,3,4,5)
sns.distplot(x=x)
y= pd.Series([1,2,3,4,5])
sns.barplot(x=x, y=y)
'''