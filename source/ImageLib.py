class ImageLibraryClass:
   def __init__(self):
      self._lib = {}
   
   def Add(self, name, path):
      if self._lib.get(name):
         print("ImageLibrary already loaded %s" % name)
         return True
      
      if not os.path.exists(path):
         return False
      surf = pygame.image.load(path)
      if surf:
         self._lib[name] = surf
         return True
      else:
         return False

   def Get(self, name):
      return self._lib.get(name)

### STATIC ###
ImageLib = ImageLibraryClass()