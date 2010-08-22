class ImageLibraryClass:
   def __init__(self):
      self._lib = {} # stores name -> path
      self._pathLib = {} # stores path -> surface
   
   def Add(self, name, path):
      if self._lib.get(name):
         print("ImageLibrary already loaded %s" % name)
         return FromFile(self._lib[name])
         
      surf = self.FromFile(path)
      if surf:
         self._lib[name] = path
         return surf
      return None
      

   def Get(self, name):
      p = self._lib.get(name)
      if p:
         return self.FromFile(p)
      return None
   
   def FromFile(self, path):
      surf = self._pathLib.get(path)
      if surf:
         return surf

      if not os.path.exists(path):
         print('Could not load %s' % path)
         return None
      
      surf = pygame.image.load(path)
      if surf:
         self._pathLib[path] = surf
         return surf
      else:
         print('Could not load %s' % path)
         return None

### STATIC ###
ImageLib = ImageLibraryClass()