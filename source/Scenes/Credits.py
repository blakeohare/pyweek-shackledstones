class CreditsScene:
   def __init__(self):
      self.next = self
      self._y = 250
      
      lines = [
         "heading1:%s" % GAME_NAME,
         "heading:Team Nerdparadise",
         "www.nerdparadise.com",
         "",
         "",
         "heading:Programming",
         "Blake O'Hare",
         "Richard Bailey",
         "Adrian Cline",
         "",
         "",
         "",
         "heading:Pixel Art",
         "Angel McLaughlin",
         "",
         "",
         "",
         "heading:Cutscene, Menu Art",
         "Fixception",
         "",
         "",
         "",
         "heading:Music",
         "Adrian Cline",
         "",
         "",
         "",
         "heading:Level Design",
         "Christine Sandquist",
         "YY",
         "Brett S."
         "",
         "",
         "",
         "heading:Special Thanks...",
         "www.anke-art.de, for Fortunaschwein font",
         "Ray Meadows, for RM Typerighter font",
         "",
         "",
         "",
         "heading:Welcoming To Team",
         "heading:Nerdparadise",
         "Christine Sandquist",
         "YY",
         "Fixception",
      ]
      
      cSurf = []
      max_x = 0
      cum_y = 0
      for l in lines:
         sz = 18
         if l.startswith('heading1:'):
            l = l.split(':')[1]
            sz = 45
         if l.startswith('heading:'):
            l = l.split(':')[1]
            sz = 30
         surf = render_text_size(sz, l, WHITE)
         cSurf.append(surf)
         max_x = max(max_x, surf.get_width())
         cum_y += surf.get_height()
      
      self._credits = pygame.Surface((max_x, cum_y))
      
      y = 0
      for s in cSurf:
         x = int((max_x - s.get_width()) / 2)
         self._credits.blit(s, (x, y))
         y += s.get_height()
   
   def ProcessInput(self, events):
      for e in events:
         if e.down:
            if e.Start():
               mm = MainMenuScene()
               self.next = mm
               mm.next = mm
   
   def Update(self, conter):
      pass
   
   def Render(self, screen):
      c = self._credits
      sw = screen.get_width()
      offy = self._y
      
      screen.blit(c, (int((sw - c.get_width()) / 2), offy))
      
      self._y -= 1
      
      if (c.get_height() - abs(self._y)) == -40:
         mm = MainMenuScene()
         self.next = mm
         mm.next = mm