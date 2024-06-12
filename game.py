'''
This program is based on MPL-2.0 license.
This program is open-source at 
'''

import json, time, os, pygame

pygame.init()
pygame.font.init()

from lib import util
from lib import info

def load(world, no):
	with open("saves/save" + str(no), "r", encoding = "utf8") as f:
		world.fromDict(json.loads(f.read()))

def save(world, no):
	with open("saves/save" + str(no), "w", encoding = "utf8") as f:
		f.write(json.dumps(world.toDict(), separators = (',', ':')))

screen = pygame.display.set_mode((1200, 950))
pygame.display.set_caption("A Dark Room")
clock = pygame.time.Clock()
world = util.World()

world.addItem("wood", 10)

if os.path.isfile("saves/save0"):
	load(world, 0)
else:
	world.setLang("zh_cn")

world.addTemperatureLogger()

progress = 0
lastCycleTime = time.time()

bl = True
while bl:
	if world.hangLoading >= 0:
		hangLoading = world.hangLoading
		world.__init__()
		load(world, hangLoading)
		lastCycleTime = time.time()
	elif world.hangSaving >= 0:
		save(world, world.hangSaving)
		world.hangSaving = -1
	elif world.hangRestart:
		lang = world.getLang()
		world.__init__()
		world.setLang(lang)
		lastCycleTime = time.time()
		world.addItem("wood", 10)
		world.addTemperatureLogger()

	if world.adventureHang:
		world.delAdventure()

	screen.fill("white")

	mousePos = pygame.mouse.get_pos()
	currentTime = time.time()
	buttons = world.getButtons()
	columnBar = world.getColumnBar()
	consoleBar = world.getConsoleBar()
	onAdventure = world.isOnAdventure()
	hasPopUp = world.hasPopUp()

	#pygame.sprite.Group(*buttons).draw(screen)

	if currentTime - lastCycleTime >= 10.0:
		lastCycleTime = time.time()
		world.run()

	if onAdventure:
		world.adventure.itemTab.render(screen, world)
		world.adventure.mapSet.render(screen, world)
		world.adventure.mapSet.handleHover(world, mousePos, screen)
	else:
		if world.currentColumn == "house":
			if world.testProperty("can_construct"):
				screen.blit(info.getConstructText(world), (350, 200))
			if world.testProperty("can_craft"):
				screen.blit(info.getCraftText(world), (500, 200))
			if world.testProperty("can_trade"):
				screen.blit(info.getTradeText(world), (650, 200))

		if world.shouldRenderCareerActionBar():
			world.careerActionBar.render(screen, world)

		dy = 0
		for itemTab in world.getItemTabs():
			itemTab.render(screen, world, (800, 50 + dy))
			dy += itemTab.getHeight() + 24

		if world.currentColumn == "adventure":
			world.adventurePreparationTab.render(world, screen)
			if not hasPopUp:
				world.adventurePreparationTab.handleHover(world, mousePos, screen)

		for button0 in buttons:
			if not hasPopUp:
				button0.setHovered(button0.rect.collidepoint(mousePos))
			button0.render(screen, world)

		if not hasPopUp:
			if world.shouldRenderCareerActionBar():
				world.careerActionBar.handleHover(world, mousePos, screen)
			for button0 in buttons:
				if button0.isHovered():
					button0.renderTip(screen, world)
			for button0 in columnBar.columnButtons:
				button0.setHovered(button0.rect.collidepoint(mousePos))
			for button0 in consoleBar.consoleButtons:
				button0.setHovered(button0.rect.collidepoint(mousePos))

		columnBar.render(screen)

	world.renderLogger(screen, (100, 20))
	consoleBar.render(screen)
		
	if hasPopUp:
		popUp = world.getTopPopUp()
		popUp.render(screen, world, mousePos)
		popUp.renderButtonTip(screen, world)
	
	pygame.display.flip()
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
			if hasPopUp:
				popUp.handleClick(world, mousePos)
			elif onAdventure:
				world.adventure.mapSet.handleClick(mousePos)
			else:
				if world.currentColumn == "adventure":
					world.adventurePreparationTab.handleClick(world, mousePos)
				if world.shouldRenderCareerActionBar():
					world.careerActionBar.handleClick(world, mousePos)
				for button0 in buttons:
					if button0.rect.collidepoint(mousePos):
						button0.onClicked(world)
				for button0 in columnBar.columnButtons:
					if button0.rect.collidepoint(mousePos):
						button0.onClicked(world)
			if not hasPopUp:
				for button0 in consoleBar.consoleButtons:
					if button0.rect.collidepoint(mousePos):
						button0.onClicked(world)
		elif event.type == pygame.KEYDOWN:
			if onAdventure and not hasPopUp:
				if event.key == pygame.K_UP:
					world.adventure.moveY(-1)
				elif event.key == pygame.K_DOWN:
					world.adventure.moveY(1)
				elif event.key == pygame.K_LEFT:
					world.adventure.moveX(-1)
				elif event.key == pygame.K_RIGHT:
					world.adventure.moveX(1)
		elif event.type == pygame.QUIT:
			bl = False
			save(world, 0)

pygame.quit()