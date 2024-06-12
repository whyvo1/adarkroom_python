import json, random, os
from lib import button
from lib import info
from lib import map
from lib import gacha

def mergeItemStacks(list0, list1):
	for itemStack1 in list1:
		bl = True
		for itemStack0 in list0:
			if itemStack0.item == itemStack1.item:
				itemStack0.add(itemStack1.count)
				bl = False
				break
		if bl:
			list0.append(itemStack1)

def getAvailableLanguages():
	with open("lang/langs.json", "r", encoding = "utf8") as f:
		return list(json.loads(f.read()).keys())

class ItemStack:
	WEIGHT_0 = ["bullet", "amulet"]
	WEIGHT_2 = ["spear"]
	WEIGHT_3 = ["iron_sword", "steel_sword"]
	WEIGHT_5 = ["rifle", "laser_rifle"]

	def __init__(self, item: str, count: int):
		self.item = item
		self.count = count

	def isOf(self, item: str) -> bool:
		return self.item == item

	def add(self, count):
		self.count += count

	def getKey(self) -> str:
		return "item." + self.item

	def getWeight(self):
		if self.item in ItemStack.WEIGHT_0:
			return 0
		if self.item in ItemStack.WEIGHT_2:
			return 2
		if self.item in ItemStack.WEIGHT_3:
			return 3
		if self.item in ItemStack.WEIGHT_5:
			return 5
		return 1

	@staticmethod
	def getItemWeight(item):
		if item in ItemStack.WEIGHT_0:
			return 0
		if item in ItemStack.WEIGHT_2:
			return 2
		if item in ItemStack.WEIGHT_3:
			return 3
		if item in ItemStack.WEIGHT_5:
			return 5
		return 1

	def __str__(self):
		return str(self.count) + " " + self.item

class Inventory:
	def __init__(self):
		self.__itemStacks = []

	def add(self, item: str, count) -> bool:
		if count >= 0:
			i = self.find(item)
			if i >= 0:
				self.__itemStacks[i].add(count)
			else:
				self.__itemStacks.append(ItemStack(item, count))
		else:
			i = self.find(item, -count)
			if i < 0:
				return False
			self.__itemStacks[i].add(count)
		return True

	def decline(self, item, count):
		for itemStack in self.__itemStacks:
			if itemStack.item == item:
				if itemStack.count - count < 0:
					count = itemStack.count
				itemStack.count -= count

	def addAll(self, itemStacks) -> bool:
		count = 0
		for itemStack in itemStacks:
			count += itemStack.count
		for itemStack in itemStacks:
			if itemStack.count < 0 and not self.has(itemStack.item, -itemStack.count):
				return False
		for itemStack in itemStacks:
			self.add(itemStack.item, itemStack.count)
		return True

	def removeAll(self, itemStacks) -> int:
		i = 0
		for itemStack in itemStacks:
			if not self.has(itemStack.item, itemStack.count):
				return i
			i += 1
		for itemStack in itemStacks:
			self.add(itemStack.item, -itemStack.count)
		return -1

	def find(self, item, count = 0) -> int:
		i = 0
		for itemStack in self.__itemStacks:
			if itemStack.isOf(item) and itemStack.count >= count:
				return i
			i += 1
		return -1

	def has(self, item, count = 1):
		for itemStack in self.__itemStacks:
			if itemStack.isOf(item) and itemStack.count >= count:
				return True
		return False

	def getCount(self, item):
		for itemStack in self.__itemStacks:
			if itemStack.isOf(item):
				return itemStack.count
		return 0

	def getItemStacks(self):
		return self.__itemStacks

	def toDict(self):
		dict0 = {}
		for itemStack in self.__itemStacks:
			dict0[itemStack.item] = itemStack.count
		return dict0

	def fromDict(self, dic):
		self.__itemStacks.clear()
		for item, count in dic.items():
			self.__itemStacks.append(ItemStack(item, count))

	@staticmethod
	def create(itemStackList, volumn = -1):
		inventory = Inventory()
		inventory.__itemStacks = itemStackList
		return inventory

class AdventureInventory:
	def __init__(self):
		self.itemStacks = []
		self.occupied = 0

	def increase(self, item, count):
		i = self.find(item)
		if i >= 0:
			self.itemStacks[i].add(count)
		else:
			self.itemStacks.append(ItemStack(item, count))
		self.occupied += count * ItemStack.getItemWeight(item)

	def decline(self, item, count) -> bool:
		for i in range(len(self.itemStacks)):
			if self.itemStacks[i].isOf(item):
				if self.itemStacks[i].count - count < 0:
					return False
				self.itemStacks[i].count -= count
				if self.itemStacks[i].count == 0:
					del self.itemStacks[i]
				self.occupied -= count * ItemStack.getItemWeight(item)
				return True
		return False

	def find(self, item, count = 0) -> int:
		i = 0
		for itemStack in self.itemStacks:
			if itemStack.isOf(item) and itemStack.count >= count:
				return i
			i += 1
		return -1

	def has(self, item, count = 1):
		for itemStack in self.itemStacks:
			if itemStack.isOf(item) and itemStack.count >= count:
				return True
		return False

	def getCount(self, item):
		for itemStack in self.itemStacks:
			if itemStack.isOf(item):
				return itemStack.count
		return 0

	def clear(self):
		self.itemStacks.clear()
		self.occupied = 0

class Career:
	def __init__(self, name: str, count):
		self.name = name
		self.count = count

	def workResult(self) -> list:
		return []
		
	def isOf(self, name: str):
		return self.name == name

	def add(self, count):
		self.count += count

	def unlock(self):
		self.count = 0

	def isUnlocked(self):
		return self.count >= 0

	def __str__(self):
		return str(self.count) + " " + self.name

class Logger(Career):
	def __init__(self, count = -1):
		super().__init__("logger", count)

	def workResult(self):
		return [ItemStack("wood", self.count)]

class Hunter(Career):
	def __init__(self, count = -1):
		super().__init__("hunter", count)

	def workResult(self):
		return [ItemStack("fur", self.count), ItemStack("flesh", self.count)]

class Trapper(Career):
	def __init__(self, count = -1):
		super().__init__("trapper", count)

	def workResult(self):
		return [ItemStack("flesh", -self.count), ItemStack("bait", self.count)]

