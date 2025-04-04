from GUI import GUI
from MqttRequestSender import MqttRequestSender
from SocketSender import SocketSender
from SharedMemorySender import SharedMemorySender
from DomesticRequestSender import DomesticRequestSender
from RequestHandler import RequestHandler
# Създаваме инстанции на различните бекенд изпращачи
mqttRequestSender = MqttRequestSender()  # MQTT комуникация

socketSender = SocketSender()  # Комуникация чрез сокети

sharedMemorySender = SharedMemorySender()  # Комуникация чрез споделена памет

# В случай че GUI и бакенд са написани на един и същ програмен език може да се използва директно обекта от RequestHandler като зависимост на DomesticRequestSender
rquestHandler = RequestHandler() # Зависимост на DomesticRequestSender
domesticRequestSender = DomesticRequestSender(requestHandler=rquestHandler)

# Създаваме GUI и подаваме SharedMemorySender като бекенд изпращач
gui = GUI(sharedMemorySender)

# Изпращаме заявка чрез GUI
print("Sending request via Shared Memory")
gui.sendRequest("Hello")