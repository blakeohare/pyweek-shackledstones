class TextTest:
   def __init__(self, dlg):
      ImageLib.Add('d-frame', uiImgPath('dframe'))
      
      self.next = self
      self._dlg = dlg
      
   def ProcessInput(self, events):
      if 0 != len(events):
         print(str(events))
         for e in events:
            print(e)

   def Update(self, game_counter):
      pass

   def Render(self, screen):
      screen.fill(WHITE)
      
      d = self._dlg
      txt = _font.render(d.Text(), True, BLACK)
      p = d.Profile()
      p = portraitPath(p)
      
      if p:
         pSurf = ImageLib.FromFile(p)
      else:
         pSurf = None
      
      screen.blit(txt, (10, 20))
      if pSurf:
         screen.blit(pSurf, (4, 120))
      
      df = ImageLib.Get('d-frame')
      screen.blit(df, (0,screen.get_height() - df.get_height() - 4))
      
      
