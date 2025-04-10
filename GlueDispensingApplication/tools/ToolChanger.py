from GlueDispensingApplication.tools.enums.Gripper import Gripper
class ToolChanger():
    STATUS_AVAILABLE = -1
    STATUS_OCCUPIED = 0

    def __init__(self):
        # Initialize slots with position and occupancy status (0: empty, 1: occupied)
        self.slots = {
            10: {"position": [-405.203,549.522, 130, 180, 0, 0], "occupied": self.STATUS_OCCUPIED,"reservedFor": Gripper.SINGLE},
            11: {"position": [-403.73, 564.799, 126.4, 180, 0, 5], "occupied": self.STATUS_AVAILABLE,"reservedFor": Gripper.MOCK},
            12: {"position": [-406.73, 638.915, 129.1, 180, 0, 5], "occupied": self.STATUS_AVAILABLE,"reservedFor": Gripper.MOCK2},
            13: {"position": [-416.544, 775.733, 135, 180, 0, 2], "occupied": self.STATUS_AVAILABLE,"reservedFor": Gripper.MOCK3},
            14: {"position": [-412.905, 792.998, 128.469, 180, 0, 8.5], "occupied": self.STATUS_OCCUPIED,"reservedFor": Gripper.DOUBLE},
        }

    def getSlotPosition(self, slotId):
        """Returns the position of the specified slot."""
        return self.slots[slotId]["position"]

    def _setSlotOccupied(self, slotId, status):
        print("Slot ID: ", slotId)
        print("Status: ", status)
        """Sets the slot as occupied (1) or empty (0)."""
        if slotId in self.slots and status in [-1, 0]:
            self.slots[slotId]["occupied"] = status
        else:
            raise ValueError("Invalid slot ID or status. Use -1 or 0.")

    def setSlotNotAvailable(self, slotId):
        """Sets the slot as not available (1)."""
        self._setSlotOccupied(slotId, self.STATUS_OCCUPIED)

    def setSlotAvailable(self, slotId):
        """Sets the slot as available (0)."""
        self._setSlotOccupied(slotId, self.STATUS_AVAILABLE)

    def isSlotOccupied(self, slotId):
        """Checks if a slot is occupied."""
        print("Slot ID: ", slotId)
        taken = self.slots[slotId]["occupied"] == self.STATUS_OCCUPIED
        print("Occupied: ", taken)
        return taken

    def getOccupiedSlots(self):
        """Returns a list of occupied slot IDs."""
        return [slot for slot, data in self.slots.items() if data["occupied"] == self.STATUS_OCCUPIED]

    def getEmptySlots(self):
        """Returns a list of empty slot IDs."""
        return [slot for slot, data in self.slots.items() if data["occupied"] == self.STATUS_AVAILABLE]

    def getReservedFor(self,slotId):
        return self.slots[slotId]["reservedFor"]

    def isSlotReserved(self,slotId):
        return self.slots[slotId]["reservedFor"] != None

    def getSlotToolMap(self):
        """MAP REPRESENTING THE ARUCO MARKERS IDS FOR SLOT AND TOOL"""
        map = {
            10: 0,
            11: 1,
            12: 2,
            13: 3,
            14: 4
        }
        return map

    def getSlotIds(self):
        return list(self.slots.keys())

    def getReservedForIds(self):
        return [int(data["reservedFor"].value) for slot, data in self.slots.items()]

    def getSlotIdByGrippedId(self, gripperId):
        print("Gripper ID: ", gripperId)
        for slot, data in self.slots.items():
            if int(data["reservedFor"].value) == gripperId:
                return slot