class Smoker(Career):
	def __init__(self, count = -1):
		super().__init__("smoker", count)

	def workResult(self):
		return [ItemStack("flesh", -self.count * 5), ItemStack("wood", -self.count * 5), ItemStack("smoked_meat", self.count * 2)]

class Tanner(Career):
	def __init__(self, count = -1):
		super().__init__("tanner", count)

	def workResult(self):
		return [ItemStack("fur", -self.count * 5), ItemStack("smoked_meat", -self.count), ItemStack("leather", self.count)]

class Village:
	def __init__(self):
		self.level = "quiet_village"
		self.population = 0
		self.maxPopulation = 0
		self.careers = [
			Logger(0),
			Hunter(),
			Trapper(),
			Smoker(),
			Tanner()
		]
		self.buildings = Inventory()

	def addPopulation(self, count):
		if self.population + count > self.maxPopulation:
			count = self.maxPopulation - self.population
		self.population += count
		self.careers[0].count += count

	def expandPopulation(self, count):
		self.maxPopulation += count
		if self.maxPopulation >= 64:
			self.level = "big_town"
		elif self.maxPopulation >= 48:
			self.level = "medium_town"
		elif self.maxPopulation >= 32:
			self.level = "small_town"
		elif self.maxPopulation >= 16:
			self.level = "noisy_village"

	def addCareer(self, name, count):
		if name != "logger":
			self.careers[0].add(count)
			return
		if self.careers[0].count + count < 0:
			return
		bl = False
		for career in self.careers:
			if career.isOf(name) and career.isUnlocked():
				if career.count + count >= 0:
					career.add(count)
					bl = True
				break
		if bl:
			self.careers[0].add(-count)

	def addCareerIn(self, index, count):
		if index == 0:
			self.careers[0].add(count)
			return
		if self.careers[0].count - count < 0:
			return
		i = 0
		bl = False
		for career in self.careers:
			if not career.isUnlocked():
				continue
			if i == index:
				if self.careers[index].count + count >= 0:
					self.careers[index].add(count)
					bl = True
				break
			i += 1
		if bl:
			self.careers[0].add(-count)

	def getUnlockedCareerCount(self):
		c = 0
		for career in self.careers:
			if career.isUnlocked():
				c += 1
		return c

	def getUnlockedCareers(self):
		list0 = []
		for career in self.careers:
			if career.isUnlocked():
				list0.append(career)
		return list0

	def removePopulation(self, count):
		if self.population < count:
			count = self.population
		self.population -= count
		for career in self.careers:
			if not career.isUnlocked():
				continue
			if count >= career.count:
				count -= career.count
				career.count = 0
			else:
				career.add(-count)
				break

	def unlockCareer(self, name):
		for career0 in self.careers:
			if career0.isOf(name):
				career0.unlock()

	def isCareerUnlocked(self, name):
		for career0 in self.careers:
			if career0.isOf(name):
				return career0.isUnlocked()
		return False

	def getRestPopulation(self):
		return self.maxPopulation - self.population

	def toDict(self):
		dict0 = {
			"level": self.level,
			"population": self.population,
			"max_population": self.maxPopulation,
			"buildings": self.buildings.toDict()
		}
		dict1 = {}
		for career in self.careers:
			dict1[career.name] = career.count
		dict0["careers"] = dict1
		return dict0

	def fromDict(self, dic):
		self.level = dic["level"]
		self.population = dic["population"]
		self.maxPopulation = dic["max_population"]
		self.buildings.fromDict(dic["buildings"])
		for name, count in dic["careers"].items():
			for c in self.careers:
				if c.isOf(name):
					c.count = count

