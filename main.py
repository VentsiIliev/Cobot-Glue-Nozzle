from GlueDispensingApplication.GlueSprayingApplication import GlueSprayingApplication
from GlueDispensingApplication.DomesticRequestSender import DomesticRequestSender
from GlueDispensingApplication.RequestHandler import RequestHandler
# IMPORT SERVICES
from GlueDispensingApplication.settings.SettingsService import SettingsService
from GlueDispensingApplication.vision.VisionService import VisionServiceSingleton
from GlueDispensingApplication.tools.GlueNozzleService import GlueNozzleService
from API.shared.workpiece.WorkpieceService import WorkpieceService
from GlueDispensingApplication.robot.RobotService import RobotService
from GlueDispensingApplication.robot.RobotCalibrationService import RobotCalibrationService
# IMPORT CONTROLLERS
from GlueDispensingApplication.settings.SettingsController import SettingsController
from GlueDispensingApplication.vision.CameraSystemController import CameraSystemController
from GlueDispensingApplication.tools.GlueNozzleController import GlueNozzleController
from GlueDispensingApplication.workpiece.WorkpieceController import WorkpieceController
from GlueDispensingApplication.robot.RobotController import RobotController

# GUI RELATED IMPORTS
newGui = True
testRobot = False
if newGui:
    from GUI_NEW.GUI_NEW import GUI_NEW
    from pl_gui.PlGui import PlGui
else:
    import tkinter as tk
    from GUI.GUI import GUI
    from GUI.MainWindow import MainWindow

robotIp = '192.168.58.2'

if testRobot:
    from GlueDispensingApplication.robot.RobotWrapper import TestRobotWrapper
    robot = TestRobotWrapper()
else:
    from GlueDispensingApplication.robot.RobotWrapper import RobotWrapper
    robot = RobotWrapper(robotIp)

if __name__ == "__main__":

    # INIT SERVICES
    settingsService = SettingsService()
    cameraService = VisionServiceSingleton().get_instance()
    glueNozzleService = GlueNozzleService()
    workpieceService = WorkpieceService()

    robotService = RobotService(robot,settingsService, glueNozzleService)
    robotCalibrationService = RobotCalibrationService()

    # INIT CONTROLLERS
    settingsController = SettingsController(settingsService)
    cameraSystemController = CameraSystemController(cameraService)
    glueNozzleController = GlueNozzleController(glueNozzleService)
    workpieceController = WorkpieceController(workpieceService)
    robotController = RobotController(robotService,robotCalibrationService)

    # INIT APPLICATION
    glueSprayingApplication = GlueSprayingApplication(None, cameraService, settingsService,
                                                      glueNozzleService, workpieceService,
                                                      robotService,robotCalibrationService)  # Initialize ActionManager with a placeholder callback

    # INIT REQUEST HANDLER
    requestHandler = RequestHandler(glueSprayingApplication, settingsController, cameraSystemController,
                                    glueNozzleController, workpieceController,robotController)
    print("Request Handler initialized")
    """GUI RELATED INITIALIZATIONS"""

    # INIT DOMESTIC REQUEST SENDER
    domesticRequestSender = DomesticRequestSender(requestHandler)
    print("Domestic Request Sender initialized")
    # INIT MAIN WINDOW

    if newGui:
        from pl_gui.controller.Controller import Controller
        controller= Controller(domesticRequestSender)
        gui=PlGui(controller=controller)
        gui.start()
        # gui = GUI_NEW(domesticRequestSender)
        # gui.start()
    else:
        root = tk.Tk()
        mainWindow = MainWindow(root, domesticRequestSender)
        # Set the callback function for the glue spraying application
        glueSprayingApplication.callbackFunction = mainWindow.manageCallback
        # START GUI
        gui = GUI(domesticRequestSender, mainWindow)
        gui.start()


