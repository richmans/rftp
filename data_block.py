class DataBlock:
  blockSize = 512
  def __init__(self, path, offset, data, incrementalHash=None, filesize=0):
    self.path = path
    self.offset = offset
    self.data = data
    self.incrementalHash = incrementalHash
    self.filesize = filesize
    