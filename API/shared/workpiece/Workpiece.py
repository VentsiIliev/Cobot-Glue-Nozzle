from enum import Enum
from abc import ABC, abstractmethod
import numpy as np
from API.shared.interfaces.JsonSerializable import JsonSerializable


class WorkpieceField(Enum):
    WORKPIECE_ID = "workpieceId"
    NAME = "name"
    DESCRIPTION = "description"
    TOOL_ID = "toolId"
    GRIPPER_ID = "gripperId"
    GLUE_TYPE = "glueType"
    PROGRAM = "program"
    MATERIAL = "material"
    CONTOUR = "contour"
    OFFSET = "offset"
    HEIGHT = "height"
    SPRAY_PATTERN = "sprayPattern"
    CONTOUR_AREA = "contourArea"
    NOZZLES = "nozzles"

    def getAsLabel(self):
        return self.name.capitalize().replace("_", " ")

    def lower(self):
        return self.value.lower()

class AbstractWorkpiece(ABC):
    def __init__(self, workpieceId, contour):
        if not workpieceId:
            raise ValueError("Workpiece ID must be provided")
        self.workpieceId = workpieceId

    @abstractmethod
    def __eq__(self, other):
        pass


class BaseWorkpiece(AbstractWorkpiece):
    def __init__(self, workpieceId, contour):
        super().__init__(workpieceId, contour)

    def __eq__(self, other):
        return self.workpieceId == other.workpieceId
