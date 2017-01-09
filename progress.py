import time
import threading
import sys
class ProgressMeter(threading.Thread):
  def __init__(self, reader):
    threading.Thread.__init__(self)
    self.reader = reader  
    self.done = False

  def stop(self):
    self.done = True
    self.join()
    
  def run(self):
    while self.done == False:
      time.sleep(0.5)
      self.progress()
      
  #http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
  def progress(self):
    bar_len = 60
    total = self.reader.filesize
    if total == None: return
    count = self.reader.offset
    
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s\r' % (bar, percents, '%'))
    sys.stdout.flush()  # As suggested by Rom Ruben