class World:
	def __init__(self):
		self.__logger = info.LoggerRow(200, 700, 16)
		self.__progress = 0
		self.__langFile = {}

		with open("lang/langs.json", "r", encoding = "utf8") as f:
			self.__langs = json.loads(f.read())

		self.__lang = "zh_cn"
		self.__inventory = Inventory()
		self.__village = Village()
		self.__events = [
			MakeFire(),
			AddFuel(),
			CollectWood(),
			ConstructCart(),
			ConstructTrap(),
			ConstructHouse(),
			CheckTraps(),
			SmallGroupCome(),
			FamilyCome(),
			OneCome(),
			ConstructHunterHouse(),
			ConstructTradingPost(),
			Trade("scale", [ItemStack("fur", 150)]),
			Trade("tooth", [ItemStack("fur", 200)]),
			TradeCompass(),
			ConstructSmokehouse(),
			ConstructTannery(),
			ConstructWorkshop(),
			Craft("torch", [ItemStack("wood", 50), ItemStack("fabric", 10)]),
			CraftEquipment("backpack", [ItemStack("leather", 100)]),
			CraftEquipment("kettle", [ItemStack("leather", 80)]),
			Craft("spear", [ItemStack("wood", 100), ItemStack("fabric", 10)]),
			CraftEquipment("leather_armor", [ItemStack("leather", 300), ItemStack("fabric", 40)]),
			FurReward(),
			Start()
		]
		self.__popUpEvents = [
			MonsterAttack(),
			PopUpOk(),
			TrapDestroyed(),
			TrapDestroyedExplore(),
			WoodStolen(),
			WoodStolenCheck(),
			FurRequire(),
			FurRequireGive(200),
			FurRequireGive(500),
			FurRequireGive(1000),
			ConsoleSaves(),
			SavesLoad(),
			SavesSave(),
			ConsoleRestart(),
			Restart(),
			ConsoleLanguage()
		]
		self.__fireLit = False
		self.__properties = Properties()
		self.__equiments = Equipments()
		self.__houseWarmth = 0
		self.currentColumn = "house"

		self.itemTab0 = info.ItemTab("village", 240, 28, self.__village.buildings.getItemStacks())
		self.itemTab1 = info.ItemTab("items", 240, 28, self.__inventory.getItemStacks())

		self.__comeGacha0 = gacha.Gacha.createFromLists(["one_come", "family_come", "small_group_come"], [1, 3, 9])
		self.__comeGacha1 = gacha.Gacha.createFromLists(["one_come", "family_come"], [1, 3])

		self.__sufferingGacha = gacha.Gacha.createFromLists(["monster_attack", "trap_destroyed", "wood_stolen", "fur_require"], [3, 3, 4, 2])

		self.careerActionBar = info.CareerActionBar(40, self.__village, (540, 100))
		self.__popUps = []

		self.__justSuffered = True
		self.__canFurReward = True
		self.__onAdventure = False

		self.__adventureInventory = AdventureInventory()
		self.adventurePreparationTab = info.AdventurePreparationTab((330, 100), 320, 36, self.__adventureInventory)
		self.adventureHang = False
		self.mapStrings = []
		self.mapSeed = -1

		self.hangLoading = -1
		self.hangSaving = -1
		self.hangRestart = False

	def setLang(self, lang: str):
		self.__lang = lang
		with open("lang/" + self.__lang + ".json", encoding = "utf8") as langFile:
			self.__langFile = json.loads(langFile.read())

	def getLang(self):
		return self.__lang

	def getLangValue(self, key: str, *args, raw = True):
		if len(args) > 0:
			if raw:
				list0 = []
				for arg in args:
					list0.append(self.__langFile.get(arg, arg))
				string = self.__langFile.get(key, key).format(*list0)
			else:
				string = self.__langFile.get(key, key).format(*args)
			return string
		return self.__langFile.get(key, key)

	def hasLang(self, name):
		return os.path.isfile("lang/" + name + '.json')

	def getNameInLang(self, name):
		return self.__langs[name]

	def changeColume(self, name: str):
		self.currentColumn = name

	def shouldRenderCareerActionBar(self):
		return self.currentColumn == "village" and self.__village.population > 0

	def getButtons(self):
		buttons = []
		if self.currentColumn == "house":
			if self.__fireLit:
				buttons.append(ADD_FUEL_BUTTON)
			else:
				buttons.append(MAKE_FIRE_BUTTON)

			if self.__properties.test("can_construct"):
				buttons.append(CONSTRUCT_CART_BUTTON)
			if self.__properties.test("can_construct0"):
				buttons.append(CONSTRUCT_TRAP_BUTTON)
				buttons.append(CONSTRUCT_HOUSE_BUTTON)
			if self.__properties.test("can_construct1"):
				buttons.append(CONSTRUCT_HUNTER_HOUSE_BUTTON)
			if self.__properties.test("can_construct2"):
				buttons.append(CONSTRUCT_TRADING_POST_BUTTON)
			if self.__properties.test("can_construct3"):
				buttons.append(CONSTRUCT_SMOKEHOUSE_BUTTON)
			if self.__properties.test("can_construct4"):
				buttons.append(CONSTRUCT_TANNERY_BUTTON)
			if self.__properties.test("can_construct5"):
				buttons.append(CONSTRUCT_WORKSHOP_BUTTON)

			if self.__properties.test("can_trade"):
				buttons.append(TRADE_SCALE_BUTTON)
				buttons.append(TRADE_TOOTH_BUTTON)
				buttons.append(TRADE_COMPASS_BUTTON)

			if self.__properties.test("can_craft"):
				buttons.append(CRAFT_TORCH_BUTTON)
				buttons.append(CRAFT_BACKPACK_BUTTON)
				buttons.append(CRAFT_KETTLE_BUTTON)
				buttons.append(CRAFT_SPEAR_BUTTON)
				buttons.append(CRAFT_LEATHER_ARMOR_BUTTON)
		elif self.currentColumn == "village":
			buttons.append(COLLECT_WOOD_BUTTON)
			if self.__properties.test("can_check_traps"):
				buttons.append(CHECK_TRAPS_BUTTON)
		elif self.currentColumn == "adventure":
			buttons.append(START_BUTTON)
		return buttons

	def getColumns(self) -> list:
		list0 = ["house"]
		if self.__properties.test("first_person_came"):
			list0.append("village")
		if self.__inventory.has("compass"):
			list0.append("adventure")
		return list0

	def getColumnBar(self):
		bar = info.ColumnBar()
		dx = 0
		for column in self.getColumns():
			bl = False
			if column == self.currentColumn:
				bl = True
			if column == "village":
				column += "." + self.__village.level
			button0 = button.ColumnButton(column, (350 + dx, 40), self)
			button0.setOn(bl)
			bar.addButton(button0)
			dx += button0.rect.width + 40
		return bar

	def getItemTabs(self):
		if len(self.__village.buildings.getItemStacks()) > 0:
			if self.__village.maxPopulation > 0:
				self.itemTab0.offName = str(self.__village.population) + "/" + str(self.__village.maxPopulation)
			return [self.itemTab0, self.itemTab1]
		return [self.itemTab1]

	def getConsoleBar(self):
		bar = info.ConsoleBar()
		dx = 1200
		for console in ["language", "restart", "saves"]:
			button0 = button.ConsoleButton(console, self)
			dx -= button0.rect.width + 30
			button0.setPos((dx, 915))
			bar.addButton(button0)
		return bar

	def addItem(self, item, count) -> bool:
		return self.__inventory.add(item, count)

	def declineItem(self, item, count):
		self.__inventory.decline(item, count)

	def addItemAll(self, itemStacks):
		return self.__inventory.addAll(itemStacks)

	def removeItemAll(self, itemStacks) -> int:
		return self.__inventory.removeAll(itemStacks)

	def hasItem(self, name, count = 1):
		return self.__inventory.has(name, count)

	def getItemCount(self, name):
		return self.__inventory.getCount(name)

	def addBuilding(self, name, count):
		self.__village.buildings.add(name, count)

	def declineBuilding(self, name, count):
		self.__village.buildings.decline(name, count)

	def hasBuilding(self, name, count = 1):
		return self.__village.buildings.has(name, count)

	def getBuildingCount(self, name):
		return self.__village.buildings.getCount(name)

	def getPopulation(self):
		return self.__village.population

	def getMaxPopulation(self):
		return self.__village.maxPopulation

	def addEquipment(self, name):
		self.__equiments.add(name)

	def hasEquipment(self, name):
		return self.__equiments.has(name)

	def getStorageVolumn(self):
		return self.__equiments.getStorageVolumn()

	def getVesselVolumn(self):
		return self.__equiments.getVesselVolumn()

	def getArmorEquipment(self):
		return self.__equiments.getArmor()

	def triggerProperty(self, name, value) -> bool:
		return self.__properties.trigger(name, value)

	def triggerPropertyOn(self, name) -> bool:
		return self.__properties.trigger(name, True)

	def triggerPropertyOff(self, name) -> bool:
		return self.__properties.trigger(name, False)

	def testProperty(self, name):
		return self.__properties.test(name)

	def getProgress(self):
		return self.__progress

	def putPopUp(self, popUp):
		self.__popUps.append(popUp)

	def hasPopUp(self):
		return len(self.__popUps) > 0

	def getTopPopUp(self):
		if len(self.__popUps) == 0:
			return
		return self.__popUps[-1]

	def removePopUp(self):
		if len(self.__popUps) == 0:
			return
		del self.__popUps[-1]

	def addLoggerMessage(self, name: str, *args, raw = True):
		self.__logger.addMessage(self.getLangValue("log." + name, *args, raw = raw))

	def renderLogger(self, screen, pos):
		self.__logger.render(screen, pos)

	def newCareer(self, career):
		self.__village.unlockCareer(career)

	def addCareer(self, name: str, count):
		self.__village.addCareer(career, count)

	def addPopulation(self, count):
		if count >= 0:
			self.__village.addPopulation(count)
		else:
			self.__village.removePopulation(-count)

	def expandPopulation(self, count):
		self.__village.expandPopulation(count)

	def getRestPopulation(self):
		return self.__village.getRestPopulation()

	def lightFire(self):
		self.__fireLit = True
		ADD_FUEL_BUTTON.setOnCool()

	def work(self):
		self.addItemAll(self.getWorkResults())

	def getWorkResults(self) -> list:
		list0 = []
		if self.__properties.test("first_person_came"):
			list0.append(ItemStack("wood", 2))
		for career in self.__village.careers:
			if not career.isUnlocked():
				continue
			mergeItemStacks(list0, career.workResult())
		i = 0
		while i < len(list0):
			if list0[i].count == 0:
				del list0[i]
				continue
			i += 1
		return list0

	def triggerEvent(self, name: str) -> bool:
		i = 0
		for event in self.__events:
			if event.name == name:
				return event.trigger(self)
		return False

	def triggerPopUpEvent(self, name) -> bool:
		i = 0
		for event in self.__popUpEvents:
			if event.name == name:
				return event.trigger(self)
		return False

	def handleCome(self):
		rp = self.getRestPopulation()
		if rp > 0:
			if random.random() > 0.6:
				if rp > 6:
					self.triggerEvent(self.__comeGacha0.draw())
				elif rp > 3:
					self.triggerEvent(self.__comeGacha1.draw())
				else:
					self.triggerEvent("one_come")

	def sufferEvent(self):
		self.triggerPopUpEvent(self.__sufferingGacha.draw())
		self.__justSuffered = True

	def run(self):
		self.work()
		if self.__houseWarmth > 3:
			self.firstPersonCome()

		if self.__properties.test("can_construct"):
			if self.__inventory.has("wood", 50):
				self.triggerPropertyOn("can_construct0")
			if self.__inventory.has("wood", 150) and self.__inventory.has("fur") and self.__inventory.has("flesh"):
				if not self.__properties.test("can_construct1"):
					self.addLoggerMessage("notice_hunter_house")
					self.triggerPropertyOn("can_construct1")
			if self.__inventory.has("wood", 280) and self.__inventory.has("fur", 50):
				if not self.__properties.test("can_construct2"):
					self.addLoggerMessage("notice_trading_post")
					self.triggerPropertyOn("can_construct2")
			if self.__inventory.has("wood", 400) and self.__inventory.has("flesh", 50):
				if not self.__properties.test("can_construct3"):
					self.addLoggerMessage("notice_smokehouse")
					self.triggerPropertyOn("can_construct3")
			if self.__inventory.has("wood", 400) and self.__inventory.has("fur", 150):
				if not self.__properties.test("can_construct4"):
					self.addLoggerMessage("notice_tannery")
					self.triggerPropertyOn("can_construct4")
			if self.__inventory.has("wood", 500) and self.__inventory.has("leather"):
				if not self.__properties.test("can_construct5"):
					self.addLoggerMessage("notice_workshop")
					self.triggerPropertyOn("can_construct5")

		if not self.__properties.test("can_construct") and self.__inventory.has("wood", 20):
			self.addLoggerMessage("can_construct")
			self.addLoggerMessage("notice_cart")
			self.triggerPropertyOn("can_construct")

		if not self.__onAdventure:
			if random.random() >= 0.78:
				self.addHouseWarmth(-1)

			self.addTemperatureLogger()

			self.handleCome()

			if self.__canFurReward and self.__properties.test("fur_reward_count") > 0 and random.random() > 0.75:
				self.triggerEvent("fur_reward")
				self.__properties.trigger("fur_reward_count", 0)
			if not self.__canFurReward:
				self.__canFurReward = True

			if not self.__justSuffered:
				if random.random() > 0.8:
					self.sufferEvent()
			else:
				self.__justSuffered = False

	def addTemperatureLogger(self):
		if self.__houseWarmth < 3:
			self.addLoggerMessage("too_cold")
		elif self.__houseWarmth > 7:
			self.addLoggerMessage("too_hot")

	def firstPersonCome(self):
		if not self.__properties.test("first_person_came"):
			self.triggerPropertyOn("first_person_came")
			self.addLoggerMessage("first_person")

	def createFurReward(self, count):
		self.__canFurReward = False
		self.__properties.trigger("fur_reward_count", count)

	def hasFurReward(self):
		return self.__properties.test("fur_reward_count") > 0

	def getFurRewardCount(self):
		return self.__properties.test("fur_reward_count")

	def addHouseWarmth(self, count: int):
		self.__houseWarmth += count
		if self.__houseWarmth > 10:
			self.__houseWarmth = 10
		elif self.__houseWarmth < 0:
			self.__houseWarmth = 0

	def isHouseWarm(self):
		return self.__houseWarmth > 2

	def canStartAdventure(self):
		if self.__equiments.getVesselVolumn() <= 0:
			return False
		if not self.__adventureInventory.has("smoked_meat"):
			return False
		for itemStack in self.__adventureInventory.itemStacks:
			if not self.__inventory.has(itemStack.item, itemStack.count):
				return False
		return True 

	def startAdventure(self):
		self.__inventory.removeAll(self.__adventureInventory.itemStacks)
		self.__onAdventure = True
		self.adventure = Adventure(self.__equiments.getStorageVolumn(), self.__equiments.getVesselVolumn(), self.__equiments.getHealth(), self.__adventureInventory, self)

	def isOnAdventure(self):
		return self.__onAdventure

	def suspendAdventure(self):
		self.__inventory.addAll(self.__adventureInventory.itemStacks)
		self.__onAdventure = False
		self.mapStrings = self.adventure.map.getStrings()
		self.mapSeed = self.adventure.map.seed
		self.adventureHang = True

	def delAdventure(self):
		if hasattr(self, "adventure"):
			del self.adventure
		self.adventureHang = False

	def hasSave(self, no):
		return os.path.isfile("saves/save" + str(no))

	def load(self, no):
		self.hangLoading = no

	def save(self, no):
		self.hangSaving = no

	def toDict(self):
		return {
			"inventory": self.__inventory.toDict(),
			"village": self.__village.toDict(),
			"properties": self.__properties.toDict(),
			"equiments": self.__equiments.toDict(),
			"map": self.mapStrings,
			"map_seed": self.mapSeed,
			"lang": self.__lang
		}

	def fromDict(self, dic):
		self.__inventory.fromDict(dic["inventory"])
		self.__village.fromDict(dic["village"])
		self.__properties.fromDict(dic["properties"])
		self.__equiments.fromDict(dic["equiments"])
		self.mapStrings = dic["map"]
		self.mapSeed = dic["map_seed"]
		self.setLang(dic["lang"])

