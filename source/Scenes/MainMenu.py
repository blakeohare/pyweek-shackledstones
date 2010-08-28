class MainMenuScene:
   def StartGame(self):
      scene = GameSelectScene(self)
      self.next = scene

   def Setup(self):
      self.next = JoystickConfigScene()
   
   def Credits(self):
      GameContext().SetActiveGame(1)
      ActiveGame().SetSavedVar('name', 'SUE')
      if os.path.exists('map_test.txt'):
         c = open('map_test.txt', 'rt')
         t = c.read().split('\n')
         c.close()
         map_name = trim(t[0])
         coords = trim(t[1]).split(',')
         scene = GamePlayScene(map_name, int(coords[0]) << 4, int(coords[1]) << 4)
      else:
         scene = GamePlayScene('test_level', 100, 100)
      self.next = scene
      scene.next = scene

   def __init__(self):
      self._fc = 0
      self.next = self
      self._selection = 2
      self._frame = 0
      
      self._gears = []
      i = 1
      while i <= 4:
         self._gears.append(ImageLib.FromFile(uiImgPath('gear%d' % i)))
         i += 1
   
   def ProcessInput(self, events):
      for e in events:
         if e.down:
            if e.Down():
               self._selection = (self._selection + 1) % 3
            if e.Up():
               self._selection = (self._selection - 1) % 3
            if e.A() or e.Start():
               if self._selection == 0:
                  self.StartGame()
               elif self._selection == 1:
                  self.Setup()
               elif self._selection == 2:
                  self.Credits()

   def Update(self, conter):
      play_music('title')
   
   def Render(self, screen):
      self._fc += 1
      
      frame = self._frame
      if (self._fc % 2 == 0):
         self._frame += 1
         self._frame %= len(self._gears)
      
      title = render_text_size(45, GAME_NAME, WHITE, MENU_FONT)
      start = render_text_size(20, "Start", WHITE, MENU_FONT)
      setup = render_text_size(20, "Setup", WHITE, MENU_FONT) 
      credits = render_text_size(20, "Credits", WHITE, MENU_FONT) 
      
      titleOffset = (int((screen.get_width() - title.get_width()) / 2), 20)
      startOffset = (100, 100)
      setupOffset = (100, 150)
      creditsOffset = (100, 200)
      
      screen.blit(title, titleOffset)
      screen.blit(start, startOffset)
      screen.blit(setup, setupOffset)
      screen.blit(credits, creditsOffset)
      
      gx = startOffset[0] - 50
      gy = startOffset[1] - 10 + (self._selection * 50)
      g = self._gears[frame]
      screen.blit(g, (gx, gy))
