from enum import Enum


class Mode(Enum):
    CONSTANT_FREQ = 1
    CONSTANT_DIST = 2
    PRINTER = 3
    SINGLE_DROPS = 4

    def getValue(self):
        return self.value