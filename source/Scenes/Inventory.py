class InventoryScene:
   def __init__(self, overlay):
      i = Inventory()
      ag = ActiveGame()
      print(ag)
      ag.SetSavedVar(i.Sabre(), 1)
      ag.SetSavedVar(i.Hammer(), 1)
      ag.SetSavedVar(i.Cannon(), 1)
      ag.SetSavedVar(i.CannonMulti(), 1)
      
      self._i = i
      self._baseScene = overlay
      self.next = self
   
   def ProcessInput(self, events):
      for e in events:
         if e.down and e.key == 'start':
            self._baseScene.next = self._baseScene
            self.next = self._baseScene
   
   def Update(self, conter):
      pass
   
   def Render(self, screen):
      self._baseScene.Render(screen)
      c = pygame.Color(255, 255, 255, 125)
      oa = screen.get_alpha()
      s = pygame.Surface((100, 100))
      
      s.set_alpha(c.a)
      pygame.draw.rect(s, c, pygame.Rect(0,0, 100, 100))
      screen.blit(s, (0,0))
   
   
   
class Inventory:
   def __init__(self):
      self._ag = ActiveGame()
   
   def HasSabre(self):
      return self._ag.GetVar('item_sabre') == 1
   
   def HasHammer(self):
      return self._ag.GetVar('item_hammer') == 1
   
   def HasDrill(self):
      return self._ag.GetVar('item_drill') == 1
   
   def HasCannon(self):
      return self._ag.GetVar('item_cannon') == 1
   
   def HasCannonFire(self):
      return self._ag.GetVar('item_cannon_fire') == 1
   
   def HasCannonIce(self):
      return self._ag.GetVar('item_cannon_ice') == 1
   
   def HasCannonMulti(self):
      return self._ag.GetVar('item_cannon_multi') == 1
   
   def EquipA(self, val):
      return self._ag.SetSavedVar('equipped_a', val)
   
   def EquipB(self):
      return self._ag.SetSavedVar('equipped_b', val)
   
   def EquippedX(self, val):
      return self._ag.SetSavedVar('equipped_x', val)
   
   def EquipY(self, val):
      return self._ag.SetSavedVar('equipped_y', val)
      
   def Sabre(self):
      return 'item_sabre'
   def Hammer(self):
      return 'item_hammer'
   def Drill(self):
      return 'item_drill'
   def Cannon(self):
      return 'item_cannon'
   def CannonFire(self):
      return 'item_cannon_fire'
   def CannonIce(self):
      return 'item_cannon_ice'
   def CannonMulti(self):
      return 'item_cannon_multi'