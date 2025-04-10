from API import Constants
from API.Response import Response
from GlueDispensingApplication.robot.RobotWrapper import Direction, Axis
class RobotController():
    def __init__(self,robotService,robotCalibrationService):
        self.robotService = robotService
        self.robotCalibrationService = robotCalibrationService

    def handleGetRequest(self,request):
        pass

    def handlePostRequest(self,request):
        pass

    def handleExecuteRequest(self,request):
        action = request.action

        if action == Constants.ROBOT_ACTION_JOG_X_MINUS:
            step = request.data["step"]
            self.robotService.startJog(Axis.X, Direction.MINUS,step)

        elif action == Constants.ROBOT_ACTION_JOG_X_PLUS:
            step = request.data["step"]
            self.robotService.startJog(Axis.X, Direction.PLUS,step)

        elif action == Constants.ROBOT_ACTION_JOG_Y_MINUS:
            step = request.data["step"]
            self.robotService.startJog(Axis.Y, Direction.MINUS,step)

        elif action == Constants.ROBOT_ACTION_JOG_Y_PLUS:
            step = request.data["step"]
            self.robotService.startJog(Axis.Y, Direction.PLUS,step)

        elif action == Constants.ROBOT_ACTION_JOG_Z_MINUS:
            step = request.data["step"]
            self.robotService.startJog(Axis.Z, Direction.MINUS,step)

        elif action == Constants.ROBOT_ACTION_JOG_Z_PLUS:
            step = request.data["step"]
            self.robotService.startJog(Axis.Z, Direction.PLUS,step)

        elif action == Constants.REQUEST_ACTION_CURRENT_POSITION:
            self.robotService.getCurrentPosition()

        elif action == Constants.ROBOT_ACTION_SAVE_POINT:
            currentPos = self.robotService.getCurrentPosition()
            x,y,z = currentPos[0],currentPos[1],currentPos[2]
            self.robotCalibrationService.saveRobotPoint([x,y,z])
            pointsCount = self.robotCalibrationService.robotPointIndex

            if pointsCount==4:
                result,message = self.robotCalibrationService.calibrate()
                if result:
                    self.robotService.cameraToRobotMatrix = self.robotCalibrationService.cameraToRobotMatrix
                self.robotService.moveToStartPosition()
                response = Response(status=Constants.RESPONSE_STATUS_SUCCESS,
                                    message=message,
                                    data={"pointsCount":pointsCount})
                return response.to_dict()

            else:
                x,y,z=self.robotCalibrationService.getNextRobotPoint()
                nextPosition = [x,y,150,180,0,0]
                self.robotService.moveToPosition(nextPosition,0,0,100,30)
                nextPosition = [x, y, z, 180, 0, 0]
                self.robotService.moveToPosition(nextPosition, 0, 0, 100, 30)

            responce = Response(status=Constants.RESPONSE_STATUS_SUCCESS,
                                message="Point saved",
                                data={"pointsCount":pointsCount})

            return responce.to_dict()
        elif action == Constants.HOME_ROBOT:
            return self.robotService.moveToStartPosition()
        elif action == Constants.ACTION_STOP:
            self.robotService.stopRobot();
        else:
            raise ValueError(f"Invalid request action: {action}")
