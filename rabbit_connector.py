import time
import os
import struct
import pip
from data_block import *
try:
  import pika
except:
  pip.main(['install', "pika"])
  import pika

def checkUrl(url):
  return url.scheme == "rftp"
      
class RabbitConnection:
  def __init__(self, config):
    self.config = config
    
  def start(self):
    try:
      credentials = pika.PlainCredentials(self.config.rabbitUser, self.config.rabbitPassword)
      self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                     self.config.rabbitHost,
                     5672,
                     self.config.rabbitVirtualHost,
                     credentials))
      self.channel = self.connection.channel()
      self.channel.queue_declare(queue=self.config.rabbitQueue)
    except Exception as e:
      return False
    self.started = True
    return True
  

class Reader:
  def __init__(self, config):
    self.config = config
    self.connection = RabbitConnection(config)

  def getBlock(self):
    _, properties, data = self.channel.basic_get(self.config.rabbitQueue, no_ack=True)
    offset = properties.headers["offset"]
    path = properties.headers["path"]
    incrementalHash = properties.headers["hash"]
    if data == None: return None
    return Block(path, offset, data, incrementalHash)
    
class Writer:
  def __init__(self, config):
    self.config = config
    self.connection = RabbitConnection(config)
    
  def putBlock(self, block):
    properties = pika.BasicProperties(
      headers={'path': block.path, 
               'offset': block.offset, 
               'hash': block.incrementalHash
               } 
    )
    self.channel.basic_publish(exchange=self.config.rabbitExchange,
                              routing_key=self.config.rabbitRoutingKey,
                              properties=properties,
                              body=block.data)
                        