class DialogScene:
   def __init__(self, dlg, sourceScene):
      if not isinstance(dlg, Dialog):
         raise Exception("dlg must an object of type Dialog")
      ImageLib.Add('d-frame', uiImgPath('dframe'))
      
      self.next = self
      self._source = sourceScene
      self._dlg = dlg
      self._choice = 0
      self._lineHave = 5
      self._more = False
      self._moreDot = True
      self._truncating = True
      self._fastText = False
      self._curLine = 0
      self._curLetter = 0
      self._tick = 0
      
   def ProcessInput(self, events):
      d = self._dlg
      
      if 0 != len(events):
         for e in events:
            if e.down:
               if e.Up() and d.State() == D_QUESTION:
                  self._choice -= 1
                  self._choice %= len(self._dlg.Choices())
               
               if e.Down() and d.State() == D_QUESTION:
                  self._choice += 1
                  self._choice %= len(self._dlg.Choices())
            else:
               if e.A() or e.B():
                  if self._truncating:
                     self._curLetter = 0
                     self._fastText = True
                     self._truncating = False
                  elif self._more:
                     self._curLine += self._lineHave
                     self._curLetter = 0
                     self._fastText = False
                     self._truncating = False
                     self._more = False
                  else:
                     if self._dlg.State() == D_QUESTION:
                        self._dlg.Answer(self._choice)
                     self._curLine = 0
                     self._curLetter = 0
                     self._fastText = False
                     self._truncating = False
                     self._dlg.Advance()

   def Update(self, game_counter):
      pass

   def Render(self, screen):
      self._tick += 1
      self._source
      d = self._dlg
      self._curLetter += 1
      
      if d.State() == D_END:
         self.next = self._source
         self._source.next = self._source

      self._source.Render(screen)
      
      p = d.Profile()
      pSurf = None

      if p:
         side = 'right'
         if p == 'mc_portrait':
            side = 'left'
         p = portraitPath(p)
         if p:
            pSurf = ImageLib.FromFile(p)
      if pSurf:
         if side == 'left':
            screen.blit(pSurf, (4, 110))
         else:
            screen.blit(pSurf, (290, 110))
         
      df = ImageLib.Get('d-frame')
      screen.blit(df, (0,screen.get_height() - df.get_height() - 4))
      
      textSurface= pygame.Surface(((df.get_width() - (2 * D_TEXT_OFFSET_X)), df.get_height()))
      wt = wrap_text(textSurface, d.Text(), _font)
      
      linesRequired = len(wt)
      
      tSurf = []

      lineNo = 0
      runningTotal = 0

      while lineNo < self._lineHave:
         idx = self._curLine + lineNo
         if idx < len(wt):
            line = wt[idx]
            if not self._fastText:
               if not (runningTotal + len(line) <= self._curLetter):
                  delta = self._curLetter - runningTotal
                  line = line[0:delta]
                  self._truncating = True
               else:
                  self._truncating = False
            runningTotal += len(line)
            tSurf.append(_font.render(line, True, BLACK))
            
            if self._truncating:
               break
         lineNo += 1

      if linesRequired > self._lineHave and (lineNo == self._lineHave):
         self._more = True
      if self._curLine + self._lineHave >= linesRequired:
         self._more = False

      lineNo = 0
      for t in tSurf:
         screen.blit(t, (D_TEXT_OFFSET_X, D_TEXT_OFFSET_Y + lineNo * _font.get_height()))
         lineNo += 1
      if D_QUESTION == d.State() and not self._truncating:
         cy = int(D_TEXT_OFFSET_Y + (lineNo + self._choice) * _font.get_height() + (.5 * _font.get_height()))
         cx = D_TEXT_OFFSET_X + 6
         
         # draw choice indicator
         pygame.draw.circle(screen, BLUE, (cx, cy), 4)
         
         # print choice text
         for c in d.Choices():
            cSurf = _font.render(c, True, BLACK)
            screen.blit(cSurf, (D_ANSWER_OFFSET_X, D_TEXT_OFFSET_Y + lineNo * _font.get_height()))
            lineNo += 1
         
      if self._more:
         if (self._tick % 10 == 0):
            self._moreDot = not self._moreDot
         if self._moreDot:
            pygame.draw.circle(screen, WHITE, (370, 273), 2)