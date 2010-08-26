class NameEntryScene:
   def __init__(self):
      self.next = self
      self._selection = [0, 0]
      self._erase = False
      self._done = False
      self._name = 'Lapis'
      self._nameLen = 10
      self._tic = 0
      self._mark = True
   
   def ProcessInput(self, events):
      for e in events:
         if e.down:
            if e.Up():
               self._move(0, -1)
            if e.Down():
               self._move(0, 1)
            if e.Left():
               self._move(-1, 0)
            if e.Right():
               self._move(1, 0)
            if e.A():
               if self._isCommand():
                  if len(self._name) != 0 and self._done:
                     ActiveGame().SetSavedVar('name', self._name)
                     ActiveGame().SaveToFile()

                     # TODO
                     c = open('map_test.txt', 'rt')
                     t = c.read().split('\n')
                     c.close()
                     map_name = trim(t[0])
                     coords = trim(t[1]).split(',')
                     scene = GamePlayScene(map_name, int(coords[0]) << 4, int(coords[1]) << 4)
                     
                     scene.next = scene
                     self.next = scene
                     return
                     
                  if self._erase:
                     if len(self._name):
                        self._name = self._name[0:-1]
                        return
                        
               else:
                  if (len(self._name) < self._nameLen):
                     self._name += self._toLetter()
   
   def _toLetter(self):
      s = self._selection
      if s[1] == 4:
         return None
      letters = ['A', 'N', 'a', 'n']
      return chr(ord(letters[s[1]]) + s[0])
   
   def _isCommand(self):
      return self._erase or self._done
   
   def _move(self, x, y):
      s = self._selection
      
      if s[1] == 4:
         if y == 0:
            self._done = not self._done
            self._erase = not self._erase
         else:
            s[1] += y
            s[1] %= 5
            self._done = False
            self._erase = False
      else:
         s[0] += x
         s[0] %= 13
         s[1] += y
         s[1] %= 5
         
         if s[1] == 4:
            if s[0] < 6:
               self._erase = True
            else:
               self._done = True
   
   def Update(self, conter):
      pass
   
   def Render(self, screen):
      self._tic += 1
      sz = 18
      dx = int(sz * 1.3)
      dy = int(sz * 1.5)
      letters = ['A','N','a','n']
      start_off_x = 40
      start_off_y = 80
      
      o_y = start_off_y
      for letter in letters:
         i = 0
         o_x = start_off_x
         if (letters.index(letter) >= 2):
            o_x += int(dx / 6)
         while i < 13:
            c = chr(ord(letter) + i)
            surf = render_text_size(sz, c, WHITE)
            screen.blit(surf, (o_x + int((dx - surf.get_width()) / 2.0), o_y))
            o_x += dx
            i += 1
         o_y += dy
         if (letters.index(letter) == 0):
            o_y += dy / 5
         if (letters.index(letter) == 1):
            o_y += dy / 3
      
      # draw current name
      
      if self._tic % 5 == 0:
         self._mark = not self._mark
      if len(self._name) < self._nameLen and self._mark:
         name = render_text_size(sz, 'Name: %s--' % self._name, WHITE)
      else:
         name = render_text_size(sz, 'Name: %s' % self._name, WHITE)

      screen.blit(name, (start_off_x, start_off_y/2))
      
      # draw Done and Erase
      by = start_off_y + 5 * dy
      
      erase = render_text_size(sz, 'Erase', WHITE)
      ebx = int(screen.get_width() / 4)
      screen.blit(erase, (ebx, by))
      
      done = render_text_size(sz, 'Done', WHITE)
      dbx = 3 * int(screen.get_width() / 5)
      screen.blit(done, (dbx, by))
      
      # draw selection bubble
      s = self._selection
      if s[1] == 4:
         cy = by + erase.get_height() - 5
         if self._erase:
            b = (ebx + 20, cy)
            e = (ebx + erase.get_width(), cy)
            pygame.draw.line(screen, RED, b, e)
         if self._done:
            b = (dbx + 15, cy)
            e = (dbx + done.get_width(), cy)
            pygame.draw.line(screen, RED, b, e)
      else:
         if s[1] < 2:
            x = start_off_x + s[0] * dx + int(dx / 2.0)
            y = start_off_y + s[1] * dy + int(dy / 2.0)
            if s[1] == 1:
               y += int(dy / 7.0)
            pygame.draw.circle(screen, RED, (x, y), int(sz/1.15), 1)
         else:
            x = start_off_x + s[0] * dx + int(dx / 2.0) + int(dx/6)
            y = start_off_y + int(dy/5) + int(dy/3) + s[1] * dy + int(dy / 2.1)
            if s[1] == 1:
               y += int(dy / 7.0)
            pygame.draw.circle(screen, RED, (x, y), int(sz/2), 1)
