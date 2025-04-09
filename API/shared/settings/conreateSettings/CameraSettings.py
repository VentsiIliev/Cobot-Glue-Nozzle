from API.shared.settings.BaseSettings import Settings
from API.shared.settings.conreateSettings.enums.CameraSettingKey import CameraSettingKey



class CameraSettings(Settings):
    def __init__(self, data: dict = None):
        super().__init__()
        # Initialize default camera settings using the Enum
        self.set_value(CameraSettingKey.INDEX.value, 1)
        self.set_value(CameraSettingKey.WIDTH.value, 1280)
        self.set_value(CameraSettingKey.HEIGHT.value, 720)
        self.set_value(CameraSettingKey.SKIP_FRAMES.value, 30)
        self.set_value(CameraSettingKey.THRESHOLD.value, 128)
        self.set_value(CameraSettingKey.EPSILON.value, 0.004)
        self.set_value(CameraSettingKey.CONTOUR_DETECTION.value, True)
        self.set_value(CameraSettingKey.DRAW_CONTOURS.value, True)

        # Update settings with provided data
        if data:
            for key, value in data.items():
                self.set_value(key, value)

    def set_camera_index(self, index):
        """Set the camera index."""
        self.set_value(CameraSettingKey.INDEX.value, index)

    def get_camera_index(self):
        """Get the camera index."""
        return self.get_value(CameraSettingKey.INDEX.value)

    def get_camera_width(self):
        """Get the camera width."""
        return self.get_value(CameraSettingKey.WIDTH.value)

    def get_camera_height(self):
        """Get the camera height."""
        return self.get_value(CameraSettingKey.HEIGHT.value)

    def set_resolution(self, width, height):
        """Set the camera resolution."""
        self.set_value(CameraSettingKey.WIDTH.value, width)
        self.set_value(CameraSettingKey.HEIGHT.value, height)

    def set_width(self, width):
        """Set the camera width."""
        self.set_value(CameraSettingKey.WIDTH.value, width)

    def set_height(self, height):
        """Set the camera height."""
        self.set_value(CameraSettingKey.HEIGHT.value, height)

    def get_resolution(self):
        """Get the camera resolution."""
        return (self.get_value(CameraSettingKey.WIDTH.value), self.get_value(CameraSettingKey.HEIGHT.value))

    def get_skip_frames(self):
        """Get the number of frames to skip."""
        return self.get_value(CameraSettingKey.SKIP_FRAMES.value)

    def set_skip_frames(self, skipFrames):
        """Set the number of frames to skip."""
        self.set_value(CameraSettingKey.SKIP_FRAMES.value, skipFrames)

    def get_threshold(self):
        """Get the threshold value."""
        return self.get_value(CameraSettingKey.THRESHOLD.value)

    def set_threshold(self, threshold):
        """Set the threshold value."""
        self.set_value(CameraSettingKey.THRESHOLD.value, threshold)

    def get_epsilon(self):
        """Get the epsilon value."""
        return self.get_value(CameraSettingKey.EPSILON.value)

    def set_epsilon(self, epsilon):
        """Set the epsilon value."""
        self.set_value(CameraSettingKey.EPSILON.value, epsilon)

    def get_contour_detection(self):
        """Get the contour detection status."""
        return self.get_value(CameraSettingKey.CONTOUR_DETECTION.value)

    def set_contour_detection(self, contourDetection):
        """Set the contour detection status."""
        self.set_value(CameraSettingKey.CONTOUR_DETECTION.value, contourDetection)

    def get_draw_contours(self):
        """Get the draw contours status."""
        return self.get_value(CameraSettingKey.DRAW_CONTOURS.value)

    def set_draw_contours(self, drawContours):
        """Set the draw contours status."""
        self.set_value(CameraSettingKey.DRAW_CONTOURS.value, drawContours)

    def display_settings(self):
        """Utility method to display the camera settings."""
        index = self.get_camera_index()
        width, height = self.get_resolution()
        skipFrames = self.get_skip_frames()
        threshold = self.get_threshold()
        epsilon = self.get_epsilon()
        contourDetection = self.get_contour_detection()
        drawContours = self.get_draw_contours()

        print(f"Camera Index: {index}")
        print(f"Resolution: {width}x{height}")
        print(f"Skip Frames: {skipFrames}")
        print(f"Threshold: {threshold}")
        print(f"Epsilon: {epsilon}")
        print(f"Contour Detection: {contourDetection}")
        print(f"Draw Contours: {drawContours}")

    def __str__(self):
        return (
            f"CameraSettings:\n"
            f"  Index: {self.get_camera_index()}\n"
            f"  Resolution: {self.get_camera_width()}x{self.get_camera_height()}\n"
            f"  Skip Frames: {self.get_skip_frames()}\n"
            f"  Threshold: {self.get_threshold()}\n"
            f"  Epsilon: {self.get_epsilon()}\n"
            f"  Contour Detection: {self.get_contour_detection()}\n"
            f"  Draw Contours: {self.get_draw_contours()}"
        )
