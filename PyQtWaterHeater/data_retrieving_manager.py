﻿from PySide import QtCore
import web_service_requester

class DataRetrievingManager(QtCore.QObject):
  def __init__(self, _parent):
    QtCore.QObject.__init__(self, parent=_parent)
    self.service = None

  def init(self):
    pass
    
  def finish(self):
    self.service.stop()
    if not self.service.wait(3000):
      self.service.terminate()
      self.service.wait()
    
  def parseXMLParameters(self, element):
    subDataRetrievingNode = element.firstChild()
    while not subDataRetrievingNode.isNull():
      serviceElement = subDataRetrievingNode.toElement()
      if not serviceElement.isNull():
        if "WebService" == serviceElement.tagName():
           url      = serviceElement.attribute("url", "")
           interval = float(serviceElement.attribute("interval", "1"))
           webService = web_service_requester.WebServiceRequester(self, url, interval)
           webService.start()
           self.service = webService
      subDataRetrievingNode = subDataRetrievingNode.nextSibling()
    
  def getXMLConfiguration(self, doc):
    pass
    
  def newConfigEvent(self):
    self.parent().saveXMLConfiguration()
    
  def show(self):
    pass
    