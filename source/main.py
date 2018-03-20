TILE_COLUMN_COUNT = 24
TILE_ROW_COUNT = 18

def main():
	
	counter = 0
	global _font
	
	current_screen_mode = 'windowed'
	
	pygame.init()
	_font = pygame.font.Font(TEXT_FONT, 13)	
	
	width = TILE_COLUMN_COUNT * 16
	height = TILE_ROW_COUNT * 16
	
	screen = pygame.display.set_mode((width * 2, height * 2))
	pygame.display.set_icon(pygame.image.load("icon.png"))
		
	virtual_screen = pygame.Surface((width, height))
	
	_inputManager.initializeJoystick()
	
	scene = MainMenuScene()
	
	screen_width = screen.get_width()
	screen_height = screen.get_height()
	
	while scene != None:
			
		begin = time.time()
		
		scene.processInput(_inputManager.get_events())
		
		scene.update(counter)
		
		virtual_screen.fill((0,0,0))
		
		scene.render(virtual_screen)
		
		pygame.transform.scale(virtual_screen, (screen_width, screen_height), screen)
		
		scene = scene.next
		
		change_video_mode = _inputManager.VideoModeChange()
		if change_video_mode != None:
			if current_screen_mode == change_video_mode:
				current_screen_mode = 'windowed'
				screen = pygame.display.set_mode((width * 2, height * 2))
				screen_width = screen.get_width()
				screen_height = screen.get_height()
			else:
				current_screen_mode = change_video_mode
			
				if change_video_mode == 'wide':
					current_screen_mode = 'wide'
					screen = pygame.display.set_mode((1400, 900), FULLSCREEN)
					screen_width = screen.get_width()
					screen_height = screen.get_height()
				else:
					screen = pygame.display.set_mode((width * 2, height * 2), FULLSCREEN)
					screen_width = screen.get_width()
					screen_height = screen.get_height()
		
		if _inputManager.escape_attempted:
			scene = None
		
		counter += 1
		
		pygame.display.flip()
		
		end = time.time()
		
		duration = end - begin
		difference = 1 / 30.0 - duration
		if difference > 0:
			time.sleep(difference)
		else:
			#print("Framerate dropping! (" + str(counter) + ")")
			pass

if testCode:
   RunTests()
else:
   main()