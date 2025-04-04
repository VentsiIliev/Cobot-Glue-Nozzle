from GlueDispensingApplication.workpiece.Workpiece import Workpiece
from GlueDispensingApplication.workpiece.WorkPieceRepositorySingleton import WorkPieceRepositorySingleton

class WorkpieceService:
    DATE_FORMAT = "%Y-%m-%d"
    TIMESTAMP_FORMAT = "%Y-%m-%d_%H-%M-%S-%f"
    BASE_DIR = "GlueDispensingApplication/storage/workpieces"
    WORKPIECE_FILE_SUFFIX = "_workpiece.json"

    def __init__(self):
        self.repository = WorkPieceRepositorySingleton().get_instance()

    def saveWorkpiece(self, workpiece: Workpiece):
        return self.repository.saveWorkpiece(workpiece)

    def loadAllWorkpieces(self):
        data = self.repository.data
        return data