from enum import Enum


class GlueType(Enum):
    TypeA = "Type A"
    TypeB = "Type B"
    TypeC = "Type C"

    def __str__(self):
        """String representation of the enum value."""
        return self.value
