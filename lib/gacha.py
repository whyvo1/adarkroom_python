import random

class GachaItem:
	def __init__(self, obj, weight: int, seed = None):
		if not isinstance(weight, int):
			raise ValueError("Weight should be integer")
		if weight < 0:
			raise ValueError("Weight is negative")
		self.obj = obj
		self.weight = weight

	def __str__(self):
		return str(self.obj) + " Gacha Item weighs " + str(self.weight)

	def __eq__(self, other):
		if not isinstance(other, GachaItem):
			return False
		return self.obj == other.obj and self.weight == other.weight

	def __ne__(self, other):
		if not isinstance(other, GachaItem):
			return True
		return self.obj != other.obj or self.weight != other.weight

	def __hash__(self):
		return hash((self.obj, self.weight))

class Gacha:
	def __init__(self):
		self.__gachaItems = []
		self.__totalWeight = 0
		self.__size = 0
		self.random = random.Random()

	def add(self, obj, weight: int):
		self.__gachaItems.append(GachaItem(obj, weight))
		self.__totalWeight += weight
		self.__size += 1

	def removeOf(self, obj, order = 0) -> bool:
		j, i = 0, 0
		while i < self.__size:
			if self.__gachaItems[i].obj == obj:
				if j >= order:
					self.remove(i)
					return True
				j += 1
			i += 1
		return False

	def removeOfAll(self, obj):
		i = 0
		while i < self.__size:
			if self.__gachaItems[i].obj == obj:
				self.remove(i)
			else:
				i += 1

	def remove(self, index = -1):
		self.__totalWeight -= self.__gachaItems[index].weight
		del self.__gachaItems[index]
		self.__size -= 1

	def clear(self):
		self.__gachaItems.clear()
		self.__totalWeight = 0
		self.__size = 0

	def setWeight(self, weight: int, index = -1):
		if not isinstance(weight, int):
			raise ValueError("Weight should be integer")
		if weight < 0:
			raise ValueError("Weight is negative")
		self.__totalWeight += weight - self.__gachaItems[index].weight
		self.__gachaItems[index].weight = weight

	def getWeightOf(self, obj, order = 0) -> int:
		j, i = 0, 0
		while (i < self.__size):
			if self.__gachaItems[i].obj == obj:
				if j >= order:
					return self.__gachaItems[i].weight
				j += 1
			i += 1
		return -1

	def getWeight(self, index = -1) -> int:
		return self.__gachaItems[index].weight

	def getTotalWeight(self) -> int:
		return self.__totalWeight

	def getChanceOf(self, obj, order = 0) -> float:
		return self.getWeightOf(obj, order) / self.__totalWeight

	def getChance(self, index = -1) -> float:
		return self.__gachaItems[index].weight / self.__totalWeight

	def setObj(self, obj, index = -1):
		self.__gachaItems[index].obj = obj

	def getObj(self, index = -1):
		return self.__gachaItems[index].obj

	def size(self):
		return self.__size

	def getObjs(self) -> list:
		list0 = []
		for item in self.__gachaItems:
			list0.append(item.obj)
		return list0

	def getWeights(self) -> list:
		list0 = []
		for item in self.__gachaItems:
			list0.append(item.weight)
		return list0

	def copy(self):
		return Gacha.create(self.__gachaItems.copy())

	@staticmethod
	def createFromLists(objList, weightList):
		size = len(objList)
		if (size != len(weightList)):
			raise ValueError("Lists' sizes are inequal")
		gacha = Gacha()
		i = 0
		for weight in weightList:
			gacha.add(objList[i], weight)
			i += 1
		gacha.__size = size
		return gacha

	@staticmethod
	def create(itemList):
		'''
		Param 'itemList': a 'GachaItem' list
		'''
		gacha = Gacha()
		for item in itemList:
			if not isinstance(item, GachaItem):
				raise ValueError("List element should be 'GachaItem'")
			gacha.__totalWeight += item.weight
		gacha.__gachaItems = itemList
		gacha.__size = len(itemList)
		return gacha

	def draw(self, seed = None, remove = False):
		'''
		Draws an object from this Gacha.

		Param 'remove': whether to remove the chosen object

		Returns the chosen object.
		'''
		if self.__size <= 0:
			raise RuntimeError("Gacha is empty")
		if self.__totalWeight <= 0:
			raise RuntimeError("Gacha's total weight is 0")
		self.random.seed(seed)
		rand = self.random.random() * self.__totalWeight
		accum = 0
		i = 0
		while i < self.__size:
			accum += self.__gachaItems[i].weight
			if rand <= accum:
				if remove:
					tmp = self.__gachaItems[i].obj
					del self.__gachaItems[i]
					return tmp
				else:
					return self.__gachaItems[i].obj
			i += 1
		return self.__gachaItems[-1].obj

	def drawFor(self, times: int, seed = None, remove = False):
		'''
		Draws objects from this Gacha.


		Param 'times': how many objects will be chosen
		      'remove': whether to remove the chosen object

		Returns the chosen objects.
		'''
		if (remove and times > self.__size):
			raise ValueError("Gacha size is not so large")
		self.random.seed(seed)
		li = []
		i = 0
		while i < times:
			li.append(self.draw(None, remove))
			i += 1
		return li

	def __str__(self):
		if self.__size <= 0:
			s = "Gacha empty"
		else:
			s = "Gacha size " + str(self.__size) + ":\n"
			for item in self.__gachaItems:
				s += "\t" + str(item.obj) + " weighs " + str(item.weight) + "\n"
		s += "Total weight " + str(self.__totalWeight) + "\n"
		return s

	def __eq__(self, other):
		if not isinstance(other, Gacha):
			return False
		return self.__gachaItems == other.__gachaItems

	def __ne__(self, other):
		if not isinstance(other, Gacha):
			return True
		return self.__gachaItems != other.__gachaItems

	def __hash__(self):
		return hash(tuple(self.__gachaItems))