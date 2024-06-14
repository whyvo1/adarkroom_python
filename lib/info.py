'''
This program is based on MPL-2.0 license.
This program is open-source at https://github.com/whyvo1/adarkroom_python
'''

import pygame

unifont = pygame.font.Font("lib/unifont-15.1.05.otf", 20)
unifontSmall = pygame.font.Font("lib/unifont-15.1.05.otf", 18)

whiteSurface = pygame.Surface((12, 12))
whiteSurface.fill((255, 255, 255))
addButton0 = whiteSurface.copy()
pygame.draw.line(addButton0, (0, 0, 0), (0, 5), (10, 5), width = 2)
pygame.draw.line(addButton0, (0, 0, 0), (5, 0), (5, 10), width = 2)
addButton0Dis = whiteSurface.copy()
pygame.draw.line(addButton0Dis, (120, 120, 120), (0, 5), (10, 5), width = 2)
pygame.draw.line(addButton0Dis, (120, 120, 120), (5, 0), (5, 10), width = 2)
addButton1 = whiteSurface.copy()
pygame.draw.line(addButton1, (0, 0, 0), (0, 5), (10, 5), width = 3)
pygame.draw.line(addButton1, (0, 0, 0), (5, 0), (5, 10), width = 3)
addButton1Dis = whiteSurface.copy()
pygame.draw.line(addButton1Dis, (120, 120, 120), (0, 5), (10, 5), width = 3)
pygame.draw.line(addButton1Dis, (120, 120, 120), (5, 0), (5, 10), width = 3)
minusButton0 = whiteSurface.copy()
pygame.draw.line(minusButton0, (0, 0, 0), (0, 5), (10, 5), width = 2)
minusButton0Dis = whiteSurface.copy()
pygame.draw.line(minusButton0Dis, (120, 120, 120), (0, 5), (10, 5), width = 2)
minusButton1 = whiteSurface.copy()
pygame.draw.line(minusButton1, (0, 0, 0), (0, 5), (10, 5), width = 3)
minusButton1Dis = whiteSurface.copy()
pygame.draw.line(minusButton1Dis, (120, 120, 120), (0, 5), (10, 5), width = 3)

WEIGHT_0 = ["bullet", "amulet"]
WEIGHT_2 = ["spear"]
WEIGHT_3 = ["iron_sword", "steel_sword"]
WEIGHT_5 = ["rifle", "laser_rifle"]
def getWeight(item):
	if item in WEIGHT_0:
		return 0
	if item in WEIGHT_2:
		return 2
	if item in WEIGHT_3:
		return 3
	if item in WEIGHT_5:
		return 5
	return 1

def createTextbox(string, width: int, lineDis: int):
	texts = []
	x, y = 0, 0
	for char in string:
		t = unifont.render(char, True, (0, 0, 0))
		if x + t.get_width() > width:
			y += lineDis
			x = 0
		texts.append((t, (x, y)))
		x += t.get_width()
	text = pygame.Surface((width, y + lineDis))
	text.fill((255, 255, 255))
	text.blits(texts)
	return text

def getConstructText(world):
	return unifont.render(world.getLangValue("sign.construct"), True, (0, 0, 0))

def getTradeText(world):
	return unifont.render(world.getLangValue("sign.trade"), True, (0, 0, 0))

def getCraftText(world):
	return unifont.render(world.getLangValue("sign.craft"), True, (0, 0, 0))

class LoggerRow:
	def __init__(self, width, height, distance):
		self.massages = []
		self.totalHeight = 0
		self.width = width
		self.height = height
		self.distance = distance

	def addMessage(self, string):
		message0 = createTextbox(string, self.width, 20)
		tmp = message0.get_height() + self.distance
		i = len(self.massages) - 1
		while i >= 0:
			tmp += self.massages[i].get_height() + self.distance
			if tmp > self.height:
				del self.massages[0 : i]
				break
			if tmp > self.height * 0.5:
				self.massages[i].set_alpha(int((1 - (tmp - self.height * 0.5) / (self.height * 0.5)) * 255))
			i -= 1
		self.massages.append(message0)

	def render(self, screen, pos: tuple):
		i = len(self.massages) - 1
		dy = 0
		while i >= 0:
			screen.blit(self.massages[i], (pos[0], pos[1] + dy))
			dy += self.massages[i].get_height() + self.distance
			i -= 1

