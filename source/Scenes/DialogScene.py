class DialogScene:
   def __init__(self, dlg):
      if not isinstance(dlg, Dialog):
         raise Exception("dlg must an object of type Dialog")
      ImageLib.Add('d-frame', uiImgPath('dframe'))
      
      self.next = self
      self._dlg = dlg
      self._choice = 0
      
   def ProcessInput(self, events):
      d = self._dlg
      
      if 0 != len(events):
         for e in events:
            if e.down:
               if e.key == 'up' and d.State() == D_QUESTION:
                  self._choice -= 1
                  self._choice %= len(self._dlg.Choices())
               
               if e.key == 'down' and d.State() == D_QUESTION:
                  self._choice += 1
                  self._choice %= len(self._dlg.Choices())
            else:
               if e.key == 'B':
                  if self._dlg.State() == D_QUESTION:
                     self._dlg.Answer(self._choice)
                  self._dlg.Advance()

   def Update(self, game_counter):
      pass

   def Render(self, screen):
      d = self._dlg
      
      if d.State() == D_END:
         print("TODO: Advance to next scene")
         return
      
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
         cy = int(D_TEXT_OFFSET_Y + (lineNo + self._choice) * _font.get_height() + (.5 * _font.get_height()))
         cx = D_TEXT_OFFSET_X + 6
         
         # draw choice indicator
         pygame.draw.circle(screen, BLUE, (cx, cy), 4)
         
         # print choice text
         for c in d.Choices():
            cSurf = _font.render(c, True, BLACK)
            screen.blit(cSurf, (D_ANSWER_OFFSET_X, D_TEXT_OFFSET_Y + lineNo * _font.get_height()))
            lineNo += 1
         