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