class ItemTab:
	def __init__(self, name, width, lineDis, itemStacks):
		self.name = name
		self.offName = ""
		self.lineDis = lineDis
		self.__itemStackList = itemStacks
		self.width = width

	def getHeight(self):
		return len(self.__itemStackList) * self.lineDis + 19

	def render(self, screen, world, pos):
		height = self.getHeight()
		
		nameSurface = unifont.render(world.getLangValue("itemTab." + self.name), True, (0, 0, 0), (255, 255, 255))
		bl = False
		if self.offName != "":
			offNameText = unifont.render(self.offName, True, (0, 0, 0), (255, 255, 255))
			bl = True

		surface = pygame.Surface((self.width, height))
		surface.fill((255, 255, 255))
		dy = 0
		workResult = world.getWorkResults()
		for itemStack in self.__itemStackList:
			extra = ""
			for itemStack0 in workResult:
				if itemStack.item == itemStack0.item:
					extra = "("
					if itemStack0.count >= 0:
						extra += "+"
					extra += str(itemStack0.count) + ")"
					break
			surface.blit(unifont.render(world.getLangValue(itemStack.getKey()) + extra, True, (0, 0, 0)), (0, dy))
			countText = unifont.render(str(itemStack.count), True, (0, 0, 0))
			surface.blit(countText, (self.width - countText.get_width() - 40, dy))
			dy += self.lineDis

		screen.blit(surface, (pos[0] + 20, pos[1] + 26))
		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(pos[0] + 10, pos[1] + 10, self.width - 20, height), width = 1)
		screen.blit(nameSurface, (pos[0] + 30, pos[1]))
		if bl:
			screen.blit(offNameText, (pos[0] + self.width - offNameText.get_width() - 30, pos[1]))

class HoveringBar:
	def __init__(self, width, itemStacks, showSigns = False, extra = ""):
		self.width = width
		self.itemStacks = itemStacks
		self.showSigns = showSigns
		self.extra = extra

	def render(self, pos: tuple, screen, world):
		height = len(self.itemStacks) * 26 + 6

		surface = pygame.Surface((self.width, height))
		surface.fill((255, 255, 255))
		dy = 4
		for itemStack in self.itemStacks:
			surface.blit(unifont.render(world.getLangValue(itemStack.getKey()), True, (0, 0, 0)), (4, dy))
			sign = ""
			if self.showSigns and itemStack.count > 0:
				sign = "+"
			countText = unifont.render(sign + str(itemStack.count) + self.extra, True, (0, 0, 0))
			surface.blit(countText, (self.width - countText.get_width() - 4, dy))
			dy += 26

		screen.blit(surface, (pos[0], pos[1]))
		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(pos[0], pos[1], self.width, len(self.itemStacks) * 26 + 6), width = 2)

class ColumnBar:
	def __init__(self):
		self.columnButtons = []

	def addButton(self, columnButton):
		self.columnButtons.append(columnButton)

	def render(self, screen):
		for button in self.columnButtons:
			button.render(screen)

