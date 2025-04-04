from enum import Enum
class CameraSettingKey(Enum):
    INDEX = "Index"
    WIDTH = "Width"
    HEIGHT = "Height"
    SKIP_FRAMES = "Skip frames"
    THRESHOLD = "Threshold"
    EPSILON = "Epsilon"
    CONTOUR_DETECTION = "Contour detection"
    DRAW_CONTOURS = "Draw contours"

    def getAsLabel(self):
        return self.value + ":"