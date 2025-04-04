from API.RequestSender import RequestSender
class GUI():
    def __init__(self,requestSender: 'RequestSender',mainWindow:'MainWindow'):

        #check if RequestSender is an instance of RequestSender
        if not isinstance(requestSender, RequestSender):
            raise ValueError("requestSender must be an instance of RequestSender")

        if mainWindow is None:
            raise ValueError("mainWindow must not be None")

        self.requestSender = requestSender
        self.mainWindow = mainWindow

    def start(self):
        self.mainWindow.root.mainloop()