class CareerActionBar:
	def __init__(self, lineDis, village, pos):
		self.lineDis = lineDis
		self.village = village
		self.pos = pos

	def render(self, screen, world):
		dy = 0
		bl = True
		lc = self.village.careers[0].count
		careers = self.village.getUnlockedCareers()
		for career in careers:
			screen.blit(unifont.render(world.getLangValue("career." + career.name), True, (0, 0, 0)), (self.pos[0], self.pos[1] + dy))
			countText = unifont.render(str(career.count), True, (0, 0, 0))
			screen.blit(countText, (self.pos[0] + 137 - (countText.get_width() // 2), self.pos[1] + dy))
			if bl:
				bl = False
				dy += self.lineDis
				continue

			if career.count > 0:
				screen.blit(minusButton0, (self.pos[0] + 102, self.pos[1] + dy + 5))
				screen.blit(minusButton1 if career.count > 9 else minusButton1Dis, (self.pos[0] + 84, self.pos[1] + dy + 5))
			else:
				screen.blit(minusButton0Dis, (self.pos[0] + 102, self.pos[1] + dy + 5))
				screen.blit(minusButton1Dis, (self.pos[0] + 84, self.pos[1] + dy + 5))
			if lc > 0:
				screen.blit(addButton0, (self.pos[0] + 160, self.pos[1] + dy + 5))
				screen.blit(addButton1 if lc > 9 else addButton1Dis, (self.pos[0] + 178, self.pos[1] + dy + 5))
			else:
				screen.blit(addButton0Dis, (self.pos[0] + 160, self.pos[1] + dy + 5))
				screen.blit(addButton1Dis, (self.pos[0] + 178, self.pos[1] + dy + 5))
			dy += self.lineDis

	def handleClick(self, world, mousePos):
		i = (mousePos[1] - self.pos[1]) // self.lineDis
		x0 = mousePos[0] - self.pos[0]
		count = 0
		if x0 >= 84 and x0 < 96:
			count = -10
		elif x0 >= 102 and x0 < 114:
			count = -1
		elif x0 >= 160 and x0 < 172:
			count = 1
		elif x0 >= 178 and x0 < 190:
			count = 10
		
		if i > 0 and i < self.village.getUnlockedCareerCount() and count != 0:
			self.village.addCareerIn(i, count)

	def handleHover(self, world, mousePos, screen):
		i = (mousePos[1] - self.pos[1]) // self.lineDis
		x0 = mousePos[0] - self.pos[0]
		careers = self.village.getUnlockedCareers()

		if i >= 0 and i < self.village.getUnlockedCareerCount() and x0 >= 0 and x0 < 190:
			HoveringBar(190, careers[i].workResult(), True, "/10s").render((self.pos[0], self.pos[1] + (i + 1) * self.lineDis - 12), screen, world)
			
class PopUp:
	def __init__(self, desc = [], buttons = []):
		self.width = 400
		self.desc = [] if len(desc) == 0 else desc
		self.buttons = [] if len(buttons) == 0 else buttons

	def setDesc(self, desc):
		self.desc = desc

	def addButton(self, button):
		button.popUp = self
		self.buttons.append(button)

	def removeButtonIn(self, index):
		del self.buttons[index]

	def removeButton(self, name, order = 0):
		i, j = 0, 0
		while i < len(self.buttons):
			if self.buttons[i].name == name:
				if j == order:
					del self.buttons[i]
					return
				j += 1
			i += 1

	def insertButton(self, index, button):
		button.popUp = self
		self.buttons.insert(index, button)

	def render(self, screen, world, mousePos):
		posX = screen.get_width() // 2 - self.width // 2
		descTexts = []
		dy = 0
		for d in self.desc:
			descText = createTextbox(world.getLangValue("pop_up." + d), self.width - 32, 24)
			descTexts.append((descText, (0, dy)))
			dy += descText.get_height() + 16
		text = pygame.Surface((self.width - 32, dy))
		text.fill((255, 255, 255))
		text.blits(descTexts)
		descHeight = dy
		height = 80 + descHeight + (len(self.buttons) + 1) // 2 * 50
		posY = screen.get_height() // 2 - int(height * 1.8) // 2
		window = pygame.Surface((self.width, height))
		window.fill((255, 255, 255))
		rect = window.get_rect()
		rect.topleft = (posX, posY)

		shade = pygame.Surface(screen.get_size())
		shade.fill((0, 0, 0))
		shade.set_alpha(100)
		screen.blit(shade, (0, 0))
		screen.blit(window, (posX, posY))
		pygame.draw.rect(screen, (0, 0, 0), rect, width = 4)
		screen.blit(text, (posX + 20, posY + 20))
		i = 0
		for button in self.buttons:
			button.setPos((posX + (50 if i % 2 == 0 else 220), posY + descHeight + 50 + i // 2 * 50))
			button.setHovered(button.rect.collidepoint(mousePos))
			button.render(screen, world)
			i += 1

	def handleClick(self, world, mousePos):
		for button in self.buttons:
			if button.rect.collidepoint(mousePos):
				button.onClicked(world)
				break

	def renderButtonTip(self, world, screen):
		for button in self.buttons:
			if button.isHovered():
				button.renderTip(world, screen)

class AdventurePreparationTab:
	CAN_PREPARE = ["smoked_meat", "medicine", "torch", "amulet", "spear", "iron_sword", "steel_sword", "rifle", "bullet"]

	def __init__(self, pos, width, lineDis, inventory):
		self.pos = pos
		self.width = width
		self.lineDis = lineDis
		self.inventory = inventory

	def getHeight(self, world):
		height = self.lineDis * 3
		for item in AdventurePreparationTab.CAN_PREPARE:
			if world.hasItem(item):
				height += self.lineDis
		return height

	def getRenderedItems(self, world):
		items = []
		for item in AdventurePreparationTab.CAN_PREPARE:
			if world.hasItem(item):
				items.append(item)
		return items

	def render(self, world, screen):
		height = self.getHeight(world)
		
		nameSurface = unifont.render(world.getLangValue("ap_tab.title"), True, (0, 0, 0), (255, 255, 255))
		offNameText = unifont.render(world.getLangValue("ap_tab.space") + str(self.inventory.occupied) + "/" + str(world.getStorageVolumn()), True, (0, 0, 0), (255, 255, 255))

		armorText = pygame.Surface((self.width, 36))
		armorText.fill((255, 255, 255))
		armorText.blit(unifont.render(world.getLangValue("ap_tab.armor"), True, (0, 0, 0)), (0, 0))
		armorLevelText = unifont.render(world.getLangValue("armor." + world.getArmorEquipment()), True, (0, 0, 0))
		armorText.blit(armorLevelText, (self.width - armorLevelText.get_width() - 40, 0))
		
		waterText = pygame.Surface((self.width, 36))
		waterText.fill((255, 255, 255))
		waterText.blit(unifont.render(world.getLangValue("ap_tab.water"), True, (0, 0, 0)), (0, 0))
		waterVolumnText = unifont.render(str(world.getVesselVolumn()), True, (0, 0, 0))
		waterText.blit(waterVolumnText, (self.width - waterVolumnText.get_width() - 40, 0))
		
		surface = pygame.Surface((self.width, height - self.lineDis * 3))
		surface.fill((255, 255, 255))
		dy = 0
		for item in self.getRenderedItems(world):
			c0 = self.inventory.getCount(item)
			c1 = world.getItemCount(item) - c0
			v = world.getStorageVolumn() - self.inventory.occupied
			surface.blit(unifont.render(world.getLangValue("item." + item), True, (0, 0, 0)), (0, dy))
			countText = unifont.render(str(c0), True, (0, 0, 0))
			surface.blit(countText, (self.width - int(countText.get_width() / 2) - 100, dy))
			if c0 >= 1:
				surface.blit(minusButton0, (self.width - 135, dy + 5))
				surface.blit(minusButton1 if c0 >= 10 else minusButton1Dis, (self.width - 153, dy + 5))
			else:
				surface.blit(minusButton1Dis, (self.width - 153, dy + 5))
				surface.blit(minusButton0Dis, (self.width - 135, dy + 5))

			if c1 >= 1 and v >= 1:
				surface.blit(addButton0, (self.width - 77, dy + 5))
				surface.blit(addButton1 if c1 >= 10 and v >= 10 else addButton1Dis, (self.width - 59, dy + 5))
			else:
				surface.blit(addButton0Dis, (self.width - 77, dy + 5))
				surface.blit(addButton1Dis, (self.width - 59, dy + 5))

			dy += self.lineDis

		screen.blit(armorText, (self.pos[0] + 20, self.pos[1] + self.lineDis))
		screen.blit(waterText, (self.pos[0] + 20, self.pos[1] + self.lineDis * 2))
		screen.blit(surface, (self.pos[0] + 20, self.pos[1] + self.lineDis * 3))
		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.pos[0] + 10, self.pos[1] + 10, self.width - 20, height), width = 1)
		screen.blit(nameSurface, (self.pos[0] + 30, self.pos[1]))
		screen.blit(offNameText, (self.pos[0] + self.width - offNameText.get_width() - 30, self.pos[1]))

	def handleHover(self, world, mousePos, screen):
		i = (mousePos[1] - self.pos[1] + 5) // self.lineDis - 3
		x0 = mousePos[0] - self.pos[0]
		items = self.getRenderedItems(world)

		width = 130
		if i >= 0 and i < len(items) and x0 >= 0 and x0 < self.width:
			surface = pygame.Surface((width, 32))
			surface.fill((255, 255, 255))
			j = 0
			for item in items:
				if i == j:
					surface.blit(unifont.render(world.getLangValue("ap_tab.weight"), True, (0, 0, 0)), (4, 4))
					countText = unifont.render(str(getWeight(item)), True, (0, 0, 0))
					surface.blit(countText, (width - countText.get_width() - 4, 4))
					break
				j += 1

			screen.blit(surface, (self.pos[0] + 16, self.pos[1] + self.lineDis * (i + 4) - 10))
			pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.pos[0] + 16, self.pos[1] + self.lineDis * (i + 4) - 10, width, 32), width = 2)

	def handleClick(self, world, mousePos):
		i = (mousePos[1] - self.pos[1]) // self.lineDis - 3
		x0 = mousePos[0] - self.pos[0] - 20
		count = 0
		if x0 >= self.width - 153 and x0 < self.width - 141:
			count = -10
		elif x0 >= self.width - 135 and x0 < self.width - 123:
			count = -1
		elif x0 >= self.width - 77 and x0 < self.width - 65:
			count = 1
		elif x0 >= self.width - 59 and x0 < self.width - 47:
			count = 10
		items = self.getRenderedItems(world)

		if i >= 0 and i < len(items) and count != 0:
			if count > 0:
				if world.getItemCount(items[i]) - self.inventory.getCount(items[i]) >= count and world.getStorageVolumn() - self.inventory.occupied >= count:
					self.inventory.increase(items[i], count)
				return
			self.inventory.decline(items[i], -count)

class AdventureItemTab:
	def __init__(self, adventure, pos):
		self.adventure = adventure
		self.pos = pos

	def render(self, screen, world):
		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.pos[0], self.pos[1], 596, 145), width = 2)

		pos0 = (self.pos[0] + 6, self.pos[1] + 6)
		surface = pygame.Surface((584, 133))
		surface.fill((255, 255, 255))
		waterText = unifont.render(world.getLangValue("item.water") + ":" + str(self.adventure.getWater()), True, (0, 0, 0))
		wtw = waterText.get_width()
		pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, wtw + 8, 28), width = 2)
		surface.blit(waterText, (4, 4))

		dx, dy = wtw + 12, 0
		for itemStack in self.adventure.getInventory().itemStacks:
			text = unifont.render(world.getLangValue(itemStack.getKey()) + ":" + str(itemStack.count), True, (0, 0, 0))
			tw = text.get_width()
			if dx + tw + 8 > 584:
				dy += 30
				dx = 0
			pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(dx, dy, tw + 8, 28), width = 2)
			surface.blit(text, (4 + dx, 4 + dy))
			dx += tw + 12

		screen.blit(surface, (pos0[0] + 2, pos0[1] + 2))

