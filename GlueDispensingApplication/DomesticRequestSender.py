from API.RequestSender import RequestSender
from API.Request import Request
from GlueDispensingApplication.RequestHandler import RequestHandler
class DomesticRequestSender(RequestSender):
    def __init__(self,requestHandler: RequestHandler):
      self.requestHandler = requestHandler

    def sendRequest(self, request:Request):
        return self.requestHandler.handleRequest(request.to_dict())
