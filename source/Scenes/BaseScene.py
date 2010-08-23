class BaseScene:
   def __init__(self):
      self.next = self
   
   def ProcessInput(self, events):
      pass
   
   def Update(self, conter):
      pass
   
   def Render(self, screen):
      pass
   