class MapSet:
	def __init__(self, adventure, pos):
		self.adventure = adventure
		self.pos = pos

	def render(self, screen, world):
		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.pos[0], self.pos[1], 596, 714), width = 2)
		surface = pygame.Surface((590, 708))
		surface.fill((255, 255, 255))
		strings = self.adventure.map.getStrings()
		i = 0
		pos0 = (self.pos[0] + 3, self.pos[1] + 3)
		while i < 59:
			j = 0
			while j < 59:
				surface.blit(unifontSmall.render("@" if self.adventure.getPos() == (j, i) else strings[i][j], True, (0, 0, 0)), (j * 10, i * 12))
				j += 1
			i += 1
		screen.blit(surface, pos0)

	def handleClick(self, mousePos):
		i = (mousePos[1] - self.pos[1] - 3) // 12
		j = (mousePos[0] - self.pos[0] - 3) // 10

		if i >= 0 and i < 59 and j >= 0 and j < 59:
			t0 = self.adventure.getPos()
			t1 = (j - t0[0], i - t0[1])
			if t1[0] == 0 and t1[1] == 0:
				return
			t1Abs = (abs(t1[0]), abs(t1[1]))
			if t1Abs[0] > t1Abs[1]:
				self.adventure.moveX(t1[0] // t1Abs[0])
			else:
				self.adventure.moveY(t1[1] // t1Abs[1])

	def handleHover(self, world, mousePos, screen):
		return

class ConsoleBar:
	def __init__(self):
		self.consoleButtons = []

	def addButton(self, button):
		self.consoleButtons.append(button)

	def render(self, screen):
		for button in self.consoleButtons:
			button.render(screen)

class SRBPopUp(PopUp):
	def render(self, screen, world, mousePos):
		posX = screen.get_width() // 2 - self.width // 2
		descTexts = []
		dy = 0
		for d in self.desc:
			descText = createTextbox(world.getLangValue("pop_up." + d), self.width - 32, 24)
			descTexts.append((descText, (0, dy)))
			dy += descText.get_height() + 16
		text = pygame.Surface((self.width - 32, dy))
		text.fill((255, 255, 255))
		text.blits(descTexts)
		height = dy + 40 + len(self.buttons) * 50
		posY = screen.get_height() // 2 - int(height * 1.8) // 2
		window = pygame.Surface((self.width, height))
		window.fill((255, 255, 255))
		rect = window.get_rect()
		rect.topleft = (posX, posY)

		shade = pygame.Surface(screen.get_size())
		shade.fill((0, 0, 0))
		shade.set_alpha(100)
		screen.blit(shade, (0, 0))
		screen.blit(window, (posX, posY))
		pygame.draw.rect(screen, (0, 0, 0), rect, width = 4)
		screen.blit(text, (posX + 20, posY + 20))
		dy = text.get_height() + 20
		for button in self.buttons:
			button.setPos((posX + 20, posY + dy))
			button.setHovered(button.rect.collidepoint(mousePos))
			button.render(screen, world)
			dy += 50

	def handleClick(self, world, mousePos):
		for button in self.buttons:
			if button.rect.collidepoint(mousePos):
				button.onClicked(world)
				break

	def renderButtonTip(self, world, screen):
		return