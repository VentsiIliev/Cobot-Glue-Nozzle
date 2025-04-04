from API.RequestSender import RequestSender
class GUI():
    def __init__(self,requestSender: RequestSender):

        #check if RequestSender is an instance of RequestSender
        if not isinstance(requestSender, RequestSender):
            raise ValueError("requestSender must be an instance of RequestSender")

        self.requestSender = requestSender

    def sendRequest(self, request):
        self.requestSender.sendRequest(request)
