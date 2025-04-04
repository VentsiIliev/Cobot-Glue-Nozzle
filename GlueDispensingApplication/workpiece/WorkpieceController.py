from API.shared.workpiece.WorkpieceService import WorkpieceService
from API import Constants
from GlueDispensingApplication.workpiece.Workpiece import Workpiece


class WorkpieceController():
    def __init__(self, workpieceService: 'WorkpieceService'):
        if not isinstance(workpieceService, WorkpieceService):
            raise ValueError("workpieceService must be an instance of WorkpieceService")
        self.workpieceService = workpieceService
        self.cacheInfo = {}
        self.scaleFactor = 1

    def handlePostRequest(self, request):
        print("request in workpiece controller", request)
        if request.action == Constants.ACTION_SAVE_WORKPIECE:
            print("data in workpiece controller", request.data)
            # add the chahced info to the data
            if self.cacheInfo:
                request.data.update(self.cacheInfo)
                self.cacheInfo = {}
                self.scaleFactor = 1
            workpiece = Workpiece.fromDict(request.data)
            return self.workpieceService.saveWorkpiece(workpiece)