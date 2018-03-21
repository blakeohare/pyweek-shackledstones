
def main():

	counter = 0
	global _font, _activeScreen
	
	current_screen_mode = 'windowed'
	
	pygame.init()
	_font = pygame.font.Font(TEXT_FONT, 13)	
	
	width = TILE_COLUMN_COUNT * 16
	height = TILE_ROW_COUNT * 16
	
	screen = pygame.display.set_mode((SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2))
	pygame.display.set_icon(pygame.image.load("icon.png"))
	pygame.display.set_caption("Shackeld Stones")
		
	virtual_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
	_activeScreen = virtual_screen
	
	getInputManager().initializeJoystick()
	
	scene = MainMenuScene()
	
	while scene != None:
			
		begin = time.time()
		
		scene.processInput(getInputManager().get_events())
		
		scene.update(counter)
		
		virtual_screen.fill((0,0,0))
		
		scene.render(virtual_screen, (0, 0))
		
		pygame.transform.scale(virtual_screen, screen.get_size(), screen)
		
		scene = scene.next
		
		if getInputManager().escape_attempted:
			scene = None
		
		counter += 1
		
		pygame.display.flip()
		
		end = time.time()
		
		duration = end - begin
		difference = 1 / 30.0 - duration
		if difference > 0:
			time.sleep(difference)

main()