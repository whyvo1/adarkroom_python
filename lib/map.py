import random
import lib.gacha

class Point:
	def __init__(self, name, char):
		self.name = name
		self.char = char

	def onStep(self, adventure) -> str:
		return ""

	def getChar(self):
		return ""

	def getHoverTip(self, adventure):
		return adventure.getLangValue("point." + self.name)

class Null(Point):
	def __init__(self):
		super().__init__("null", " ")

	def onStep(self, adventure):
		return ""

	def getHoverTip(self, adventure):
		return ""

class Village(Point):
	def __init__(self):
		super().__init__("village", "V")

	def onStep(self, adventure):
		adventure.back()
		return ""

class Plain(Point):
	def __init__(self):
		super().__init__("plain", ".")

	def onStep(self, adventure):
		return "path"

	def getHoverTip(self, adventure):
		return ""

class Path(Point):
	def __init__(self):
		super().__init__("path", "#")

	def onStep(self, adventure):
		return ""

	def getHoverTip(self, adventure):
		return ""

class Dessert(Point):
	def __init__(self):
		super().__init__("dessert", ",")

	def onStep(self, adventure):
		return "path"

	def getHoverTip(self, adventure):
		return ""

class Outpost(Point):
	def __init__(self):
		super().__init__("outpost", "P")

	def onStep(self, adventure):
		return "path"

class Map:
	BORN_POS = (30, 30)

	def __init__(self, adventure):
		self.points = [[getPoint("null")] * 59]
		for i in range(98):
			self.points.append([getPoint("null")] * 59)
		self.adventure = adventure
		self.seed = int(random.random() * 65536)
		self.generateAround(Map.BORN_POS)
		self.setPoint((30, 30), "village")
		self.adventure.triggerEvent("enter_map")

	def setPoint(self, pos, name):
		self.points[pos[1]][pos[0]] = getPoint(name)

	def getSight(self):
		return 3

	def generateAround(self, pos):
		sight = self.getSight()
		for i in range(-sight, sight + 1):
			ai = abs(i)
			for j in range(-sight + ai, sight - ai + 1):
				if self.points[pos[1] + i][pos[0] + j].name == "null":
					self.generate((pos[0] + j, pos[1] + i))

	def step(self, pos):
		self.generateAround(pos)
		s = self.points[pos[1]][pos[0]].onStep(self.adventure)
		if s != "":
			self.setPoint(pos, s)

	def generate(self, pos):
		self.setPoint(pos, "plain")

	def cleanPaths(self):
		i = 0
		while i < 59:
			j = 0
			while j < 59:
				if self.points[i][j].name == "path":
					self.setPoint((j, i), "plain")
				j += 1
			i += 1

	def getStrings(self):
		l = []
		i = 0
		while i < 59:
			l.append("")
			j = 0
			while j < 59:
				l[i] += self.points[i][j].char
				j += 1
			i += 1
		return l

	def fromStrings(self, strings):
		i = 0
		while i < 59:
			j = 0
			while j < 59:
				self.points[i][j] = getPointOf(strings[i][j])
				j += 1
			i += 1

ALL_POINTS = [Null(), Village(), Plain(), Path(), Dessert(), Outpost()]

def getPoint(name):
	for point in ALL_POINTS:
		if point.name == name:
			return point

def getPointOf(char):
	for point in ALL_POINTS:
		if point.char == char:
			return point
	return ALL_POINTS[0]