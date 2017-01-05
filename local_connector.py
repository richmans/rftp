import time
import os
import struct
import hashlib
from data_block import *

def checkUrl(url):
  return url.scheme == ""
  
class Writer:
  def __init__(self, url):
    self.path = url.path
    self.file = open(url.path, 'wb')
    self.md5 = hashlib.md5()
    self.offset = 0
    
  def putBlock(self, block):
    if block.offset != self.offset:
      raise Exception("Unexpected block with offset %d" % block.offset) 
    self.md5.update(block.data)
    self.checkHash(block.incrementalHash)
    self.file.write(block.data)
    self.offset += len(block.data)
  
  def checkHash(self, otherHash):
    if self.md5.hexdigest() != otherHash:
      raise Exception("File hash mismatch at offset %d" % self.offset)
    
class Reader:
  def __init__(self, url):
    self.path = url.path
    self.file = open(url.path, 'rb')
    self.offset = 0
    self.md5 = hashlib.md5()
    
  def getBlock(self):
    data = self.file.read(DataBlock.blockSize)
    if data == None or len(data) == 0:
      return None
    startOffset = self.offset
    self.offset += len(data)
    self.md5.update(data)
    incrementalHash = self.md5.hexdigest()
    return DataBlock(self.path, startOffset, data, incrementalHash)
  
  def hash(self):
    return self.md5.hexdigest()