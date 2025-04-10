import math
import time
from tkinter import messagebox

import cv2
import numpy as np
from src.plvision.PLVision import Contouring

from GlueDispensingApplication.tools.GlueNozzleService import GlueNozzleService

from GlueDispensingApplication.tools.enums import ToolID
from GlueDispensingApplication.tools.enums.ToolID import ToolID
from GlueDispensingApplication.tools.enums.Gripper import Gripper
from GlueDispensingApplication.tools.nozzles.Tool1 import Tool1
from GlueDispensingApplication.tools.VacuumPump import VacuumPump
from GlueDispensingApplication.tools.nozzles.Tool2 import Tool2
from GlueDispensingApplication.tools.nozzles.Tool3 import Tool3
from GlueDispensingApplication.utils import utils
from GlueDispensingApplication.robot import RobotUtils
from GlueDispensingApplication.tools.ToolChanger import ToolChanger

from API.shared.settings.conreateSettings.RobotSettings import RobotSettingKey
from API.shared.Contour import Contour


class RobotService:
    MIN_Z_VALUE = 250
    RX_VALUE = 180
    RY_VALUE = 0
    RZ_VALUE = 0  # TODO: Change to 0

    TOOL_DEFAULT = 0  # Default tool ID
    USER_DEFAULT = 0  # Default user ID

    def __init__(self, robot, settingsService, glueNozzleService: GlueNozzleService = None):
        self.robot = robot
        self.robot.printSdkVerison()
        self.pump = VacuumPump()
        # TODO: FINISH IMPLEMENTATION FOR ROBOT SETTINGS
        self.settingsService = settingsService
        self.robotSettings = self.settingsService.robot_settings

        self.glueNozzleService = glueNozzleService
        self.startPosition = [-4.36, 421.145, 757.939, 180, 0, 0]
        self.debugPath = []
        self.currentGripper = None
        self.toolChanger = ToolChanger()

    def getMotionParams(self):
        robotMotionParams = (self.robotSettings.get_robot_velocity(),
                             self.robotSettings.get_robot_tool(),
                             self.robotSettings.get_robot_user(),
                             self.robotSettings.get_robot_acceleration(),
                             1)
        return robotMotionParams

    def zigZag(self, contour, spacing, direction):
        path = RobotUtils.zigZag(contour, spacing, direction)
        return path

    def moveToStartPosition(self):
        try:
            if not self.robot:
                messagebox.showwarning("Warning", "Robot not connected.")
                return

            startPosition = [-4.36, 421.145, 757.939, 180, 0, 0]

            ret = self.robot.moveCart(startPosition, self.TOOL_DEFAULT, self.USER_DEFAULT, vel=100, acc=30)
            print("Moving to start: ", ret)
        except Exception as e:
            print("Error moving to start position:", e)
            messagebox.showerror("Error", f"Error moving to start position: {e}")

    def traceContours(self, contours, height, toolID=None):
        print(" Tracing contours")
        requiredSprayingHeight, toolTip = self.__getTool(toolID)
        threshold = 5
        height = self.pump.zOffset + height + requiredSprayingHeight
        try:
            if not self.robot:
                messagebox.showwarning("        Warning", "Robot not connected.")
                return

            if toolTip == None:
                xOffset = 0
                yOffset = 0
            else:
                xOffset = toolTip.xOffset
                yOffset = toolTip.yOffset

            print("     xOffset: ", xOffset, "yOffset: ", yOffset)
            robotPaths = []
            for cnt in contours:

                path = []
                for point in cnt:
                    point = point[0]
                    path.append((point[0] + xOffset, point[1] + yOffset,
                                 height, self.RX_VALUE, self.RY_VALUE, self.RZ_VALUE))
                    self.debugPath.append((point[0] + xOffset, point[1] + yOffset,
                                           height, self.RX_VALUE, self.RY_VALUE, self.RZ_VALUE))
                robotPaths.append(path)

            velocity, tool, workpiece, acceleration, blendR = self.getMotionParams()

            print("     Path = ", robotPaths)
            # startPoint = robotPaths[0][0]

            # speed_thread = threading.Thread(target=self.query_speed, args=())
            # speed_thread.daemon = True
            # speed_thread.start()

            for path in robotPaths:
                startPoint = path[0]
                print("     Start point: ", startPoint)
                self.robot.moveCart(startPoint, tool, workpiece, vel=velocity, acc=acceleration)
                self._waitForRobotToReachPosition(startPoint, threshold=threshold,
                                                  delay=0)  # TODO comment out when using test robot

                if isinstance(toolTip, Tool1):
                    self.pump.turnOn(self.robot)
                elif isinstance(toolTip, Tool2):
                    self.glueNozzleService.startGlueDotsDispensing()
                    # pass
                elif isinstance(toolTip, Tool3):
                    self.pump.turnOn(self.robot)

                self.executePathWithMoveL(acceleration, blendR, path, tool, velocity, workpiece)

                endPoint = path[-1]
                print("     End point: ", endPoint)
                self._waitForRobotToReachPosition(endPoint, threshold=5,
                                                  delay=0.5)  # TODO comment out when using test robot

                if isinstance(toolTip, Tool1):
                    self.pump.turnOff(self.robot)
                elif isinstance(toolTip, Tool2):
                    self.glueNozzleService.stopGlueDispensing()
                    pass
                elif isinstance(toolTip, Tool3):
                    self.pump.turnOff(self.robot)

            # # write self.debugPath to txt file
            # with open('points.txt', 'w') as f:
            #     for point in self.debugPath:
            #         f.write(str(point) + "\n")

        except Exception as e:
            raise Exception(e)

    def __getTool(self, toolID):
        if toolID == ToolID.Tool1:
            return 25, Tool1()
        elif toolID == ToolID.Tool2:
            return 25, Tool2()
        elif toolID == ToolID.Tool3:
            return 25, Tool3()
        elif toolID == ToolID.Tool0:
            return 25,None
        else:
            raise ValueError("Invalid tool ID")

    def _waitForRobotToReachPosition(self, endPoint, threshold, delay):
        while True:
            time.sleep(delay)
            print("     Waiting for robot to reach end point")
            currentPos = self.robot.getCurrentPosition()
            print("     Current position: ", currentPos[0], currentPos[1], currentPos[2])
            currentPos[0] = currentPos[0]
            currentPos[1] = currentPos[1]
            if abs(currentPos[0] - endPoint[0]) < threshold and abs(
                    currentPos[1] - endPoint[1]) < threshold and abs(currentPos[2] - endPoint[2]) < threshold:
                break

    def getCurrentPosition(self):
        return self.robot.getCurrentPosition()

    def query_speed(self):
        while True:
            ret = self.robot.getCurrentLinierSpeed()
            currentSpeed = ret[1][0]

    def executePathWithMoveL(self, acceleration, blendR, robotPath, tool, velocity, workpiece):
        count = 1
        print("Robot Path:", robotPath)
        for point in robotPath:
            # speed_thread = threading.Thread(target=query_speed, args=(robot,))
            # speed_thread.daemon = True
            # speed_thread.start()
            if count == 1:
                count = 0
                continue

            ret = self.robot.moveL(point, tool, workpiece, vel=velocity, acc=acceleration, blendR=blendR)
        # stop thread
        # speed_thread.join()

    def __getNestingMoves(self, angle, centroid, dropOffPositionX, dropOffPositionY, height):
        print("performPickAndPlaceMovement height: ", height)
        xOffset = 50
        yOffset = 50
        theta = math.radians(angle)
        # Apply 2D rotation matrix
        newXOffset = xOffset * math.cos(theta) - yOffset * math.sin(theta)
        newYOffset = xOffset * math.sin(theta) + yOffset * math.cos(theta)
        print("NewX: ", newXOffset, "NewY: ", newYOffset)

        x = centroid[0] + newXOffset
        y = centroid[1] + newYOffset

        # Step 1: Pick up the workpiece
        path = []

        path.append([x, y, self.MIN_Z_VALUE +30,
                     self.RX_VALUE, self.RY_VALUE, self.RZ_VALUE])

        # Step 2: Move down to the workpiece with the correct orientation angle
        path.append([x, y, height-1+6,
                     self.RX_VALUE, self.RY_VALUE, angle])

        # Step 3 pick up the workpiece
        path.append([x, y, self.MIN_Z_VALUE + 30,
                     self.RX_VALUE, self.RY_VALUE, self.RZ_VALUE])

        # Step 4: Move to drop-off location
        path.append([dropOffPositionX + xOffset, dropOffPositionY + yOffset, height + 30,
                     self.RX_VALUE, self.RY_VALUE, self.RZ_VALUE])

        return path

    def enableRobot(self):
        self.robot.enable()
        print("Robot enabled")

    def disableRobot(self):
        self.robot.disable()
        print("Robot disabled")

    def moveToPosition(self, position, tool, workpiece, velocity, acceleration, waitToReachPosition=False):
        self.robot.moveCart(position, tool, workpiece, vel=velocity, acc=acceleration)

        if waitToReachPosition:  # TODO comment out when using test robot
            self._waitForRobotToReachPosition(position, 1, delay=0.1)

        # self.robot.moveL(position, tool, workpiece, vel=velocity, acc=acceleration,blendR=20)

    def moveToHeightMeasurePosition(self, centroid, motionParams):
        position = [centroid[0], centroid[1] - 75, 300, self.RX_VALUE, self.RY_VALUE, self.RZ_VALUE]
        print("Moving to height measurement position", position)
        self.moveToPosition(position, motionParams[1], motionParams[2], motionParams[0], motionParams[3])

    def _isValid(self, contour):
        """Check if the contour is valid."""
        return contour is not None and len(contour) > 0


    def __executeNestingTrajectory(self,grippers,paths):
        velocity, tool, workpiece, acceleration, blendR = self.getMotionParams()
        for gripperId, path in zip(grippers, paths):
            """CHECK IF GRIPPER CHANGE IS NECESSARY"""
            print("Path: ", path)
            print("Gripper: ", gripperId)
            print("Current gripper: ", self.currentGripper)
            print(f"Type of gripperId: {type(gripperId)}, Type of self.currentGripper: {type(self.currentGripper)}")

            if self.currentGripper != gripperId:
                if self.currentGripper != None:
                    result, message = self.dropOffGripper(self.currentGripper)
                    if not result:
                        return False, message

                result, message = self.pickupGripper(gripperId)
                if not result:
                    return False, message

            """MOVE ROBOT ALONG PATH TO PICK AND PLACE WORKPIECE"""
            self.pump.turnOn(self.robot)
            for point in path:
                self.robot.moveCart(point, tool, workpiece, vel=velocity, acc=40)
            self.pump.turnOff(self.robot)

    def nestingNew(self, workpieces,callback=None):
        if callback is not None:
            validationPos = [-350, 650, 450, 180, 0, 90]
            self.moveToPosition(validationPos, 0, 0, 100, 30, waitToReachPosition=True)
            callback()

        grippers = [] # List of grippers
        paths = [] # List of pick and place paths
        count = 0 # Workpiece counter
        rowCount = 0 # Row counter

        xMin = -250 # Minimum x value for nesting work area
        xMax = 400 # Maximum x value for nesting work area
        yMax = 600 # Maximum y value for nesting work area
        yMin = 250 # Minimum y value for nesting work area
        spacing = 30 # Spacing between workpieces

        xOffset = 0 # Offset for the next workpiece
        yOffset = 0 # Offset for the next row
        higherContour = 0 # Highest contour height in the row

        for item in workpieces:
            """ADD WORKPIECE GRIPPER TO GRIPPERS LIST"""
            grippers.append(int(item.gripperID.value))

            """GET NESTING POSITION FOR WORKPIECE"""
            print("COUNT: ",count)
            cnt = item.contour
            cntObject = Contour(cnt) # Create Contour object

            """ROTATE CONTOUR TO ALIGN WITH THE X-AXIS"""
            angle = cntObject.getOrientation()
            centroid = cntObject.getCentroid()
            cntObject.rotate(-angle, centroid)

            """GET MINIMUM AREA RECTANGLE OF THE CONTOUR"""
            minRect = cntObject.getMinAreaRect()
            box = cv2.boxPoints(minRect)
            box = np.intp(box)

            """GET BOUNDING BOX CENTER AND DIMENSIONS"""
            bboxCenter = (minRect[0][0], minRect[0][1])

            width = minRect[1][1]
            height = minRect[1][0]
            print(" bboxWidth: ", width)
            print(" bboxHeight: ", height)

            """UPDATE HIGHEST CONTOUR HEIGHT ( IT IS USED FOR ROW SPACING)"""
            if height > higherContour:
                higherContour = height

            """GET TARGET POINT FOR PLACING THE WORKPIECE"""
            targetPointX = xOffset + xMin + (width / 2)
            targetPointY = yMax -yOffset
            print(f"    Target point: ({targetPointX}, {targetPointY}")

            """MOVE TO NEXT ROW IF THE CONTOUR EXCEEDS THE CANVAS WIDTH"""
            if targetPointX + (width / 2) > xMax:
                print(" The contour exceeds the canvas width. Moving to the next row.")

                rowCount += 1  # Increment row counter
                xOffset = 0  # Reset xOffset for the new row
                yOffset += higherContour + 50  # Use only the tallest contour + fixed spacing

                targetPointX = xMin + (width / 2)  # Reset to the left
                targetPointY = yMax - yOffset  # Move down
                print(" Target point after moving to the next row:", targetPointX, targetPointY)

                # Reset the row's tallest contour tracking
                higherContour = height

                """CHECK IF THE CONTOUR EXCEEDS THE CANVAS HEIGHT"""
                if targetPointY - (height / 2) < yMin:
                    print(" The contour exceeds the canvas height.")
                    break

            print(f"    bboxCenter: {bboxCenter}")
            count += 1

            """TRANSLATE THE CONTOUR TO THE TARGET POINT"""
            cntObject.translate(targetPointX - bboxCenter[0], targetPointY - bboxCenter[1])
            translated = cntObject.get_contour_points()

            """GET THE TRANSLATED CONTOUR CENTER"""
            newCentroid = cntObject.getCentroid()
            print(f"    New centroid: {newCentroid}")

            """"UPDATE THE xOffset FOR THE NEXT CONTOUR"""
            xOffset += width + spacing  # Add horizontal spacing between contours

            """ADD PICK AND PLACE PATH TO PATHS LIST"""
            moveHeight = self.pump.zOffset + item.height
            path = self.__getNestingMoves(angle, centroid, newCentroid[0], newCentroid[1], moveHeight)
            paths.append(path)
            print(f"    Path: ",path)

        """EXECUTE NESTING TRAJECTORY"""
        self.__executeNestingTrajectory(grippers,paths)

        return True, None



    def pickupGripper(self, gripperId, callBack=None):

        slotId = self.toolChanger.getSlotIdByGrippedId(gripperId)

        if not self.toolChanger.isSlotOccupied(slotId):
            message = f"Slot {slotId} is empty"
            print(message)
            return False, message

        slotPosition = self.toolChanger.getSlotPosition(slotId)
        self.toolChanger.setSlotAvailable(slotId)

        x, y, z, rx, ry, rz = slotPosition
        pos1 = [x, y, z + 100, rx, ry, rz]
        pos2 = [x, y, z, rx, ry, rz]
        pos3 = [x + 150, y, z, rx, ry, rz]

        path = [pos1, pos2, pos3]
        print("pickUp path: ", path)

        for point in path:
            self.robot.moveL(point, 0, 0, 100, 30, 0)
        self.currentGripper = slotId-10

        return True, None

    def dropOffGripper(self, slotId, callBack=None):
        slotId = int(slotId)

        print("Drop off gripper: ", slotId)
        if self.toolChanger.isSlotOccupied(slotId):
            message = f"Slot {slotId} is taken"
            print(message)
            return False, message

        slotPosition = self.toolChanger.getSlotPosition(slotId)
        self.toolChanger.setSlotNotAvailable(slotId)

        x, y, z, rx, ry, rz = slotPosition
        pos1 = [x + 150, y, z, rx, ry, rz]
        pos2 = [x, y, z, rx, ry, rz]
        pos3 = [x, y, z + 100, rx, ry, rz]

        path = [pos1, pos2, pos3]
        print("dropOff path: ", path)

        for point in path:
            self.robot.moveL(point, 0, 0, 100, 30, 0)
        self.currentGripper = None

        return True, None

    def startJog(self, axis, direction, step):
        self.robot.startJog(axis, direction, step, vel=50, acc=30)

    def stopRobot(self):
        self.robot.stopMotion()

