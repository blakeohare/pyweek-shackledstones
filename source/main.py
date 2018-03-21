
def main():
	counter = 0
	window = GameWindow('Shackled Stones', 30, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2)
	getInputManager().initializeJoystick()
	scene = MainMenuScene()
	while scene != None:
		scene.processInput(getInputManager().get_events(window.pumpEvents()))
		scene.update(counter)
		Graphics2D.Draw.fill(0, 0, 0)
		scene.render(None, (0, 0))
		scene = scene.next
		if getInputManager().escape_attempted:
			scene = None
		counter += 1
		window.clockTick()

main()
