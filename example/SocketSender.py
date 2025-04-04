from API.RequestSender import RequestSender

class SocketSender(RequestSender):
    def __init__(self):
      pass

    def sendRequest(self, request):
        print(f"Request sent via Socket: {request}")