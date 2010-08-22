class TextTest:
   def __init__(self, dlg):
      ImageLib.Add('d-frame', uiImgPath('dframe'))
      
      self.next = self
      self._dlg = dlg
      
   def ProcessInput(self, events):
      if 0 != len(events):
         for e in events:
            if e.key == 'B' and e.up:
               if self._dlg.State() == D_QUESTION:
                  # TODO
                  self._dlg.Answer(1)
               self._dlg.Advance()

   def Update(self, game_counter):
      pass

   def Render(self, screen):
      d = self._dlg
      screen.fill(WHITE)
      
      p = d.Profile()
      pSurf = None

      if p:
         p = portraitPath(p)
         if p:
            pSurf = ImageLib.FromFile(p)
      if pSurf:
         screen.blit(pSurf, (4, 120))
      
      df = ImageLib.Get('d-frame')
      screen.blit(df, (0,screen.get_height() - df.get_height() - 4))

      txt = d.Text()
      txt = txt.split('\n')
      tSurf = []
      for t in txt:
         if t == '$nl$':
            t = ''
         tSurf.append(_font.render(t, True, BLACK))
      
      lineNo = 0
      for t in tSurf:
         screen.blit(t, (D_TEXT_OFFSET_X, D_TEXT_OFFSET_Y + lineNo * _font.get_height()))
         lineNo += 1

      if D_QUESTION == d.State():
         for c in d.Choices():
            cSurf = _font.render(c, True, BLACK)
            screen.blit(cSurf, (D_ANSWER_OFFSET_X, D_TEXT_OFFSET_Y + lineNo * _font.get_height()))
            lineNo += 1