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
        if request.action == Constants.ACTION_SAVE_WORKPIECE or request.action == Constants.ACTION_SAVE_WORKPIECE_DXF:
            print("data in workpiece controller", request.data)
            # add the chahced info to the data
            print("before if")
            if self.cacheInfo:
                print("IN IF")
                request.data.update(self.cacheInfo)
                self.cacheInfo = {}
                self.scaleFactor = 1
            print("New DATA: ",request.data)
            workpiece = Workpiece.fromDict(request.data)
            print("WP: ",workpiece)
            return self.workpieceService.saveWorkpiece(workpiece)