class MainMenuScene:
   def __init__(self):
      self._fc = 0
      self.next = self
      self._selection = 0
      self._frame = 0
      
      self._gears = []
      i = 1
      while i <= 4:
         self._gears.append(ImageLib.FromFile(uiImgPath('gear%d' % i)))
         i += 1
   
   def ProcessInput(self, events):
      for e in events:
         if e.down:
            if e.key == 'down':
               self._selection = (self._selection + 1) % 3
            if e.key == 'up':
               self._selection = (self._selection - 1) % 3
            if e.key == 'B':
               if self._selection == 0:
                  self.StartGame()
               elif self._selection == 1:
                  self.Setup()
               elif self._selection == 2:
                  self.Credits()

   def Update(self, conter):
      pass
   
   def Render(self, screen):
      self._fc += 1
      
      frame = self._frame
      if (self._fc % 2 == 0):
         self._frame += 1
         self._frame %= len(self._gears)
      
      titleOffset = (20, 20)
      startOffset = (100, 100)
      setupOffset = (100, 150)
      creditsOffset = (100, 200)
      
      title = render_text_size(45, "Steapmpunk Game", WHITE, MENU_FONT)
      start = render_text_size(20, "Start", WHITE, MENU_FONT)
      setup = render_text_size(20, "Setup", WHITE, MENU_FONT) 
      credits = render_text_size(20, "Credits", WHITE, MENU_FONT) 
      
      screen.blit(title, titleOffset)
      screen.blit(start, startOffset)
      screen.blit(setup, setupOffset)
      screen.blit(credits, creditsOffset)
      
      gx = startOffset[0] - 50
      gy = startOffset[1] - 10 + (self._selection * 50)
      g = self._gears[frame]
      screen.blit(g, (gx, gy))
   
   def StartGame(self):
      print("start Game")
   
   def Setup(self):
      print("Setup")
   
   def Credits(self):
      print("Credits")