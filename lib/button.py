import time
import pygame
from lib import util
from lib import info

unifont = pygame.font.Font("lib/unifont-15.1.05.otf", 20)

class Button(pygame.sprite.Sprite):
	def __init__(self, name, pos, itemStacks = []):
		super().__init__()
		self.name = name
		self.rect = pygame.Rect(pos, (130, 40))
		self.lastClickedTime = 0.0
		self.hovered = False
		self.itemStacks = itemStacks
		self.cooltime = 0.0

	def setPos(self, pos):
		self.rect.topleft = pos

	def setHovered(self, hovered: bool):
		self.hovered = hovered

	def isHovered(self):
		return self.hovered

	def getTextPos(self, text):
		return (self.rect.centerx - text.get_width() / 2, self.rect.centery - text.get_height() / 2)

	def render(self, screen, world):
		return

	def renderTip(self, screen, world):
		if not self.isAvailable(world) or len(self.itemStacks) == 0:
			return
		info.HoveringBar(130, self.itemStacks).render((self.rect.left, self.rect.bottom), screen, world)

	def onClicked(self, world):
		return

	def getCoolProgress(self, world) -> float:
		if self.isAvailable(world):
			return 0.0
		return 1 - (time.time() - self.lastClickedTime) / self.cooltime

	def isAvailable(self, world):
		return time.time() - self.lastClickedTime >= self.cooltime

	def setOnCool(self):
		self.lastClickedTime = time.time()

	def getKey(self) -> str:
		return "button." + self.name

class SimpleButton(Button):
	def render(self, screen, world):
		string = world.getLangValue(self.getKey())
		if self.isAvailable(world):
			text = unifont.render(string, True, (0, 0, 0))
		else:
			text = unifont.render(string, True, (130, 130, 130))
		if self.isAvailable(world):
			if self.hovered:
				pygame.draw.rect(screen, (210, 210, 210), self.rect)
			pygame.draw.rect(screen, (0, 0, 0), self.rect, width = 1)
		else:
			pygame.draw.rect(screen, (130, 130, 130), self.rect, width = 1)
		screen.blit(text, self.getTextPos(text))

	def isAvailable(self, world):
		return True

	def onClicked(self, world):
		if self.isAvailable(world):
			world.triggerEvent(self.name)

class CoolableButton(Button):
	def __init__(self, name, pos, cooltime, itemStacks = []):
		super().__init__(name, pos, itemStacks)
		self.cooltime = cooltime

	def render(self, screen, world):
		string = world.getLangValue(self.getKey())
		if self.isAvailable(world):
			text = unifont.render(string, True, (0, 0, 0))
		else:
			text = unifont.render(string, True, (130, 130, 130))
		if self.isAvailable(world):
			if self.hovered:
				pygame.draw.rect(screen, (210, 210, 210), self.rect)
			pygame.draw.rect(screen, (0, 0, 0), self.rect, width = 1)
		else:
			pygame.draw.rect(screen, (130, 130, 130), self.rect, width = 1)
			if self.getCoolProgress(world) > 0.0:
				pygame.draw.rect(screen, (180, 180, 180), pygame.Rect(self.rect.left, self.rect.top, int(self.rect.width * self.getCoolProgress(world)), self.rect.height))
		screen.blit(text, self.getTextPos(text))

	def onClicked(self, world):
		if self.isAvailable(world):
			if world.triggerEvent(self.name):
				self.setOnCool()

class Construct(SimpleButton):
	def __init__(self, name, pos, itemStacks):
		super().__init__("construct." + name, pos, itemStacks)
		self.id = name

	def isAvailable(self, world):
		return not world.hasBuilding(self.id)

class ConstructTrap(Construct):
	def __init__(self, pos):
		super().__init__("trap", pos, [])

	def isAvailable(self, world):
		return not world.hasBuilding("trap", 10)

	def renderTip(self, screen, world):
		if not self.isAvailable(world):
			return
		itemStacks = [util.ItemStack("wood", 10 * (world.getBuildingCount("trap") + 1))]
		info.HoveringBar(130, itemStacks).render((self.rect.left, self.rect.bottom), screen, world)

class ConstructHouse(Construct):
	def __init__(self, pos):
		super().__init__("house", pos, [])

	def isAvailable(self, world):
		return not world.hasBuilding("house", 20)

	def renderTip(self, screen, world):
		if not self.isAvailable(world):
			return
		itemStacks = [util.ItemStack("wood", 50 * (world.getBuildingCount("house") + 2))]
		info.HoveringBar(130, itemStacks).render((self.rect.left, self.rect.bottom), screen, world)

class Trade(SimpleButton):
	def __init__(self, name, pos, itemStacks):
		super().__init__("trade." + name, pos, itemStacks)
		self.id = name

class TradeCompass(Trade):
	def __init__(self, pos):
		super().__init__("compass", pos, [util.ItemStack("fur", 400), util.ItemStack("scale", 30), util.ItemStack("tooth", 30)])

	def isAvailable(self, world):
		return not world.hasItem("compass")

class Craft(SimpleButton):
	def __init__(self, name, pos, itemStacks):
		super().__init__("craft." + name, pos, itemStacks)

class CraftEquipment(Craft):
	def __init__(self, name, pos, itemStacks):
		Button.__init__(self, "craft_equipment." + name, pos, itemStacks)
		self.id = name

	def isAvailable(self, world):
		return not world.hasEquipment(self.id)

