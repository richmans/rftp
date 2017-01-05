class DataBlock:
  blockSize = 512
  def __init__(self, path, offset, data, incrementalHash=None):
    self.path = path
    self.offset = offset
    self.data = data
    self.incrementalHash = incrementalHash
    

