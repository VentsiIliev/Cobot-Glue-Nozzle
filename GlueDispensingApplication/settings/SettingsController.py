from GlueDispensingApplication.vision.VisionService import VisionServiceSingleton
from GlueDispensingApplication.settings.SettingsService import SettingsService
from API.Request import Request
from API.Response import Response
from API import Constants
import traceback
class SettingsController():
    def __init__(self,settingsService: SettingsService):
        self.settingsService = settingsService

    def handleGetRequest(self, request:Request):
        if request.action == Constants.ACTION_GET_SETTINGS:
            if request.resource is None or request.resource == "":
                raise ValueError(f"Invalid request {request.to_dict()}")

            print("request.resource",request.resource)
            data = self.settingsService.getSettings(request.resource)
            print("data in settings controller",data)

            if data is not None:
                return Response(Constants.RESPONSE_STATUS_SUCCESS, message="Success", data=data).to_dict()
            else:
                return Response(Constants.RESPONSE_STATUS_ERROR, message="Error getting settings").to_dict()

    def handlePostRequest(self,request:Request):
        if request.resource is None or request.resource == "":
            raise ValueError(f"Invalid request {request.to_dict()}")

        if request.data is None or request.data == {}:
            raise ValueError(f"Invalid request {request.to_dict()}")

        try:
            self.settingsService.updateSettings(request.data)
            if request.resource == Constants.REQUEST_RESOURCE_CAMERA:
                result, message = VisionServiceSingleton().get_instance().updateCameraSettings(request.data)
                if result:
                    return Response(Constants.RESPONSE_STATUS_SUCCESS, message="Settings saved successfully").to_dict()
                else:
                    return Response(Constants.RESPONSE_STATUS_ERROR, message=f"Error saving settings: {message}").to_dict()

            return Response(Constants.RESPONSE_STATUS_SUCCESS, message="Settings saved successfully").to_dict()


        except Exception as e:
            traceback.print_exc()  # This prints the full stack trace
            return Response(Constants.RESPONSE_STATUS_ERROR, message=f"Uncaught exception: {e}").to_dict()