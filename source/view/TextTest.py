class TextTest:
   def __init__(self):
      self.next = self
      f = pygame.font.SysFont(pygame.font.get_default_font(), 17)
      t = f.render("To be or not to be", True, BLACK)
      self.txt = t
      print(t)
      print(f.size("To be or not to be"))
	
   def ProcessInput(self, events):
      pass

   def Update(self, game_counter):
      pass

   def Render(self, screen):
      screen.fill(WHITE)
      p = os.path.join('images', 'letters', 'capital', 'a.png')
      Asurf = pygame.image.load(p)
      p = os.path.join('images', 'letters', 'lowercase', 'a.png')
      asurf = pygame.image.load(p)
      screen.blit(Asurf, (30, 30))
      screen.blit(asurf, (45, 30))
	
      screen.blit(self.txt, (30, 70))