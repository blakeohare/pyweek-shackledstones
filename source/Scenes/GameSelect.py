class GameSelectScene:
   def __init__(self, prevScene):
      self._prevScene = prevScene
      self.next = self
      
      self._eraseMode = False
      self._erase = False
      self._cancel = False
      self._selection = 0
      self._fc = 0
      self._frame = 0
      self._gears = []
      i = 1
      while i <= 4:
         self._gears.append(ImageLib.FromFile(uiImgPath('gear%d' % i)))
         i += 1

   
   def ProcessInput(self, events):
      for e in events:
         if e.down:
            if self._erase or self._cancel:
               if e.Up():
                  self._erase = False
                  self._cancel = False
                  self._selection = 2
                  return
               if e.Down():
                  self._erase = False
                  self._cancel = False
                  self._selection = 0
                  return
               if e.Right() or e.Left():
                  self._erase = not self._erase
                  self._cancel = not self._cancel
                  return
            elif e.Up():
               self._selection -= 1
               self._selection %= 4
               
            elif e.Down():
               self._selection += 1
               self._selection %= 4
            
            if self._selection == 3:
               self._erase = True

            if e.B():
               if self._cancel:
                  self.next = self._prevScene
                  self._prevScene.next = self._prevScene
                  return
               
               if self._erase:
                  self._eraseMode = True
                  return
               
               if self._eraseMode:
                  GameContext().DeletePlayer(self._selection + 1)
                  self._eraseMode = False
                  return
               
               # TODO: BUG I'm always transfering to name select, only do this on new game
               newGame = not GameContext().GetPlayerName(self._selection + 1)
               GameContext().SetActiveGame(self._selection + 1)
               
               if newGame:
                  self.next = NameEntryScene()
                  
   
   def Update(self, conter):
      pass
   
   def Render(self, screen):
      # what color is used for everything else
      txtColor = BLACK
      # what color is in the game select thing
      descColor = WHITE
      
      self._fc += 1
      frame = self._frame
      if (self._fc % 2 == 0):
         self._frame += 1
         self._frame %= len(self._gears)
      g = self._gears[frame]

      screen.fill(WHITE)
      gc = GameContext()
      
      sw = screen.get_width()
      gameSel_y = 20
      
      gameTxt = "Game Select"
      if self._eraseMode:
         gameTxt = 'Erase Game'
      gameSel = render_text_size(23, gameTxt, txtColor)
      screen.blit(gameSel, (int((sw - gameSel.get_width()) / 2), gameSel_y))
   
      post_title_y = gameSel_y + gameSel.get_height() + 10
   
      # game sel width
      sel_w = int(.7 * sw)
      # game sel height
      sel_h = 45
      # separation between game sel blocks
      gameSel_sep = 15
      selSurf = pygame.Surface((sel_w, sel_h))
      selSurf.set_alpha(ALPHA)
      selSurf.fill(BLACK)
      
      i = 0
      while i < 3:
         sx = int(sw * .2)
         sy = i * (gameSel_sep + sel_h) + post_title_y

         if i == self._selection:
            screen.blit(g, (sx - 50, sy))

         screen.blit(selSurf, (sx, sy))
         
         slot_num = i + 1
         name = gc.GetPlayerName(slot_num)
         if not name:
            nameSurf = render_text_size(17, 'New Game', descColor)
            nx = sx + 10 #int((selSurf.get_width() - nameSurf.get_width())/2) + sx
            ny = int((selSurf.get_height() - nameSurf.get_height()) / 2) + sy
            screen.blit(nameSurf, (nx, ny))

         #end while
         i += 1
      
      erase = render_text_size(20, 'Erase', txtColor)
      cancel = render_text_size(20, 'Cancel', txtColor)
      
      screen.blit(erase, (75, 240))
      cx = 230
      screen.blit(cancel, (cx, 240))
      
      gy = 230
      if self._erase:
         screen.blit(g, (sx - 50, gy))
      if self._cancel:
         screen.blit(g, (cx + 10 + cancel.get_width(), gy))
      
      