# from API.shared.database.repositories.WorkPieceRepository import WorkPieceRepository
from API.shared.workpiece.WorkpieceJsonRepository import WorkpieceJsonRepository
from API.shared.workpiece.Workpiece import  WorkpieceField
from GlueDispensingApplication.workpiece.Workpiece import Workpiece
class WorkPieceRepositorySingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            dir = "GlueDispensingApplication/storage"
            fields = [WorkpieceField.WORKPIECE_ID, WorkpieceField.NAME, WorkpieceField.DESCRIPTION,
                      WorkpieceField.TOOL_ID,WorkpieceField.GRIPPER_ID,
                      WorkpieceField.GLUE_TYPE, WorkpieceField.PROGRAM, WorkpieceField.MATERIAL, WorkpieceField.CONTOUR,
                      WorkpieceField.OFFSET, WorkpieceField.HEIGHT, WorkpieceField.SPRAY_PATTERN,
                      WorkpieceField.CONTOUR_AREA,
                      WorkpieceField.NOZZLES]
            cls._instance = WorkpieceJsonRepository(dir,fields,Workpiece)
        return cls._instance