class InventoryScene:
   def __init__(self, overlay):
      self.next = self
      
      i = Inventory()
      ag = ActiveGame()
      ag.SetSavedVar(i.Sabre(), 1)
      ag.SetSavedVar(i.Hammer(), 1)
      ag.SetSavedVar(i.Cannon(), 1)
      ag.SetSavedVar(i.Drill(), 1)
      ag.SetSavedVar(i.CannonMulti(), 1)

      self._layout = ([i.Sabre(), i.Hammer(), i.Drill(), i.Hook()],
                      [i.Cannon(), i.CannonFire(), i.CannonIce(), i.CannonMulti()])
      
      self._i = i
      self._baseScene = overlay
      self._itemSurf = {}
      self._selection = [0, 0]
      
      il = ImageLib
      isurf = self._itemSurf
      
      isurf['cannon-icon'] = il.FromFile(uiImgPath('cannon-icon'))
      isurf[i.Cannon()] = il.FromFile(uiImgPath('ammo-sshot'))
      isurf[i.CannonFire()] = il.FromFile(uiImgPath('ammo-fire'))
      isurf[i.CannonIce()] = il.FromFile(uiImgPath('ammo-ice'))
      isurf[i.CannonMulti()] = il.FromFile(uiImgPath('ammo-multi'))
      isurf[i.Sabre()] = il.FromFile(uiImgPath('sabre-have'))
      isurf[i.Hammer()] = il.FromFile(uiImgPath('hammer-have'))
      isurf[i.Drill()] = il.FromFile(uiImgPath('drill-have'))
      isurf[i.Hook()] = il.FromFile(uiImgPath('hook-have'))
   
   def ProcessInput(self, events):
      for e in events:
         if e.down and e.key == 'start':
            self._baseScene.next = self._baseScene
            self.next = self._baseScene
            return
         if e.down:
            if e.key == 'up':
               self._selection[1] -= 1
               self._selection[1] %= 2
            elif e.key == 'down':
               self._selection[1] += 1
               self._selection[1] %= 2
            elif e.key == 'right':
               self._selection[0] += 1
               self._selection[0] %= 4
            elif e.key =='left':
               self._selection[0] -= 1
               self._selection[0] %= 4
            else:
               self._select(e.key, self._selection[0], self._selection[1])

   def _select(self, key, row, col):
      item = self._layout[col][row]

      i = self._i
      if not i.Check(item):
         print('player does not have %s' % item)
      else:
         i.Equip(key.lower(), item)

   def Update(self, conter):
      pass
   
   def Render(self, screen):
      self._baseScene.Render(screen)
      i = self._i
      isurf = self._itemSurf
      
      
      itemSurf = pygame.Surface((112, 60))
      itemSurf.set_alpha(120)
      
      off_x = int((screen.get_width() - itemSurf.get_width()) / 2)
      off_y = 20

      screen.blit(itemSurf, (off_x, off_y))
      
      col = 0      
      while col < 4:
         row = 0
         while row < 2:
            item = self._layout[row][col]
            
            if isurf[item] and i.Check(item):
               screen.blit(isurf[item], (off_x + 4 + (28 * col), off_y + 4 + (28 * row)))
            
            row += 1
         col += 1
   
      off_x = off_x + 2 + (28 * self._selection[0])
      off_y = off_y + 2 + (28 * self._selection[1])
      pygame.draw.rect(screen, RED, pygame.Rect(off_x, off_y, 24, 24), 1)
   
   
   
   
class Inventory:
   def __init__(self):
      self._ag = ActiveGame()
   
   def Check(self, item):
      return self._ag.GetVar(item) == 1
   
   def HasSabre(self):
      return self.Check('item_sabre')
   
   def HasHammer(self):
      return self.Check('item_hammer')
   
   def HasDrill(self):
      return self.Checu('item_drill')
   
   def HasHook(self):
      return self.Check('item_hook')
   
   def HasCannon(self):
      return self.Check('item_cannon')
   
   def HasCannonFire(self):
      return self.Check('item_cannon_fire')
   
   def HasCannonIce(self):
      return self.Check('item_cannon_ice')
   
   def HasCannonMulti(self):
      return self.Check('item_cannon_multi')
   
   def HasAnyCannon(self):
      return self.HasCannon() or self.HasCannonFire() or self.HasCannonIce() or self.HasCannonMulti()
   
   def Equip(self, button, item):
      if not (button == 'a' or button == 'b' or button == 'x' or button == 'y'):
         print('Could not equip to slot "%s"' % str(key))
         return False
      else:
         # TODO: verify we're not equipping the same item elsewhere
         self._ag.SetSavedVar('equipped_%s' % button, item)
         print('Equipped %s to %s' % (item, button))
         return True
   
   def EquipA(self, val):
      return self._ag.SetSavedVar('equipped_a', val)
   
   def EquipB(self):
      return self._ag.SetSavedVar('equipped_b', val)
   
   def EquipX(self, val):
      return self._ag.SetSavedVar('equipped_x', val)
   
   def EquipY(self, val):
      return self._ag.SetSavedVar('equipped_y', val)
   
   def EquippedA(self):
      return self._Equipped('a')
   def EquippedB(self):
      return self._Equipped('b')
   def EquippedX(self):
      return self._Equipped('x')
   def EquippedY(self):
      return self._Equipped('y')
   def _Equipped(self, button):
      return self._ag.GetVar('equipped_' % button)
   
   def Sabre(self):
      return 'item_sabre'
   def Hammer(self):
      return 'item_hammer'
   def Drill(self):
      return 'item_drill'
   def Hook(self):
      return 'item_hook'
   def Cannon(self):
      return 'item_cannon'
   def CannonFire(self):
      return 'item_cannon_fire'
   def CannonIce(self):
      return 'item_cannon_ice'
   def CannonMulti(self):
      return 'item_cannon_multi'