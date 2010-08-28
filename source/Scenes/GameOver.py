class GameOverScene:
   def _LastSave(self):
      pass
   
   def _MainMenu(self):
      mm = MainMenuScene()
      self.next = mm
      mm.next = mm
   
   def _Quit(self):
      self.next = None

   def __init__(self):
      self.next = self
      
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
            if e.Up():
               self._selection -= 1
               self._selection %= 3
            if e.Down():
               self._selection += 1
               self._selection %= 3
            if e.A() or e.B() or e.Start():
               if self._selection == 0:
                  self._LastSave()
               if self._selection == 1:
                  self._MainMenu()
               if self._selection == 2:
                  self._Quit()
   
   def Update(self, conter):
      pass
   
   def Render(self, screen):
      self._fc += 1
      
      frame = self._frame
      if (self._fc % 2 == 0):
         self._frame += 1
         self._frame %= len(self._gears)

      screen.fill(BLACK)
      sw = screen.get_width()
      
      death = render_text_size(23, "You Have Perished", WHITE)
      death_sub = render_text_size(15,  "The empire has lost its best hope", WHITE)
      death_sub2 = render_text_size(15, "for salvation. Are there any that", WHITE)
      death_sub3 = render_text_size(15, "may hope to fill your place?", WHITE)

      death_x = int((sw - death.get_width()) / 2)
      death_y = 23
      screen.blit(death, (death_x, death_y))
      death_x = int((sw - death_sub.get_width()) / 2)
      death_y = death_y + death.get_height() + 4
      screen.blit(death_sub, (death_x, death_y))
      death_x = int((sw - death_sub2.get_width()) / 2)
      death_y = death_y + death_sub.get_height()
      screen.blit(death_sub2, (death_x, death_y))
      death_x = int((sw - death_sub3.get_width()) / 2)
      death_y = death_y + death_sub2.get_height()
      screen.blit(death_sub3, (death_x, death_y))
      
      cont = render_text_size(23, "Go to Last Save", WHITE)
      main = render_text_size(23, "Main Menu", WHITE)
      quit = render_text_size(23, "Quit", RED)
      
      cx = 135 #int((sw - cont.get_width()) / 2)
      cy = death_y + death_sub3.get_height() + 20
      mx = cx #int((sw - main.get_width()) / 2)
      my = cy + cont.get_height() + 15
      qx = cx #int((sw - quit.get_width()) / 2)
      qy = my + main.get_height() + 13
      
      screen.blit(cont, (cx, cy))
      screen.blit(main, (mx, my))
      screen.blit(quit, (qx, qy))
      
      gx = cx - 50
      gy = cy + (43 * self._selection) - 7
      g = self._gears[frame]
      screen.blit(g, (gx, gy))