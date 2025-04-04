from API.RequestSender import RequestSender

class MqttRequestSender(RequestSender):
    def __init__(self):
      pass

    def sendRequest(self, request):
        print(f"Request sent via MQTT: {request}")