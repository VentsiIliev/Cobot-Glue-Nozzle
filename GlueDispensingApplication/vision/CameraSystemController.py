from API import Constants
from API.Response import Response
import traceback
class CameraSystemController():
    def __init__(self,cameraService: 'CameraService'):
        self.cameraService = cameraService

    def handleGetRequest(self,request:'Request'):
        if request.action == Constants.CAMERA_ACTION_GET_LATEST_FRAME:
            try:
                frame = self.cameraService.getLatestFrame()
                if frame is None:
                    data = {"frame": None}
                else:
                    data = {"frame": frame}
                return Response(Constants.RESPONSE_STATUS_SUCCESS, message="Success", data=data).to_dict()
            except Exception as e:
                return Response(Constants.RESPONSE_STATUS_ERROR,
                                message=f"Error getting latest frame: {e}").to_dict()
        else:
            traceback.print_exc()  # This prints the full stack trace
            raise ValueError(f"Invalid request action: {request.action}")

    def handlePostRequest(self,request:'Request'):
        pass

    def handleExecuteRequest(self,request:'Request'):
        if request.action == Constants.CAMERA_ACTION_RAW_MODE_ON:
            self.cameraService.setRawMode(True)
            return Response(Constants.RESPONSE_STATUS_SUCCESS, message="Raw mode enabled").to_dict()

        if request.action == Constants.CAMERA_ACTION_RAW_MODE_OFF:
            self.cameraService.setRawMode(False)
            return Response(Constants.RESPONSE_STATUS_SUCCESS, message="Raw mode disabled").to_dict()

    def updateCameraSettings(self,settings:dict):
        return self.cameraService.updateSettings(settings)