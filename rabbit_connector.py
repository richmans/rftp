import string
import time
import os
import struct
import pip
import random
from data_block import *

try:
  import pika
except:
  pip.main(['install', "pika"])
  import pika

rabbitExchange = "files"
class Config:
  def __init__(self):
    self.data = {}

  def __getattr__(self, attr):
    if attr in self.__dict__ or attr in ['data']:
      return super().__getattr__(attr)
    elif attr in self.data:
      return self.data[attr]
    return None
    
  def __setattr__(self, attr, value):
    if attr in self.__dict__ or attr in ['data']:
      return super().__setattr__(attr, value)
    else:
      self.data[attr] = value
      
def checkUrl(url):
  return url.scheme == "rftp"

def parseUrl(url):
  config = Config()
  config.rabbitUser = url.username
  config.rabbitPassword = url.password
  config.rabbitQueue = url.path[1:]
  config.rabbitHost = url.hostname
  config.rabbitVirtualHost= "/"
  config.rabbitExchange = rabbitExchange
  return config
  
class RabbitConnection:
  def __init__(self, config):
    self.config = config
    self.start()
    
  def start(self):
    try:
      credentials = pika.PlainCredentials(self.config.rabbitUser, self.config.rabbitPassword)
      self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                     self.config.rabbitHost,
                     5672,
                     self.config.rabbitVirtualHost,
                     credentials))
      self.channel = self.connection.channel()
    except Exception as e:
      print("Rabbit connection failure %s" % str(e))
      return False
    self.started = True
    return True

  def close(self):
    self.connection.close()
  

class Reader:
  def __init__(self, url):
    self.config = parseUrl(url)
    self.connection = RabbitConnection(self.config)
    self.config.rabbitQueue = self.createQueue()
    self.startupComplete = False
    self.offset = 0
    self.filesize = -1
    
  def createQueue(self):
    chars = string.ascii_uppercase + string.digits
    size = 6
    queueName = ''.join(random.choice(chars) for _ in range(size))
    self.connection.channel.queue_declare(queueName, auto_delete=True)
    self.connection.channel.queue_bind(queueName, self.config.rabbitExchange, queueName)
    return queueName

  def getBlock(self):
    if self.startupComplete == False:
      print("Waiting for data on queue %s. You can now start the sender!" % self.config.rabbitQueue)
      self.startupComplete = True
    if self.filesize > 0 and self.offset >= self.filesize:
      #EOF
      return None
      
    data = None
    _, properties, data = self.connection.channel.basic_get(self.config.rabbitQueue, no_ack=True)
    while data == None:
      _, properties, data = self.connection.channel.basic_get(self.config.rabbitQueue, no_ack=True)
      time.sleep(0.1)
    
    offset = properties.headers["offset"]
    path = properties.headers["path"]
    self.filesize = properties.headers["filesize"]
    incrementalHash = properties.headers["hash"]
    
    self.offset = offset + len(data)
    
    return DataBlock(path, offset, data, incrementalHash, self.filesize)
  
  def close(self):
    self.connection.channel.queue_delete(self.config.rabbitQueue)
    self.connection.close()
      
class Writer:
  def __init__(self, url):
    self.config = parseUrl(url)
    self.connection = RabbitConnection(self.config)
    
  def putBlock(self, block):
    properties = pika.BasicProperties(
      headers={'path': block.path, 
               'offset': block.offset, 
               'hash': block.incrementalHash,
               'filesize': block.filesize
               } 
    )
    self.connection.channel.basic_publish(exchange=self.config.rabbitExchange,
                              routing_key=self.config.rabbitQueue,
                              properties=properties,
                              body=block.data)
  def close(self):
    self.connection.close()
                          