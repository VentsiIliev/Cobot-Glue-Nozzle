import threading
from tkinter import messagebox
import cv2
import numpy as np
import traceback
import time

from GlueDispensingApplication.settings.SettingsService import SettingsService

from src.plvision.PLVision import Contouring

from API.shared.workpiece.WorkpieceService import WorkpieceService
from GlueDispensingApplication.utils import Teaching
from GlueDispensingApplication import CompareContours
from GlueDispensingApplication.tools.Laser import Laser
from GlueDispensingApplication.robot.RobotService import RobotService
from GlueDispensingApplication.tools.enums.Program import Program
from GlueDispensingApplication.tools.enums.ToolID import ToolID
from GlueDispensingApplication import Initializations
from GlueDispensingApplication.vision.VisionService import VisionServiceSingleton
from GlueDispensingApplication.utils import utils
from GlueDispensingApplication.tools.GlueNozzleService import GlueNozzleService
from GlueDispensingApplication.robot.RobotCalibrationService import RobotCalibrationService
from API.shared.Contour import Contour

"""
ENDPOINTS
- start
- measureHeight
- calibrateRobot
- calibrateCamera
- createWorkpiece

"""


class GlueSprayingApplication:
    """
    ActionManager is responsible for connecting actions to functions.
    The MainWindow will just emit signals, and ActionManager handles them.
    """

    MAX_QUEUE_SIZE = 1  # Define the maximum number of frames to keep in the queue
    WORK_AREA_WIDTH = 750  # Width of the work area in mm
    WORK_AREA_HEIGHT = 500  # Height of the work area in mm

    def __init__(self, callbackFunction, visionService: VisionServiceSingleton, settingsManager: SettingsService,
                 glueNozzleService: GlueNozzleService, workpieceService: WorkpieceService,
                 robotService: RobotService, robotCalibrationService: RobotCalibrationService):
        super().__init__()

        self.settingsManager = settingsManager
        self.visionService = visionService
        self.glueNozzleService = glueNozzleService
        self.workpieceService = workpieceService
        self.robotService = robotService
        self.robotService.moveToStartPosition()

        # self.robotService.startExecutionThreads()

        self.robotCalibService = robotCalibrationService

        # Start the camera feed in a separate thread
        self.cameraThread = threading.Thread(target=self.visionService.run, daemon=True)
        self.cameraThread.start()

        self.callbackFunction = callbackFunction

        self.ppmX = self.visionService.getFrameWidth() / self.WORK_AREA_WIDTH  # Pixels per millimeter in x direction
        self.ppmY = self.visionService.getFrameHeight() / self.WORK_AREA_HEIGHT  # Pixels per millimeter in

    # Action functions
    def start(self, contourMatching=True):

        if contourMatching is True:
            workpieces = self.workpieceService.loadAllWorkpieces()

            result, newContours = self.visionService.processContours()

            if not result:
                return result, "No contours found"

            matches, noMatches, _ = CompareContours.findMatchingWorkpieces(workpieces, newContours)
            print("Matches: ", matches)

            if noMatches is not None and len(noMatches) > 0:
                message = "Unknown workpiece found!"
                print(message)

            if matches is None or len(matches) == 0:
                message = f"No matching workpiece found!\nDo you want to teach the new workpiece?"
                print(message)
                return False, message

            self.robotService.cleanNozzle()

            try:
                result, message = self.robotService.nestingNew(matches, self.updateToolChangerStation)
                if not result:
                    self.robotService.moveToStartPosition()
                    return result, message
            except:
                traceback.print_exc()

            self.robotService.moveToStartPosition()

            time.sleep(2)

            result, newContours = self.visionService.processContours()
            if not result:
                return result, "No contours found"

            matches, noMatches, _ = CompareContours.findMatchingWorkpieces(workpieces, newContours)

            if matches is None or len(matches) == 0:
                message = f"No matching workpiece found!"
                print("New contours2: ", len(newContours))
                print("New contours2: ", newContours)
                print(message)
                return False, message

            finalData = []
            for match in matches:
                program = match.program
                if match.sprayPattern is None or len(match.sprayPattern) <= 0:
                    contour = match.contour
                    # cntObject = Contour(contour)
                    # cntObject.shrink(5, 5)
                    # contour = cntObject.get_contour_points()
                    # contour = cntObject.simplify(0.004)  # Simplify the contour to remove redundant points
                    contour = contour.tolist()
                    contour.append(contour[0])
                    print("Contour: ",contour)
                else:
                    finalContourList = []

                    contourList = match.sprayPattern.get("Contour")
                    if len(contourList) > 0:
                        finalContourList = contourList

                    filList = match.sprayPattern.get("Fill")
                    if len(filList) > 0:
                        for fill in filList:
                            cnt = self.robotService.zigZag(fill,1,"horizontal")
                            finalContourList.append(fill)



                    # print("SprayPattern = ",contour)
                    # transformed = utils.applyTransformation(self.visionService.cameraToRobotMatrix,
                    #                                     [contour])

                # Perform robot motion depending on the program type
                if program == Program.ZIGZAG:
                    contour = np.array(contour, dtype=np.float32)  # Ensure the points array is of type CV_32F
                    contour = self.robotService.zigZag(contour, 10, "horizontal")
                    # self.robotService.traceContours([contour], match.height, match.toolID)
                    data = [contour], match.height, match.toolID
                    finalData.append(data)
                elif program == Program.TRACE:
                    data = contourList, match.height, match.toolID
                    finalData.append(data)
                    # self.robotService.traceContours([contour], match.height,match.toolID)
                else:
                    raise ValueError(f"Unknown program: {program}")

            # self.robotService.cleanNozzle()
            for d in finalData:
                self.robotService.traceContours(d[0], d[1], d[2])

        else:

            result, newContours = self.visionService.processContours()
            # newListContours = []

            # for cnt in newContours:
            #     cntObject = Contour(cnt)
            #     cntObject.shrink(5, 5)
            #     contour = cntObject.simplify(0.004)
            #     contour = contour.tolist()
            #     contour.append(contour[0])
            #     newListContours.append(contour)
            #     # cnt = contour

            self.robotService.traceContours(newContours, height=4, toolID=ToolID.Tool0)

        self.robotService.moveToStartPosition()
        return True, "Success"

    def measureHeight(self, frame, maxAttempts=1, debug=False):
        attempts = 0
        estimatedHeight = None
        laserTracker = Initializations.initLaserTracker()
        while estimatedHeight is None and attempts < maxAttempts:
            estimatedHeight = laserTracker.run(frame)
            frame = self.visionService.captureImage()
            attempts += 1

        if debug:
            if estimatedHeight is not None:
                cv2.putText(frame, f"Estimated height: {estimatedHeight:.2f} mm", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Height estimation failed", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2)

        return estimatedHeight

    def calibrateRobot(self):
        print("Calibrating robot")
        message = ""
        maxAttempts = 30
        while maxAttempts > 0:
            print("Aruco Attempt: ", maxAttempts)
            arucoCorners, arucoIds, image = self.visionService.detectArucoMarkers()
            print("ids: ", arucoIds)
            # cv2.imwrite(f"aruco{maxAttempts}.png", image)
            if arucoIds is not None and len(arucoIds) >= 3:
                break  # Stop retrying if enough markers are detected
            maxAttempts -= 1

        # convert image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if arucoIds is None or len(arucoIds) == 0:
            print("No ArUco markers found")
            message = "No ArUco markers found"
            return False, message, image

        # Dictionary to store corners for each ID
        id_to_corners = {}

        # Store corners in dictionary
        for i, aruco_id in enumerate(arucoIds.flatten()):
            id_to_corners[aruco_id] = arucoCorners[i][0]  # Store all 4 corners of this ID

        # Ensure we have all 4 required IDs
        # required_ids = {4, 5, 6, 7}
        required_ids = {2, 3, 4, 5, 6, 7, 8, 10, 12, 14}
        if not required_ids.issubset(id_to_corners.keys()):
            message = "Missing ArUco markers"
            return False, message, image

        # # Assign corners based on IDs
        # top_left = id_to_corners[4][0]  # First corner of ID 4
        # top_right = id_to_corners[5][0]  # First corner of ID 5
        # bottom_right = id_to_corners[6][0]  # First corner of ID 6
        # bottom_left = id_to_corners[7][0]  # First corner of ID 7

        # Assign corners based on IDs
        marker2 = id_to_corners[2][0]  # First corner of ID 2
        marker3 = id_to_corners[3][0]   # First corner of ID 3
        marker4 = id_to_corners[4][0]  # First corner of ID 4
        marker5 = id_to_corners[5][0]  # First corner of ID 5
        marker6 = id_to_corners[6][0]  # First corner of ID 6
        marker7 = id_to_corners[7][0]  # First corner of ID 7
        marker8 = id_to_corners[8][0]  # First corner of ID 8
        marker10 = id_to_corners[10][0]  # First corner of ID 10
        marker12 = id_to_corners[12][0]  # First corner of ID 12
        marker14 = id_to_corners[14][0]  # First corner of ID 14
        # marker16 = id_to_corners[16][0]  # First corner of ID 16


        # Ordered marker points
        # orderedMarkers = [top_left, top_right, bottom_right, bottom_left]
        orderedMarkers = [marker2,marker3,marker4,marker5,marker6,marker7,marker8,marker10,marker12,marker14]
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]  # Red, Green, Blue, Yellow
        labels = [4, 5, 6, 7]  # ArUco IDs

        # Draw markers on the image with different colors
        # for i, (point, color, label) in enumerate(zip(orderedMarkers, colors, labels)):
        #     cv2.circle(image, (int(point[0]), int(point[1])), 8, color, -1)  # Larger circle for visibility

        print(f"Assigned corners: {orderedMarkers}")

        # Send to robot calibration service
        self.robotCalibService.setCameraPoints(orderedMarkers)

        if self.robotCalibService.getRobotPoints() is not None and len(self.robotCalibService.getRobotPoints()) == 10:
            x, y, z = self.robotCalibService.getRobotPoints()[0]
            position = [x, y, z, 180, 0, 0]
            self.robotService.moveToPosition(position, 0, 0, 100, 30)
            position = [x, y, z, 180, 0, 0]
            self.robotService.moveToPosition(position, 0, 0, 100, 30)

        message = "Calibration successful"
        return True, message, image

    def calibrateCamera(self):
        self.robotService.moveToStartPosition()
        self.visionService.setRawMode(True)
        result = self.visionService.calibrateCamera()
        self.visionService.setRawMode(False)
        return result

    def createWorkpiece(self):

        result, contours = self.visionService.processContours()
        if not result:
            return result, "No contours found"

        contour = contours[0]
        contour.append(contour[0])
        contour = np.array(contour, dtype=np.float32)  # Convert to numpy array with correct data type
        centroid = Contouring.calculateCentroid(contour)
        contourArea = cv2.contourArea(contour)
        createWpImage = self.visionService.captureImage()

        """MEASURE HEIGHT"""
        laserController = Laser()
        laserController.turnOn()

        initialX = self.robotService.startPosition[0]
        initialY = self.robotService.startPosition[1]
        image = self.visionService.captureImage()

        cameraToRobotMatrix = self.visionService.getCameraToRobotMatrix()
        imageCenter = (image.shape[1] // 2, image.shape[0] // 2)
        offsets = Teaching.calculateTcpToImageCenterOffsets(imageCenter, initialX, initialY,
                                                            cameraToRobotMatrix)

        position = [centroid[0], centroid[1] + offsets[1], 300, 180, 0, 0]
        self.robotService.moveToPosition(position, 0, 0, 100, 30, waitToReachPosition=True)

        time.sleep(1)

        # capture new frame fom the height measurement point
        newFrame = self.visionService.captureImage()
        estimatedHeight = self.measureHeight(newFrame, maxAttempts=10, debug=False)
        laserController.turnOff()

        # self.robotService.moveToStartPosition()
        scaleFactor = 1
        message = "Workpiece created successfully"
        # convert new frame to rgb
        newFrame = cv2.cvtColor(newFrame, cv2.COLOR_BGR2RGB)
        self.robotService.moveToStartPosition()
        return True, estimatedHeight, contourArea, contour, scaleFactor, createWpImage, message

    def updateToolChangerStation(self):
        toolChanger = self.robotService.toolChanger

        slotToolMap = toolChanger.getSlotToolMap()

        X_TOLERANCE = 150  # Allowable X-offset between slot and tool
        slotIds = toolChanger.getSlotIds()  # Slot markers
        toolIds = toolChanger.getReservedForIds()  # Tool markers
        validIds = set(slotIds + toolIds)  # Combine slot & tool IDs into a valid set
        expected_mapping = dict(zip(slotIds, toolIds))  # Expected slot-to-tool mapping

        time.sleep(1)

        arucoCorners, arucoIds, image = self.visionService.detectArucoMarkers()

        if arucoIds is None or len(arucoIds) == 0:
            print("No ArUco markers detected!")
            return False, "No ArUco markers detected!"

        arucoIds = arucoIds.flatten()  # Convert to a flat list

        # рџ”№ Strict filtering: Only process markers in slotIds or toolIds
        validMarkers = [(id, corners) for id, corners in zip(arucoIds, arucoCorners) if id in validIds]
        filteredIds = [id for id, _ in validMarkers]  # Only valid IDs

        if not validMarkers:
            print("No valid markers detected!")
            return False, "No valid markers detected!"

        detected_slots = []
        detected_tools = []
        marker_positions = {}  # Store marker bounding boxes

        # Process only valid markers
        for marker_id, corners in validMarkers:
            center_x = np.mean(corners[0][:, 0])  # Get center X
            center_y = np.mean(corners[0][:, 1])  # Get center Y
            marker_positions[marker_id] = corners[0]  # Store full bounding box

            if marker_id in slotIds:
                detected_slots.append((marker_id, center_x, center_y))  # Store slot marker
            elif marker_id in toolIds:
                detected_tools.append((marker_id, center_x, center_y))  # Store tool marker

        # Print detected slots and tools
        print("Detected Slots:", detected_slots)
        print("Detected Tools:", detected_tools)

        # Sort by Y-coordinate (top-to-bottom)
        detected_slots.sort(key=lambda x: x[2])  # Sort slots by Y
        detected_tools.sort(key=lambda x: x[2])  # Sort tools by Y

        correct_placement = True
        detected_mapping = {}
        misplaced_tools = []  # Store misplaced tools for red bounding box

        print("\nDEBUG: Detected Slot-Tool Mapping:")
        for slot_id, slot_x, slot_y in detected_slots:
            # Find the nearest tool below the slot
            matching_tool = -1  # Default if no tool is found
            if len(detected_tools) > 0:
                tool_id = detected_tools[0][0]

            for tool_id, tool_x, tool_y in detected_tools:
                if abs(slot_x - tool_x) < X_TOLERANCE and tool_y > slot_y:  # X alignment + tool below slot
                    matching_tool = tool_id
                    break  # Stop after finding the first valid tool

            detected_mapping[slot_id] = matching_tool  # Store detected slot-tool pairs

            print(f"   - Slot {slot_id} в†’ Detected Tool: {matching_tool} (Expected: {expected_mapping[slot_id]})")

            # Call tool changer functions
            if matching_tool == -1:
                print(f"Setting {slot_id} as available!")
                self.robotService.toolChanger.setSlotAvailable(slot_id)
            else:
                self.robotService.toolChanger.setSlotNotAvailable(slot_id)

            print("ToolChanger: ", self.robotService.toolChanger.slots)

            # Validate slot-tool match (allowing -1 but NOT incorrect tools)
            expected_tool = expected_mapping.get(slot_id)
            if matching_tool != -1 and expected_tool != matching_tool:
                correct_placement = False
                print(f"ERROR: Wrong tool under slot {slot_id}: Expected {expected_tool}, Found {matching_tool}")
                misplaced_tools.append(matching_tool)  # Store misplaced tool for red box drawing

        if correct_placement:
            print("All tools are correctly placed (or missing but allowed)!")
        else:
            print(f"Incorrect placement detected! Mapping: {detected_mapping}")

        # Draw only valid ArUco markers on the frame
        filteredCorners = [corners for id, corners in validMarkers]  # Filtered corners for valid markers
        cv2.aruco.drawDetectedMarkers(image, filteredCorners, np.array(filteredIds, dtype=np.int32))

        # Draw red rectangles around misplaced tools
        for tool_id in misplaced_tools:
            if tool_id in marker_positions:
                corners = marker_positions[tool_id].astype(int)
                cv2.polylines(image, [corners], isClosed=True, color=(0, 0, 255), thickness=3)  # Red bounding box

        toolCheckPos = [-350, 650, 200, 180, 0, 90]
        self.robotService.moveToPosition(toolCheckPos, 0, 0, 100, 30)

        maxAttempts = 30

        filteredIds = []
        while maxAttempts > 0:
            arucoCorners, arucoIds, image = self.visionService.detectArucoMarkers(flip=True)
            if arucoIds is not None:
                image_height = image.shape[0]
                # рџ”№ Strict filtering: Only process markers in slotIds or toolIds and in the lower half of the image
                validMarkers = [(id, corners) for id, corners in zip(arucoIds, arucoCorners)
                                if id.item() in validIds and np.mean(corners[0][:, 1]) > image_height / 2]

                filteredIds = [id for id, _ in validMarkers]  # Only valid IDs

                if validMarkers:
                    break
            maxAttempts -= 1

        if len(filteredIds) != 0:
            currentTool = int(arucoIds[0])
            print("Current tool in tool check: ", currentTool)
            self.robotService.currentGripper = currentTool
        else:
            print("No tool detected in tool check")