class ColumnButton(pygame.sprite.Sprite):
	def __init__(self, name, pos, world):
		super().__init__()
		self.name = name
		self.image = unifont.render(world.getLangValue("column." + self.name), True, (0, 0, 0))
		self.rect = self.image.get_rect()
		self.rect.topleft = pos
		self.on = False
		self.hovered = False

	def setOn(self, on: bool):
		self.on = on

	def setHovered(self, hovered: bool):
		self.hovered = hovered

	def render(self, screen):
		screen.blit(self.image, self.rect.topleft)
		if self.on:
			pygame.draw.line(screen, (0, 0, 0), (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.bottom), width = 2)
		elif self.hovered:
			pygame.draw.line(screen, (0, 0, 0), (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.bottom), width = 1)

	def onClicked(self, world):
		if self.on:
			return
		name = self.name
		i = 0
		for c in name:
			if c == ".":
				name = name[:i]
				break
			i += 1
		world.changeColume(name)

class PopUpButton(SimpleButton):
	def __init__(self, name, itemStacks = []):
		super().__init__(name, (0, 0), itemStacks)

	def onClicked(self, world):
		if self.isAvailable(world):
			world.triggerPopUpEvent(self.name)

class CoolablePopUpButton(CoolableButton):
	def __init__(self, name, cooltime, itemStacks = []):
		super().__init__(name, (0, 0), cooltime, itemStacks)

	def onClicked(self, world):
		if self.isAvailable(world):
			if world.triggerPopUpEvent(self.name):
				self.setOnCool()

class Ok(PopUpButton):
	def __init__(self, name = "ok"):
		super().__init__(name, [])

	def onClicked(self, world):
		if self.isAvailable(world):
			world.triggerPopUpEvent("ok")

class Cancel(Ok):
	def __init__(self):
		super().__init__("cancel")

class GiveFur(PopUpButton):
	def __init__(self, count):
		super().__init__("give_fur." + str(count), [])
		self.count = count

	def onClicked(self, world):
		if self.isAvailable(world):
			world.triggerPopUpEvent("fur_require.give_" + str(self.count))

	def isAvailable(self, world):
		return world.hasItem("fur", self.count)

class Start(SimpleButton):
	def __init__(self, pos):
		super().__init__("start", pos, [])

	def isAvailable(self, world):
		return world.canStartAdventure()

class ConsoleButton:
	def __init__(self, name, world):
		self.name = name
		self.image = unifont.render(world.getLangValue("console." + self.name), True, (88, 88, 88))
		self.rect = self.image.get_rect()
		self.hovered = False

	def setPos(self, pos):
		self.rect.topleft = pos

	def setHovered(self, hovered):
		self.hovered = hovered

	def render(self, screen):
		screen.blit(self.image, self.rect.topleft)
		if self.hovered:
			pygame.draw.line(screen, (0, 0, 0), self.rect.bottomleft, self.rect.bottomright, width = 1)

	def onClicked(self, world):
		world.triggerPopUpEvent("console." + self.name)

class SaveButton(PopUpButton):
	def __init__(self, name, no):
		self.name = name
		self.no = no
		self.rect = pygame.Rect((0, 0), (360, 40))
		self.hovered = False

	def setPos(self, pos):
		self.rect.topleft = pos

	def getTextPos(self, text):
		return (self.rect.centerx - text.get_width() / 2, self.rect.centery - text.get_height() / 2)

	def isAvailable(self, world):
		return self.name == "save" or world.hasSave(self.no)

	def render(self, screen, world):
		if self.no == 0:
			string = world.getLangValue("save_button.auto")
		else:
			string = world.getLangValue("save_button.no", str(self.no))
		if not world.hasSave(self.no):
			string += world.getLangValue("save_button.empty_sign")
		if self.isAvailable(world):
			text = unifont.render(string, True, (0, 0, 0))
		else:
			text = unifont.render(string, True, (130, 130, 130))
			
		if self.isAvailable(world):
			if self.hovered:
				pygame.draw.rect(screen, (210, 210, 210), self.rect)
			pygame.draw.rect(screen, (0, 0, 0), self.rect, width = 1)
		else:
			pygame.draw.rect(screen, (130, 130, 130), self.rect, width = 1)

		screen.blit(text, self.getTextPos(text))

	def onClicked(self, world):
		if self.isAvailable(world):
			if self.name == "load":
				world.load(self.no)
			elif self.name == "save":
				world.save(self.no)
			world.triggerPopUpEvent("ok")

class LanguageButton(PopUpButton):
	def __init__(self, name):
		self.name = name
		self.rect = pygame.Rect((0, 0), (360, 40))
		self.hovered = False

	def isAvailable(self, world):
		return world.hasLang(self.name)

	def render(self, screen, world):
		string = world.getNameInLang(self.name)
		if self.isAvailable(world):
			text = unifont.render(string, True, (0, 0, 0))
		else:
			text = unifont.render(string, True, (130, 130, 130))
			
		if self.isAvailable(world):
			if self.hovered:
				pygame.draw.rect(screen, (210, 210, 210), self.rect)
			pygame.draw.rect(screen, (0, 0, 0), self.rect, width = 1)
		else:
			pygame.draw.rect(screen, (130, 130, 130), self.rect, width = 1)

		screen.blit(text, self.getTextPos(text))


	def onClicked(self, world):
		if self.isAvailable(world):
			world.setLang(self.name)
			world.triggerPopUpEvent("ok")