class Properties:
	def __init__(self):
		self.dic = {
			"first_person_came": False,
			"can_construct": False,
			"can_construct0": False,
			"can_check_traps": False,
			"can_construct1": False,
			"can_construct2": False,
			"can_trade": False,
			"can_construct3": False,
			"can_construct4": False,
			"can_construct5": False,
			"can_craft": False,
			"can_explore": False,
			"fur_reward_count": 0
		}

	def trigger(self, name: str, value) -> bool:
		if self.dic[name] == value:
			return False
		self.dic[name] = value
		return True

	def test(self, name):
		return self.dic[name]

	def toDict(self):
		return self.dic.copy()

	def fromDict(self, dic):
		self.dic.update(dic)

class Equipments:
	ALL_STORAGES = ["backpack"]
	ALL_VESSELS = ["kettle"]
	ALL_ARMORS = ["leather_armor"]

	def __init__(self):
		self.storages = []
		self.vessels = []
		self.armors = []
		self.storageLevel = -1
		self.vesselLevel = -1
		self.armorLevel = -1

	def add(self, name):
		if name in Equipments.ALL_STORAGES:
			self.storages.append(name)
			l = Equipments.ALL_STORAGES.index(name)
			if l > self.storageLevel:
				self.storageLevel = l
		elif name in Equipments.ALL_VESSELS:
			self.vessels.append(name)
			l = Equipments.ALL_VESSELS.index(name)
			if l > self.vesselLevel:
				self.vesselLevel = l
		elif name in Equipments.ALL_ARMORS:
			self.armors.append(name)
			l = Equipments.ALL_ARMORS.index(name)
			if l > self.armorLevel:
				self.armorLevel = l

	def has(self, name):
		return name in self.storages or name in self.vessels or name in self.armors

	def getStorageVolumn(self):
		if self.storageLevel < 0:
			return 0
		return (self.storageLevel + 1) * 20

	def getVesselVolumn(self):
		if self.vesselLevel < 0:
			return 0
		return (self.storageLevel + 1) * 30

	def getArmor(self):
		if self.armorLevel < 0:
			return "none"
		return Equipments.ALL_ARMORS[self.armorLevel]

	def getHealth(self):
		if self.armorLevel < 0:
			return 20
		return 20 + (self.armorLevel + 1) * 10

	def toDict(self):
		return {
			"storages": self.storages,
			"vessels": self.vessels,
			"armors": self.armors
		}

	def fromDict(self, dic):
		self.storages = dic["storages"]
		for s in self.storages:
			l = Equipments.ALL_STORAGES.index(s)
			if l > self.storageLevel:
				self.storageLevel = l
		self.vessels = dic["vessels"]
		for s in self.vessels:
			l = Equipments.ALL_VESSELS.index(s)
			if l > self.vesselLevel:
				self.vesselLevel = l
		self.armors = dic["armors"]
		for s in self.armors:
			l = Equipments.ALL_ARMORS.index(s)
			if l > self.armorLevel:
				self.armorLevel = l

