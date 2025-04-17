import numpy as np
from API.shared.workpiece.Workpiece import BaseWorkpiece
from API.shared.interfaces.JsonSerializable import JsonSerializable
from API.shared.workpiece.Workpiece import WorkpieceField
from GlueDispensingApplication.tools.enums.Program import Program
from GlueDispensingApplication.tools.enums.ToolID import ToolID
from GlueDispensingApplication.tools.enums.GlueType import GlueType
from GlueDispensingApplication.tools.enums.Gripper import Gripper


class Workpiece(BaseWorkpiece, JsonSerializable):
    def __init__(self, workpieceId, name, description, toolID, gripperID, glueType, program, material, contour, offset,
                 height,
                 nozzles, contourArea, sprayPattern=None):
        if sprayPattern is None:
            sprayPattern = []
        self.workpieceId = workpieceId
        self.name = name
        self.description = description
        self.toolID = toolID
        self.gripperID = gripperID
        self.glueType = glueType
        self.program = program
        self.material = material
        self.contour = contour  # This should be a list of nd arrays
        self.offset = offset
        self.height = height
        self.sprayPattern = sprayPattern
        self.contourArea = contourArea
        self.nozzles = nozzles

    def __str__(self):
        return (f"Workpiece ID: {self.workpieceId} \n"
                f"   Name: {self.name}\n"
                f"   Description: {self.description}\n"
                f"   Spray Type: {self.toolID}\n"
                f"   Glue Type: {self.glueType}\n"
                f"   Program: {self.program}\n"
                f"   Tool ID: {self.toolID}\n"
                f"   Gripper ID: {self.gripperID}\n"
                f"   Material: {self.material}\n"
                f"   Offset: {self.offset}\n"
                f"   Height: {self.height}\n"
                f"   Nozzles: {self.nozzles}\n"
                f"   Area: {self.contourArea}\n")
                # f"   Spray Pattern: {{ Contour: {len(self.sprayPattern.get('Contour', []))}, Fill: {len(self.sprayPattern.get('Fill', []))} }}\n")


    def getFormattedDetails(self):
        return [
            f"ID: {self.workpieceId} ",
            f"Description: {self.description}",
            f"Program: {self.program}",
            f"Offset: {self.offset}",
            f"Height: {self.height} mm",
            f"Tool ID: {self.toolID}",
            f"Gripper ID: {self.gripperID}",
            f"Glue Type: {self.glueType}",
            f"Material: {self.material}",
            f"Area {self.contourArea} ",
            # f"Nozzles: {self.nozzles}"
        ]

    @staticmethod
    def serialize(workpiece):
        """
        Serialize the Workpiece object to a dictionary that can be converted to JSON.
        Ensure numpy arrays (such as contours) are converted to lists for JSON serialization.
        """

        def convert_ndarray_to_list(obj):
            """Helper function to convert ndarrays and lists of ndarrays to lists."""
            if isinstance(obj, np.ndarray):
                return obj.tolist()  # Convert ndarray to list
            elif isinstance(obj, list):
                return [convert_ndarray_to_list(item) for item in obj]  # Recursively convert elements in a list
            return obj

        def flatten_points(obj):
            """Helper function to flatten nested points to a consistent shape (N, 1, 2)."""
            if isinstance(obj, list) and len(obj) > 0 and isinstance(obj[0], list):
                flat_obj = [point[0] if isinstance(point[0], list) else point for point in obj]
                return flat_obj
            return obj

        # Apply the conversion for contour and sprayPattern

        # Debugging: Print the types of contour and sprayPattern
        print("Type of workpiece.contour:", type(workpiece.contour))
        print("Type of workpiece.sprayPattern:", type(workpiece.sprayPattern))
        print("Contour before serialization: ",workpiece.contour)
        contour_list = convert_ndarray_to_list(workpiece.contour)
        # if isinstance(workpiece.sprayPattern, np.ndarray):
        #     spray_pattern_list = workpiece.sprayPattern.tolist()
        # else:
        #     spray_pattern_list = flatten_points(workpiece.sprayPattern)
        if isinstance(workpiece.sprayPattern, dict):
            spray_pattern_dict = {
                key: convert_ndarray_to_list(val) for key, val in workpiece.sprayPattern.items()
            }
        else:
            spray_pattern_dict = flatten_points(workpiece.sprayPattern)

        workpiece.sprayPattern = spray_pattern_dict

        print("Serialized cnt and spray")
        workpiece.contour = contour_list
        # workpiece.sprayPattern = spray_pattern_list

        # Debugging: Print the types of contour and sprayPattern
        print("Type of workpiece.contour after serialization:", type(workpiece.contour))
        print("Type of workpiece.sprayPattern after serialization :", type(workpiece.sprayPattern))

        return workpiece.toDict()

    def deserialize(data):
        """
        Deserialize a dictionary back into a Workpiece object.
        """

        def convert_list_to_ndarray(obj):
            """Convert lists to numpy arrays with the correct shape."""
            if isinstance(obj, list) and len(obj) > 0 and isinstance(obj[0], list):
                arr = np.array(obj, dtype=np.float32)  # Convert list to NumPy array
                if arr.ndim == 2 and arr.shape[1] == 2:  # Ensure correct shape
                    return arr.reshape(-1, 1, 2)  # Reshape to (N, 1, 2)
                return arr
            return obj

        # Deserialize fields
        contour = convert_list_to_ndarray(data[WorkpieceField.CONTOUR.value])
        print("Contour after deserialization:", contour)

        # Spray pattern logic stays the same
        raw_spray_pattern = data.get(WorkpieceField.SPRAY_PATTERN.value, {})
        spray_pattern = {}
        if isinstance(raw_spray_pattern, dict):
            for key, pattern in raw_spray_pattern.items():
                spray_pattern[key] = Workpiece.reshape_spray_pattern(pattern)
        else:
            spray_pattern = raw_spray_pattern  # fallback

        workpiece = Workpiece.fromDict(data)
        workpiece.contour = contour
        workpiece.sprayPattern = spray_pattern

        return workpiece

    def toDict(self):
        return {
            WorkpieceField.WORKPIECE_ID.value: self.workpieceId,
            WorkpieceField.NAME.value: self.name,
            WorkpieceField.DESCRIPTION.value: self.description,
            WorkpieceField.TOOL_ID.value: self.toolID.value,
            WorkpieceField.GRIPPER_ID.value: self.gripperID.value,
            WorkpieceField.GLUE_TYPE.value: self.glueType.value,
            WorkpieceField.PROGRAM.value: self.program.value,
            WorkpieceField.MATERIAL.value: self.material,
            WorkpieceField.CONTOUR.value: self.contour,
            WorkpieceField.OFFSET.value: self.offset,
            WorkpieceField.HEIGHT.value: self.height,
            WorkpieceField.SPRAY_PATTERN.value: self.sprayPattern,
            WorkpieceField.CONTOUR_AREA.value: self.contourArea,
            WorkpieceField.NOZZLES.value: self.nozzles

        }

    @staticmethod
    def flatten_spray_pattern(obj):
        if isinstance(obj, list):
            flat_obj = []
            for item in obj:
                if isinstance(item, list):
                    flat_obj.extend(Workpiece.flatten_spray_pattern(item))
                else:
                    flat_obj.append(item)
            return flat_obj
        return [obj]

    @staticmethod
    def reshape_spray_pattern(obj):
        """
        Reshape spray pattern list into list of (N, 1, 2) numpy arrays.
        Handles multiple contours (lists of point lists).
        """
        if not obj:
            return []

        # If it's a single contour, flatten and reshape it
        if all(isinstance(pt, (list, np.ndarray)) and len(pt) == 2 for pt in obj):
            grouped = np.array(obj, dtype=np.float32).reshape(-1, 1, 2)
            return [grouped]

        # If it's a list of contours
        if isinstance(obj, list) and all(isinstance(c, list) for c in obj):
            result = []
            for contour in obj:
                if not contour:
                    continue
                flat = Workpiece.flatten_spray_pattern(contour)
                if all(isinstance(x, (int, float)) for x in flat):
                    grouped = [[flat[i], flat[i + 1]] for i in range(0, len(flat), 2)]
                elif all(isinstance(x, list) and len(x) == 2 for x in flat):
                    grouped = flat
                else:
                    raise ValueError(f"Invalid spray pattern shape: {flat}")
                result.append(np.array(grouped, dtype=np.float32).reshape(-1, 1, 2))
            return result

        raise ValueError(f"Unknown spray pattern format: {obj}")

    @staticmethod
    def fromDict(dict):

        return Workpiece(
            workpieceId=dict[WorkpieceField.WORKPIECE_ID.value],
            name=dict[WorkpieceField.NAME.value],
            description=dict[WorkpieceField.DESCRIPTION.value],
            toolID=ToolID(dict[WorkpieceField.TOOL_ID.value]),
            gripperID=Gripper(dict[WorkpieceField.GRIPPER_ID.value]),
            glueType=GlueType(dict[WorkpieceField.GLUE_TYPE.value]),
            program=Program(dict[WorkpieceField.PROGRAM.value]),
            material=dict[WorkpieceField.MATERIAL.value],
            contour=dict[WorkpieceField.CONTOUR.value],
            offset=dict[WorkpieceField.OFFSET.value],
            height=dict[WorkpieceField.HEIGHT.value],
            nozzles=dict.get(WorkpieceField.NOZZLES.value, []),  # Setting nozzles to empty list if missing
            contourArea=dict[WorkpieceField.CONTOUR_AREA.value],
            sprayPattern=dict.get(WorkpieceField.SPRAY_PATTERN.value, [])
            # Setting spray pattern to empty list if missing
        )
