class TextTest:
   def __init__(self):
      self.next = self
      ImageLib.Add('d-frame', uiImgPath('dframe'))
      self.portrait = pygame.image.load(portraitPath('filler'))
      f = pygame.font.SysFont(pygame.font.get_default_font(), 20)
      t = f.render("To be or not to be\nNew line! wheewheewhee!", True, BLACK)
      self.txt = t
      print(t)
      print(f.size("To be or not to be\tNew line! wheewheewheee!"))
	
   def ProcessInput(self, events):
      if 0 != len(events):
         print(str(events))
         for e in events:
            print(e)

   def Update(self, game_counter):
      pass

   def Render(self, screen):
      screen.fill(WHITE)

      screen.blit(self.portrait, (4, 130))
      df = ImageLib.Get('d-frame')
      screen.blit(df, (0,screen.get_height() - df.get_height() - 4))
      
      
