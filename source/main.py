TILE_COLUMN_COUNT = 24
TILE_ROW_COUNT = 18



def main():
	
	counter = 0
	
	pygame.init()
	
	width = TILE_COLUMN_COUNT * 16
	height = TILE_ROW_COUNT * 16
	
	screen = pygame.display.set_mode((width * 2, height * 2))
	
	virtual_screen = pygame.Surface((width, height))
	
	scene = GamePlayScene()
	#scene = TextTest()
	
	while scene != None:
			
		begin = time.time()
		
		scene.ProcessInput(_inputManager.get_events())
		
		scene.Update(counter)
		
		virtual_screen.fill((0,0,0))
		
		scene.Render(virtual_screen)
		
		pygame.transform.scale(virtual_screen, (width * 2, height * 2), screen)
		
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

if testCode:
   RunTests()
else:
   main()