class Adventure:
	def __init__(self, volumn, water, health, inventory, world):
		self.__volumn = volumn
		self.__water = water
		self.__maxWater = water
		self.__health = health
		self.__maxHealth = health
		self.__inventory = inventory
		self.world = world
		self.__events = [
			EnterMap()
		]
		self.__pos = [30, 30]
		self.map = map.Map(self)
		if len(world.mapStrings) != 0:
			self.map.fromStrings(world.mapStrings)
		if world.mapSeed >= 0:
			self.map.seed = world.mapSeed
		self.itemTab = info.AdventureItemTab(self, (320, 30))
		self.mapSet = info.MapSet(self, (320, 180))

	def back(self):
		self.map.cleanPaths()
		self.world.suspendAdventure()
		return

	def die(self):
		self.__inventory.clear()
		self.back()
		return

	def triggerEvent(self, name: str) -> bool:
		i = 0
		for event in self.__events:
			if event.name == name:
				return event.trigger(self.world)
		return False

	def getVolumn(self):
		return self.__volumn

	def getWater(self):
		return self.__water

	def comsumeWater(self):
		if self.__water == 0:
			self.die()
			return
		self.__water -= 1

	def fillWter(self):
		self.__water = self.__maxWater

	def comsumeMeat(self):
		if not self.__inventory.decline("smoked_meat", 1):
			self.die()

	def getInventory(self):
		return self.__inventory

	def getHealth(self):
		return self.__health

	def getMaxHealth(self):
		return self.__maxHealth

	def getPos(self):
		return (self.__pos[0], self.__pos[1])

	def moveX(self, dis):
		if self.__pos[0] + dis > 58 or self.__pos[0] + dis < 0:
			return
		self.__pos[0] += dis
		self.map.step((self.__pos[0], self.__pos[1]))

	def moveY(self, dis):
		if self.__pos[1] + dis > 58 or self.__pos[1] + dis < 0:
			return
		self.__pos[1] += dis
		self.map.step((self.__pos[0], self.__pos[1]))

	def heal(self, count):
		if self.__health + count > self.__maxHealth:
			self.__health = self.__maxHealth
		else:
			self.__health += count

	def damage(self, count):
		if self.__health - count <= 0:
			self.__health = 0
			self.die()
		else:
			self.__health -= count

