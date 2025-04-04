from API.RequestSender import RequestSender
class SharedMemorySender(RequestSender):
    def __init__(self):
        pass

    def sendRequest(self, request):
        print(f"Request sent to shared memory: {request}")