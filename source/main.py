TILE_COLUMN_COUNT = 24
TILE_ROW_COUNT = 18



def main():
	
	counter = 0
	
	pygame.init()
	
	screen = pygame.display.set_mode((640, 480))
	
	width = TILE_COLUMN_COUNT * 16
	height = TILE_ROW_COUNT * 16
	virtual_screen = pygame.Surface((width, height))
	
	scene = GamePlayScene()
	
	while scene != None:
			
		begin = time.time()
		
		scene.ProcessInput(_inputManager.get_events())
		
		scene.Update(counter)
		
		virtual_screen.fill((0,0,0))
		
		scene.Render(virtual_screen)
		
		pygame.transform.scale(virtual_screen, (640, 480), screen)
		
		scene = scene.next
		
		if _inputManager.escape_attempted:
			scene = None
		
		counter += 1
		
		pygame.display.flip()
		
		end = time.time()
		
		duration = end - begin
		difference = 1 / 30.0 - duration
		if difference > 0:
			time.sleep(difference)

if not testCode:
   main()