class Event:
	def __init__(self, name: str):
		self.name = name

	def trigger(self, world) -> bool:
		return True

class MakeFire(Event):
	def __init__(self):
		super().__init__("make_fire")

	def trigger(self, world):
		if world.addItem("wood", -5):
			world.addHouseWarmth(2)
			world.addLoggerMessage("make_fire.success")
			world.lightFire()
			return True
		else:
			world.addLoggerMessage("make_fire.fail")
			return False

class AddFuel(Event):
	def __init__(self):
		super().__init__("add_fuel")

	def trigger(self, world):
		if world.addItem("wood", -1):
			world.addHouseWarmth(1)
			world.addLoggerMessage("add_fuel.success")
			return True
		else:
			world.addLoggerMessage("add_fuel.fail")
			return False

class CollectWood(Event):
	def __init__(self):
		super().__init__("collect_wood")

	def trigger(self, world):
		if world.hasBuilding("cart"):
			world.addItem("wood", 50)
		else:
			world.addItem("wood", 10)
		world.addLoggerMessage("collect_wood")
		return True

class Construct(Event):
	def __init__(self, name, itemStackList):
		super().__init__("construct." + name)
		self.itemStackList = itemStackList
		self.result = name

	def trigger(self, world):
		if not world.isHouseWarm():
			world.addLoggerMessage("construct_fail.cold")
			return False
		i = world.removeItemAll(self.itemStackList)
		if i < 0:
			world.addBuilding(self.result, 1)
			return True
		else:
			world.addLoggerMessage("construct_fail", self.itemStackList[i].getKey())
			return False

class ConstructCart(Construct):
	def __init__(self):
		super().__init__("cart", [ItemStack("wood", 40)])

class ConstructTrap(Event):
	def __init__(self):
		super().__init__("construct.trap")

	def trigger(self, world):
		if not world.isHouseWarm():
			world.addLoggerMessage("construct_fail.cold")
			return False
		if world.addItem("wood", -10 * (world.getBuildingCount("trap") + 1)):
			world.addBuilding("trap", 1)
			world.triggerPropertyOn("can_check_traps")
			if world.getBuildingCount("trap") < 10:
				world.addLoggerMessage("construct.trap.success")
			else:
				world.addLoggerMessage("construct.trap.success_max")
			return True
		else:
			world.addLoggerMessage("construct.trap.fail")
			return False

class ConstructHouse(Event):
	def __init__(self):
		super().__init__("construct.house")

	def trigger(self, world):
		if not world.isHouseWarm():
			world.addLoggerMessage("construct_fail.cold")
			return False
		if world.addItem("wood", -50 * (world.getBuildingCount("house") + 2)):
			world.addBuilding("house", 1)
			world.expandPopulation(4)
			world.addLoggerMessage("construct.house.success")
			return True
		else:
			world.addLoggerMessage("construct.house.fail")
			return False

class CheckTraps(Event):
	def __init__(self):
		super().__init__("check_traps")

	def trigger(self, world):
		trapCount = world.getBuildingCount("trap")
		baitCount = world.getItemCount("bait")
		s = set()
		if baitCount > trapCount:
			baitCount = trapCount
		if baitCount > 0:
			world.addItem("bait", -baitCount)

		world.addItem("fur", int(trapCount / 2) + int(random.random() * 3) + 1)
		s.add("fur")
		if trapCount > 2:
			world.addItem("flesh", int(trapCount / 2) + int(random.random() * 2))
			it = int(trapCount / 3) + int(random.random() * 2) - 1
			if it > 0:
				s.add("flesh")
			world.addItem("fabric", int(trapCount / 3) + int(random.random() * 5))
		if trapCount > 4:
			if random.random() > 0.6:
				world.addItem("tooth", 2)
			else:
				world.addItem("tooth", 1)
			s.add("tooth")
			if random.random() > 0.5:
				world.addItem("scale", 1)
				s.add("scale")
		if trapCount > 7:
			world.addItem("tooth", 1)
			world.addItem("scale", 1)
			s.add("scale")
			if random.random() > 0.7:
				world.addItem("amulet", 1)
				s.add("amulet")
		tmp = random.random() * baitCount
		if baitCount > 0:
			world.addItem("fur", int(tmp) + 1)
		if baitCount > 3:
			world.addItem("tooth", int(tmp / 2) + 1)
			world.addItem("scale", int(tmp / 2) + 1)
			s.add("tooth")
			s.add("scale")
		if baitCount > 6:
			world.addItem("tooth", int(tmp / 2) + 1)
			world.addItem("scale", int(tmp / 2) + 1)
		if trapCount < 4:
			tmp = 0
		elif trapCount < 8:
			tmp = 1
		else:
			tmp = 2
		l = list(s)
		string = world.getLangValue("item." + l[0])
		for i in range(1, len(l)):
			string += "," + world.getLangValue("item." + l[i])
		if baitCount > 0:
			world.addLoggerMessage("check_traps.baited", string, raw = False)
		else:
			world.addLoggerMessage("check_traps.common", string, raw = False)
		return True

class SmallGroupCome(Event):
	def __init__(self):
		super().__init__("small_group_come")

	def trigger(self, world):
		world.addPopulation(5 + int(random.random() * 2))
		world.addLoggerMessage("small_group_come")
		return True

class FamilyCome(Event):
	def __init__(self):
		super().__init__("family_come")

	def trigger(self, world):
		world.addPopulation(2 + int(random.random() * 2))
		world.addLoggerMessage("family_come")
		return True

