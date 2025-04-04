from API.shared.workpiece.Workpiece import  WorkpieceField
from GlueDispensingApplication.workpiece.WorkPieceRepositorySingleton import WorkPieceRepositorySingleton

fields = [WorkpieceField.WORKPIECE_ID, WorkpieceField.NAME, WorkpieceField.DESCRIPTION, WorkpieceField.TOOL_ID,
          WorkpieceField.GLUE_TYPE, WorkpieceField.PROGRAM, WorkpieceField.MATERIAL, WorkpieceField.CONTOUR,
          WorkpieceField.OFFSET, WorkpieceField.HEIGHT, WorkpieceField.SPRAY_PATTERN, WorkpieceField.CONTOUR_AREA,
          WorkpieceField.NOZZLES]

repo = WorkPieceRepositorySingleton.get_instance()
data = repo.loadData()
print(len(data))
#
# workpiece = Workpiece(1, "Test", "Test", ToolID.Tool1, GlueType.TypeA, Program.TRACE, "Test", [1, 2, 3], 1, 1, [1, 2, 3], 1, [1, 2, 3])
# repo.saveWorkpiece(workpiece)

print(data)