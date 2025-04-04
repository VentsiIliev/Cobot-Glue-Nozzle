from API.RequestSender import RequestSender

class DomesticRequestSender(RequestSender):
    def __init__(self,requestHandler):
      self.requestHandler = requestHandler

    def sendRequest(self, reques):
        return self.requestHandler.handleRequest(reques)
