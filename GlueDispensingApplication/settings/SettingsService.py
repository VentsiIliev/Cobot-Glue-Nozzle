import json
import os

from API.shared.settings.conreateSettings.RobotSettings import RobotSettings
from API.shared.settings.conreateSettings.CameraSettings import CameraSettings
from API import Constants
from API.shared.settings.conreateSettings.enums.CameraSettingKey import CameraSettingKey
from API.shared.settings.conreateSettings.enums.RobotSettingKey import RobotSettingKey


class SettingsService:
    settings_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "storage", "settings")
    settings_dir = os.path.normpath(settings_dir)  # Normalize path to avoid issues

    settings_file_paths = {
        "camera": os.path.join(settings_dir, "camera_settings.json"),
        "robot_settings": os.path.join(settings_dir, "robot_settings.json"),
    }

    def __init__(self):
        # Initialize a dictionary to store settings objects
        self.settings_objects = {}

        # Initialize and load settings for each component
        self.camera_settings = CameraSettings()
        self.robot_settings = RobotSettings()

        # Store them in the settings dictionary
        self.settings_objects["camera"] = self.camera_settings
        self.settings_objects["robot_settings"] = self.robot_settings

        # Load settings from JSON files, or use default values if files do not exist
        self.load_all_settings()

    def set_camera_index(self, index):
        self.camera_settings.set_camera_index(index)

    def set_camera_width(self, width):
        self.camera_settings.set_width(width)

    def set_camera_height(self, height):
        self.camera_settings.set_height(height)

    def get_camera_index(self):
        return self.camera_settings.get_camera_index()

    def get_camera_width(self):
        return self.camera_settings.get_camera_width()

    def get_camera_height(self):
        return self.camera_settings.get_camera_height()

    def get_camera_settings(self):
        """Retrieve the camera settings object."""
        return self.camera_settings

    def getSettings(self, key):
        """Retrieve a settings object by key."""
        if key == Constants.REQUEST_RESOURCE_CAMERA:
            data = self.camera_settings.toDict()
            print("from Settings Service: ", data)
            return data
        elif key == Constants.REQUEST_RESOURCE_ROBOT:
            return self.robot_settings.toDict()

    def save_all_settings(self):
        """Save all settings to their respective files."""
        for key, settings_obj in self.settings_objects.items():
            filename = self.settings_file_paths.get(key)
            if filename:
                self.save_settings_to_json(filename, settings_obj)

    def load_all_settings(self):
        """Load all settings from their respective JSON files. Use default values if file doesn't exist."""
        for key, settings_obj in self.settings_objects.items():
            filename = self.settings_file_paths.get(key)
            if filename and os.path.exists(filename):
                self.load_settings_from_json(filename, settings_obj)
            else:
                print(f"{filename} not found. Using default values for {key} settings.")
                # Automatically save default settings to the missing file
                self.save_settings_to_json(filename, settings_obj)

    def display_all_settings(self):
        """Utility function to display all settings in the manager."""
        for key, settings_obj in self.settings_objects.items():
            print(f"Settings for {key}:")
            settings_obj.display_settings()
            print()

    def load_settings_from_json(self, json_file, settings_obj):
        """Load settings from a JSON file and update the settings object."""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                settings_data = json.load(f)

                print(f"Settings loaded from {json_file} Settings: {settings_data}.")
            if isinstance(settings_obj, CameraSettings):
                settings_obj.set_camera_index(settings_data.get(CameraSettingKey.INDEX.value, 1))
                settings_obj.set_resolution(settings_data.get(CameraSettingKey.WIDTH.value, 1280),
                                            settings_data.get(CameraSettingKey.HEIGHT.value, 720))
                settings_obj.set_skip_frames(settings_data.get(CameraSettingKey.SKIP_FRAMES.value, 30))
                settings_obj.set_threshold(settings_data.get(CameraSettingKey.THRESHOLD.value, 128))
                settings_obj.set_epsilon(settings_data.get(CameraSettingKey.EPSILON.value, 0.004))
                settings_obj.set_contour_detection(settings_data.get(CameraSettingKey.CONTOUR_DETECTION.value, True))
                settings_obj.set_draw_contours(settings_data.get(CameraSettingKey.DRAW_CONTOURS.value, True))
            elif isinstance(settings_obj, RobotSettings):
                settings_obj.set_robot_ip(settings_data.get(RobotSettingKey.IP_ADDRESS.value, "192.168.58.2"))
                settings_obj.set_robot_velocity(settings_data.get(RobotSettingKey.VELOCITY.value, 100))
                settings_obj.set_robot_acceleration(settings_data.get(RobotSettingKey.ACCELERATION.value, 30))
                settings_obj.set_robot_tool(settings_data.get(RobotSettingKey.TOOL.value, 0))
                settings_obj.set_robot_user(settings_data.get(RobotSettingKey.USER.value, 0))


        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading settings from {json_file}: {e}")
            print(f"Using default values for {type(settings_obj).__name__}.")

    def save_settings_to_json(self, json_file, settings_obj):
        """Save the settings object to a JSON file."""
        try:
            # Create the settings directory if it doesn't exist
            os.makedirs(self.settings_dir, exist_ok=True)

            settings_data = {}
            if isinstance(settings_obj, CameraSettings):
                settings_data = {
                    CameraSettingKey.INDEX.value: settings_obj.get_camera_index(),
                    CameraSettingKey.WIDTH.value: settings_obj.get_camera_width(),
                    CameraSettingKey.HEIGHT.value: settings_obj.get_camera_height(),
                    CameraSettingKey.SKIP_FRAMES.value: settings_obj.get_skip_frames(),
                    CameraSettingKey.THRESHOLD.value: settings_obj.get_threshold(),
                    CameraSettingKey.EPSILON.value: settings_obj.get_epsilon(),
                    CameraSettingKey.CONTOUR_DETECTION.value: settings_obj.get_contour_detection(),
                    CameraSettingKey.DRAW_CONTOURS.value: settings_obj.get_draw_contours()
                }
            elif isinstance(settings_obj, RobotSettings):
                settings_data = {
                    RobotSettingKey.IP_ADDRESS.value: settings_obj.get_robot_ip(),
                    RobotSettingKey.VELOCITY.value: settings_obj.get_robot_velocity(),
                    RobotSettingKey.ACCELERATION.value: settings_obj.get_robot_acceleration(),
                    RobotSettingKey.TOOL.value: settings_obj.get_robot_tool(),
                    RobotSettingKey.USER.value: settings_obj.get_robot_user()
                }

            with open(json_file, 'w') as f:
                json.dump(settings_data, f, indent=4)

            print(f"Settings saved to {json_file}.")

        except Exception as e:
            print(f"Error saving settings to {json_file}: {e}")

    def updateSettings(self, settings: dict):
        header = settings['header']

        if header == "Robot":
            self.updateRobotSettings(settings)
        elif header == "Camera":
            self.updateCameraSettings(settings)
        else:
            raise ValueError("Invalid header")

    def updateRobotSettings(self, settings: dict):
        self.robot_settings.set_robot_ip(settings.get(RobotSettingKey.IP_ADDRESS.value))
        self.robot_settings.set_robot_velocity(settings.get(RobotSettingKey.VELOCITY.value))
        self.robot_settings.set_robot_acceleration(settings.get(RobotSettingKey.ACCELERATION.value))
        self.robot_settings.set_robot_tool(settings.get(RobotSettingKey.TOOL.value))
        self.robot_settings.set_robot_user(settings.get(RobotSettingKey.USER.value))
        self.save_settings_to_json(self.settings_file_paths.get("robot_settings"), self.robot_settings)

    def updateCameraSettings(self, settings: dict):
        self.camera_settings.set_camera_index(settings.get(CameraSettingKey.INDEX.value))
        self.camera_settings.set_width(settings.get(CameraSettingKey.WIDTH.value))
        self.camera_settings.set_height(settings.get(CameraSettingKey.HEIGHT.value))
        self.camera_settings.set_skip_frames(settings.get(CameraSettingKey.SKIP_FRAMES.value))
        self.camera_settings.set_threshold(settings.get(CameraSettingKey.THRESHOLD.value))
        self.camera_settings.set_epsilon(settings.get(CameraSettingKey.EPSILON.value))
        self.camera_settings.set_contour_detection(settings.get(CameraSettingKey.CONTOUR_DETECTION.value))
        self.camera_settings.set_draw_contours(settings.get(CameraSettingKey.DRAW_CONTOURS.value))
        self.save_settings_to_json(self.settings_file_paths.get("camera"), self.camera_settings)
