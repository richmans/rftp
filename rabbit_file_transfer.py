import urllib.parse
import rabbit_connector
import local_connector

class RabbitFileTransfer:
  def __init__(self):
    self.modules = []
    self.registerModules()

  def registerModules(self):
    self.registerModule(rabbit_connector)
    self.registerModule(local_connector)

  def registerModule(self, module):
    self.modules.append(module)
  
  def findModule(self, url):
    for module in self.modules:
      if module.checkUrl(url):
        return module
    return None
    
  def getReader(self, url): 
    url = urllib.parse.urlsplit(url)
    module = self.findModule(url)
    if module == None: 
      return None
    else:
      return module.Reader(url)
    
  
  def getWriter(self, url):
    url = urllib.parse.urlsplit(url)
    module = self.findModule(url)
    if module == None: 
      return None
    else:
      return module.Writer(url)