class OneCome(Event):
	def __init__(self):
		super().__init__("one_come")

	def trigger(self, world):
		world.addPopulation(1)
		world.addLoggerMessage("one_come")
		return True

class ConstructHunterHouse(Construct):
	def __init__(self):
		super().__init__("hunter_house", [ItemStack("wood", 200), ItemStack("fur", 30), ItemStack("flesh", 20)])

	def trigger(self, world):
		if super().trigger(world):
			world.newCareer("hunter")
			world.newCareer("trapper")
			return True
		return False

class ConstructTradingPost(Construct):
	def __init__(self):
		super().__init__("trading_post", [ItemStack("wood", 400), ItemStack("fur", 80)])

	def trigger(self, world):
		if super().trigger(world):
			world.triggerPropertyOn("can_trade")
			return True
		return False

class Trade(Event):
	def __init__(self, name, itemStackList):
		super().__init__("trade." + name)
		self.itemStackList = itemStackList
		self.result = name

	def trigger(self, world):
		i = world.removeItemAll(self.itemStackList)
		if i < 0:
			world.addItem(self.result, 1)
			return True
		else:
			world.addLoggerMessage("construct_fail", self.itemStackList[i].getKey())
			return False

class TradeCompass(Trade):
	def __init__(self):
		super().__init__("compass", [ItemStack("fur", 400), ItemStack("scale", 30), ItemStack("tooth", 30)])

	def trigger(self, world):
		if super().trigger(world):
			world.triggerPropertyOn("can_explore")
			return True
		return False

class ConstructSmokehouse(Construct):
	def __init__(self):
		super().__init__("smokehouse", [ItemStack("wood", 500), ItemStack("flesh", 80)])

	def trigger(self, world):
		if super().trigger(world):
			world.newCareer("smoker")
			return True
		return False

class ConstructTannery(Construct):
	def __init__(self):
		super().__init__("tannery", [ItemStack("wood", 500), ItemStack("fur", 200)])

	def trigger(self, world):
		if super().trigger(world):
			world.newCareer("tanner")
			return True
		return False

class ConstructWorkshop(Construct):
	def __init__(self):
		super().__init__("workshop", [ItemStack("wood", 600), ItemStack("leather", 50)])

	def trigger(self, world):
		if super().trigger(world):
			world.triggerPropertyOn("can_craft")
			return True
		return False

class Craft(Event):
	def __init__(self, name, itemStackList):
		super().__init__("craft." + name)
		self.itemStackList = itemStackList
		self.result = name

	def trigger(self, world):
		i = world.removeItemAll(self.itemStackList)
		if i < 0:
			world.addLoggerMessage(self.name + ".success")
			world.addItem(self.result, 1)
			return True
		else:
			world.addLoggerMessage("construct_fail", self.itemStackList[i].getKey())
			return False

class CraftEquipment(Event):
	def __init__(self, name, itemStackList):
		super().__init__("craft_equipment." + name)
		self.itemStackList = itemStackList
		self.result = name

	def trigger(self, world):
		i = world.removeItemAll(self.itemStackList)
		if i < 0:
			world.addLoggerMessage(self.name + ".success")
			world.addEquipment(self.result)
			return True
		else:
			world.addLoggerMessage("construct_fail", self.itemStackList[i].getKey())
			return False

class MonsterAttack(Event):
	def __init__(self):
		super().__init__("monster_attack")

	def trigger(self, world):
		if world.getPopulation() > 0:
			world.addPopulation(-int(random.random() * 5) + 2)
			world.putPopUp(MONSTER_ATTACK_POP_UP)
			return True
		return False

class PopUpOk(Event):
	def __init__(self):
		super().__init__("ok")

	def trigger(self, world):
		world.removePopUp()
		return True

class TrapDestroyed(Event):
	def __init__(self):
		super().__init__("trap_destroyed")

	def trigger(self, world):
		if world.getBuildingCount("trap") > 0:
			world.declineBuilding("trap", int(random.random() * 6) + 1)
			world.putPopUp(TRAP_DESTROYED_POP_UP0)
			return True
		return False

class TrapDestroyedExplore(Event):
	def __init__(self):
		super().__init__("trap_destroyed.explore")

	def trigger(self, world):
		if world.getBuildingCount("trap") > 0:
			world.addItem("fur", int(random.random() * 10) + 100)
			world.addItem("flesh", int(random.random() * 10) + 95)
			world.addItem("tooth", int(random.random() * 4) + 3)
			world.removePopUp()
			world.putPopUp(TRAP_DESTROYED_POP_UP1)
			return True
		return False

class WoodStolen(Event):
	def __init__(self):
		super().__init__("wood_stolen")

	def trigger(self, world):
		count = world.getItemCount("wood")
		if count > 1000:
			world.addItem("wood", int(-random.random() * 10) + 105)
		elif count > 300:
			world.addItem("wood", int(-random.random() * 7) + 45)
		elif count > 100:
			world.addItem("wood", int(-random.random() * 4) + 10)
		else:
			return False
		world.putPopUp(WOOD_STOLEN_POP_UP0)
		return True

class WoodStolenCheck(Event):
	def __init__(self):
		super().__init__("wood_stolen.check")

	def trigger(self, world):
		world.addItem("scale", int(random.random() * 9) + 7)
		world.removePopUp()
		world.putPopUp(WOOD_STOLEN_POP_UP1)
		return True

class FurRequire(Event):
	def __init__(self):
		super().__init__("fur_require")

	def trigger(self, world):
		if not world.hasFurReward():
			world.putPopUp(FUR_REQUIRE_POP_UP)
			return True
		return False

class FurRequireGive(Event):
	def __init__(self, count):
		super().__init__("fur_require.give_" + str(count))
		self.count = count

	def trigger(self, world):
		world.addItem("fur", -self.count)
		world.createFurReward(self.count)
		world.removePopUp()
		return True

class FurReward(Event):
	def __init__(self):
		super().__init__("fur_reward")

	def trigger(self, world):
		world.addItem("fur", int(world.getFurRewardCount() * (random.random() / 5 + 2.9)))
		world.addLoggerMessage("fur_reward")
		return True

class Start(Event):
	def __init__(self):
		super().__init__("start")

	def trigger(self, world):
		world.startAdventure()
		return True

