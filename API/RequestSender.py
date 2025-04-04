from abc import ABC, abstractmethod

class RequestSender(ABC):
    @abstractmethod
    def sendRequest(self, request):
        pass