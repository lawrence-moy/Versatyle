﻿import sys
if sys.version_info[0] < 3:
  from Queue import Queue
else:
  import queue
import web_service_requester
import threading
import time

class DataRetrievingManager(threading.Thread):
  def __init__(self, _parent):
    threading.Thread.__init__(self)
    self.service = None
    self.consumers = {}
    if sys.version_info[0] < 3:
      self.queue = Queue()
    else:
      self.queue = queue.Queue()
    self.parent = _parent
    self.exiting = False

  def init(self):
    pass
    
  def run(self):
    while False == self.exiting:
      while not self.queue.empty():
        moduleId, varName, value = self.queue.get()
        if None == self.consumers.get(moduleId):
          continue
        if None == self.consumers[moduleId].get(varName):
          continue  
        for consumer in self.consumers[moduleId].get(varName):
          consumer.setValue(value)
      time.sleep(0.05)

  def finish(self):
    self.service.stop()
    self.service.join()
    self.exiting = True
    
  def getQueue(self):
    return self.queue

  def registerConsumer(self, widget, moduleId, variableName):
    if None == self.consumers.get(moduleId):
      self.consumers[moduleId] = {}
    if None == self.consumers[moduleId].get(variableName):
      self.consumers[moduleId][variableName] = []
    print("register consumer: ", moduleId, variableName, widget)
    self.consumers[moduleId][variableName].append(widget)
    
  def parseXMLParameters(self, element):
    subDataRetrievingNode = element.firstChild()
    while not subDataRetrievingNode.isNull():
      serviceElement = subDataRetrievingNode.toElement()
      if not serviceElement.isNull():
        if "WebService" == serviceElement.tagName():
           url      = serviceElement.attribute("url", "")
           interval = float(serviceElement.attribute("interval", "1"))
           webService = web_service_requester.WebServiceRequester(self.queue,
                                                                  url, interval)
           webService.start()
           self.service = webService
      subDataRetrievingNode = subDataRetrievingNode.nextSibling()
    
  def getXMLConfiguration(self, doc):
    pass
    
  def newConfigEvent(self):
    self.parent.saveXMLConfiguration()
    
  def show(self):
    pass
    