class EnterMap(Event):
	def __init__(self):
		super().__init__("enter_map")

	def trigger(self, world):
		world.putPopUp(WIP_POP_UP)
		return True

class ConsoleSaves(Event):
	def __init__(self):
		super().__init__("console.saves")

	def trigger(self, world):
		world.putPopUp(SAVES_POP_UP)
		return True

class SavesLoad(Event):
	def __init__(self):
		super().__init__("saves.load")

	def trigger(self, world):
		world.removePopUp()
		world.putPopUp(LOAD_POP_UP)
		return True

class SavesSave(Event):
	def __init__(self):
		super().__init__("saves.save")

	def trigger(self, world):
		world.removePopUp()
		world.putPopUp(SAVE_POP_UP)
		return True

class ConsoleRestart(Event):
	def __init__(self):
		super().__init__("console.restart")

	def trigger(self, world):
		world.putPopUp(RESTART_POP_UP)
		return True

class Restart(Event):
	def __init__(self):
		super().__init__("restart")

	def trigger(self, world):
		world.hangRestart = True
		world.removePopUp()
		return True

class ConsoleLanguage(Event):
	def __init__(self):
		super().__init__("console.language")

	def trigger(self, world):
		world.putPopUp(LANGUAGE_POP_UP)
		return True

MAKE_FIRE_BUTTON = button.SimpleButton("make_fire", (350, 100), [ItemStack("wood", 5)])
ADD_FUEL_BUTTON = button.CoolableButton("add_fuel", (350, 100), 5.0, [ItemStack("wood", 1)])
COLLECT_WOOD_BUTTON = button.CoolableButton("collect_wood", (350, 100), 35.0)
CONSTRUCT_CART_BUTTON = button.Construct("cart", (350, 250), [ItemStack("wood", 40)])
CONSTRUCT_TRAP_BUTTON = button.ConstructTrap((350, 310))
CONSTRUCT_HOUSE_BUTTON = button.ConstructHouse((350, 370))
CHECK_TRAPS_BUTTON = button.CoolableButton("check_traps", (350, 160), 40.0)
CONSTRUCT_HUNTER_HOUSE_BUTTON = button.Construct("hunter_house", (350, 430), [ItemStack("wood", 200), ItemStack("fur", 30), ItemStack("flesh", 20)])
CONSTRUCT_TRADING_POST_BUTTON = button.Construct("trading_post", (350, 490), [ItemStack("wood", 400), ItemStack("fur", 80)])
TRADE_SCALE_BUTTON = button.Trade("scale", (650, 250), [ItemStack("fur", 150)])
TRADE_TOOTH_BUTTON = button.Trade("tooth", (650, 310), [ItemStack("fur", 200)])
TRADE_COMPASS_BUTTON = button.TradeCompass((650, 370))
CONSTRUCT_SMOKEHOUSE_BUTTON = button.Construct("smokehouse", (350, 550), [ItemStack("wood", 500), ItemStack("flesh", 80)])
CONSTRUCT_TANNERY_BUTTON = button.Construct("tannery", (350, 610), [ItemStack("wood", 500), ItemStack("fur", 200)])
CONSTRUCT_WORKSHOP_BUTTON = button.Construct("workshop", (350, 670), [ItemStack("wood", 600), ItemStack("leather", 50)])
CRAFT_TORCH_BUTTON = button.Craft("torch", (500, 250), [ItemStack("wood", 50), ItemStack("fabric", 10)])
CRAFT_BACKPACK_BUTTON = button.CraftEquipment("backpack", (500, 310), [ItemStack("leather", 100)])
CRAFT_KETTLE_BUTTON = button.CraftEquipment("kettle", (500, 370), [ItemStack("leather", 80)])
CRAFT_SPEAR_BUTTON = button.Craft("spear", (500, 430), [ItemStack("wood", 100), ItemStack("fabric", 10)])
CRAFT_LEATHER_ARMOR_BUTTON = button.CraftEquipment("leather_armor", (500, 490), [ItemStack("leather", 300), ItemStack("fabric", 40)])
START_BUTTON = button.Start((660, 110))

MONSTER_ATTACK_POP_UP = info.PopUp(["monster_attack0", "monster_attack1"], [button.Ok()])
TRAP_DESTROYED_POP_UP0 = info.PopUp(["trap_destroyed"], [button.PopUpButton("trap_destroyed.explore"), button.Ok("trap_destroyed.ignore")])
TRAP_DESTROYED_POP_UP1 = info.PopUp(["trap_destroyed.discover0", "trap_destroyed.discover1"], [button.Ok()])
WOOD_STOLEN_POP_UP0 = info.PopUp(["wood_stolen"], [button.PopUpButton("wood_stolen.check"), button.Ok("wood_stolen.ignore")])
WOOD_STOLEN_POP_UP1 = info.PopUp(["wood_stolen.check0", "wood_stolen.check1"], [button.Ok()])
FUR_REQUIRE_POP_UP = info.PopUp(["fur_require0", "fur_require1"], [button.GiveFur(200), button.GiveFur(500), button.GiveFur(1000), button.Ok("fur_require.drive_away")])
WIP_POP_UP = info.PopUp(["wip0", "wip1"], [button.Ok()])
SAVES_POP_UP = info.PopUp(["saves0", "saves1"], [button.PopUpButton("saves.load"), button.PopUpButton("saves.save"), button.Cancel()])
LOAD_POP_UP = info.SRBPopUp(["load"], [button.SaveButton("load", 0), button.SaveButton("load", 1), button.SaveButton("load", 2), button.SaveButton("load", 3), button.SaveButton("load", 4), button.Cancel()])
SAVE_POP_UP = info.SRBPopUp(["save"], [button.SaveButton("save", 0), button.SaveButton("save", 1), button.SaveButton("save", 2), button.SaveButton("save", 3), button.SaveButton("save", 4), button.Cancel()])
RESTART_POP_UP = info.PopUp(["restart0", "restart1"], [button.PopUpButton("restart"), button.Cancel()])
names = getAvailableLanguages()
l0 = []
for name in names:
	l0.append(button.LanguageButton(name))
l0.append(button.Cancel())
LANGUAGE_POP_UP = info.SRBPopUp(["language"], l0)