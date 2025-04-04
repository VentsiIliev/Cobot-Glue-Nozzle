from API.Request import Request
from API.Response import Response
from API import Constants
from API.shared.workpiece.Workpiece import WorkpieceField
from GlueDispensingApplication.utils import utils
import traceback
import numpy as np


class RequestHandler:
    def __init__(self, controller, settingsController, cameraSystemController, glueNozzleController, workpieceController, robotController):
        self.controller = controller
        self.settingsController = settingsController
        self.cameraSystemController = cameraSystemController
        self.glueNozzleController = glueNozzleController
        self.workpieceController = workpieceController
        self.robotController = robotController

    def handleRequest(self, request: dict):
        """
        Main request dispatcher.
        Routes requests based on their type and action.
        """
        request = Request.from_dict(request)

        if request.action != Constants.CAMERA_ACTION_GET_LATEST_FRAME:
            print(f"Handling request: {request}")

        handlers = {
            Constants.REQUEST_TYPE_GET: self.handleGetRequests,
            Constants.REQUEST_TYPE_POST: self.handlePostRequest,
            Constants.REQUEST_TYPE_EXECUTE: self.handleExecuteRequest,
        }

        if request.req_type in handlers:
            return handlers[request.req_type](request)
        else:
            raise ValueError(f"Invalid request type: {request.req_type}")

    def handleGetRequests(self, request):
        """
        Handles all GET requests.
        """
        if request.action == Constants.ACTION_GET_SETTINGS:
            print("Handling get settings request", request)
            return self.settingsController.handleGetRequest(request)

        if request.resource == Constants.REQUEST_RESOURCE_CAMERA:
            return self.cameraSystemController.handleGetRequest(request)

    def handlePostRequest(self, request):
        """
        Handles all POST requests.
        """
        if request.action == Constants.ACTION_SET_SETTINGS:
            return self.settingsController.handlePostRequest(request)

        if request.action == Constants.ACTION_SAVE_WORKPIECE:
            return self._handleSaveWorkpiece(request)

    def _handleSaveWorkpiece(self, request):
        """
        Prepares and transforms the spray pattern before saving a workpiece.
        """
        print("Processing workpiece save request", request)
        sprayPattern = request.data.get(WorkpieceField.SPRAY_PATTERN.value, [])

        if sprayPattern:
            sprayPattern = np.array(sprayPattern, dtype=np.float32).reshape(-1, 2)
            sprayPattern = [[[point[0], point[1]]] for point in sprayPattern]
            sprayPattern = utils.applyTransformation(
                self.cameraSystemController.cameraService.getCameraToRobotMatrix(), sprayPattern
            )

        request.data[WorkpieceField.SPRAY_PATTERN.value] = sprayPattern
        result =  self.workpieceController.handlePostRequest(request)

        if result:
            return Response(Constants.RESPONSE_STATUS_SUCCESS, message="Workpiece saved successfully").to_dict()
        else:
            return Response(Constants.RESPONSE_STATUS_ERROR, message="Error saving workpiece").to_dict()

    def handleExecuteRequest(self, request):
        """
        Handles all EXECUTE requests.
        """
        if request.resource == Constants.REQUEST_RESOURCE_GLUE_NOZZLE:
            return self.glueNozzleController.handleExecuteRequest(request)

        if request.resource == Constants.REQUEST_RESOURCE_ROBOT:
            return self._handleRobotRequests(request)

        if request.resource == Constants.REQUEST_RESOURCE_CAMERA:

            if request.action == Constants.ACTION_CALIBRATE:
                return self._handleCameraCalibration()

            return self.cameraSystemController.handleExecuteRequest(request)

        return self._handleGeneralExecutionRequests(request)

    def _handleRobotRequests(self, request):
        """
        Handles robot-related execution requests.
        """
        if request.action == Constants.ACTION_CALIBRATE:
            return self._handleRobotCalibration()

        if request.action == Constants.ROBOT_ACTION_SAVE_POINT:
            return self.robotController.handleExecuteRequest(request)

        return self.robotController.handleExecuteRequest(request)

    def _handleRobotCalibration(self):
        """
        Handles robot calibration request.
        """

        try:
            result,message, image = self.controller.calibrateRobot()
            if result:
                return Response(Constants.RESPONSE_STATUS_SUCCESS, message=message, data={"image": image}).to_dict()
            else:
                return Response(Constants.RESPONSE_STATUS_ERROR, message=message).to_dict()
        except Exception as e:
            print(f"Error calibrating robot: {e}")
            return Response(Constants.RESPONSE_STATUS_ERROR, message=f"Error calibrating robot: {e}").to_dict()

    def _handleGeneralExecutionRequests(self, request):
        """
        Handles general execution requests like start, calibrate, and create workpiece.
        """
        action_handlers = {
            Constants.ACTION_START: self._handleStart,
            # Constants.ACTION_CALIBRATE: self._handleCameraCalibration,

            Constants.ACTION_CREATE_WORKPIECE: self._handleCreateWorkpiece
        }

        handler = action_handlers.get(request.action)
        return handler() if handler else Response(Constants.RESPONSE_STATUS_ERROR, message="Invalid action").to_dict()

    def _handleStart(self):
        """
        Handles the Start action.
        """
        try:

            result,message = self.controller.start()
            print("Result: ", result)
            if not result:
                return Response(Constants.RESPONSE_STATUS_ERROR, message=message).to_dict()
            else:
                return Response(Constants.RESPONSE_STATUS_SUCCESS, message=message).to_dict()
        except Exception as e:
            traceback.print_exc()
            return Response(Constants.RESPONSE_STATUS_ERROR, message=f"Error starting: {e}").to_dict()

    def _handleCameraCalibration(self):
        """
        Handles the Camera Calibration action.
        """
        try:
            result, message = self.controller.calibrateCamera()
            status = Constants.RESPONSE_STATUS_SUCCESS if result else Constants.RESPONSE_STATUS_ERROR
            return Response(status, message=message).to_dict()
        except Exception as e:
            return Response(Constants.RESPONSE_STATUS_ERROR, message=e).to_dict()

    def _handleCreateWorkpiece(self):
        """
        Handles the Create Workpiece action.
        """
        try:
            result,height, contourArea, contour, scaleFactor, image,message = self.controller.createWorkpiece()
            if not result:
                return Response(Constants.RESPONSE_STATUS_ERROR, message=message).to_dict()

            # Temporary workaround: force height to 4
            print("before comparison Height:", height)
            if height is None:
                height = 4
            if height < 4 or height > 4:
                height = 4

            # Cache data in the workpiece controller
            self.workpieceController.cacheInfo = {
                WorkpieceField.HEIGHT.value: height,
                WorkpieceField.CONTOUR_AREA.value: contourArea,
                WorkpieceField.CONTOUR.value: contour
            }
            self.workpieceController.scaleFactor = scaleFactor

            dataDict = {WorkpieceField.HEIGHT.value: height, "image": image}
            return Response(Constants.RESPONSE_STATUS_SUCCESS, message=message, data=dataDict).to_dict()
        except Exception as e:
            return Response(Constants.RESPONSE_STATUS_ERROR, message=f"Uncaught exception: {e}").to_dict()
