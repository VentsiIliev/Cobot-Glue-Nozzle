import copy
import time

from GlueDispensingApplication.robot.RobotWrapper import RobotWrapper
from GlueDispensingApplication.robot.RobotService import RobotService
from GlueDispensingApplication.settings.SettingsService import SettingsService

robotIp = '192.168.58.2'
robot = RobotWrapper(robotIp)
settingsService = SettingsService()
robotService = RobotService(robot, settingsService)

offsetBetweenNests = 76



nests = {
    0: [-400.71, 488.792, 124.4, 180, 0, 5],
    1: [-403.73, 564.799, 126.4, 180, 0, 5],
    2: [-406.73, 638.915, 129.1, 180, 0, 5],
    3: [-409.73, 713.674, 129.95, 180, 0, 5],
    4: [-413, 787.959, 129.95, 180, 0, 5] # not correct
}

def pickUp(nestId):
    nestPosition = nests[nestId]
    # move the robot on top of the nest
    x,y ,z ,rx, ry, rz = nestPosition
    pos1 = [x, y, z+100, rx, ry, rz]
    pos2 = [x, y, z, rx, ry, rz]
    pos3 = [x+150, y, z, rx, ry, rz]
    path = [pos1, pos2, pos3]
    print("pickUp path: ", path)
    for point in path:
        robot.moveL(point, 0, 0, 100, 30, 0)

def dropOff(nestId):
    nestPosition = nests[nestId]
    # move the robot on top of the nest
    x,y ,z ,rx, ry, rz = nestPosition
    pos1 = [x+150, y, z, rx, ry, rz]
    pos2 = [x, y, z, rx, ry, rz]
    pos3 = [x, y, z+100, rx, ry, rz]
    path = [pos1, pos2, pos3]
    print("dropOff path: ", path)
    for point in path:
        robot.moveL(point, 0, 0, 100, 30, 0)

pickUp(4)
dropOff(3)

pickUp(3)
dropOff(2)

pickUp(2)
dropOff(1)

pickUp(1)
dropOff(0)

pickUp(0)
dropOff(1)

pickUp(1)
dropOff(2)

pickUp(2)
dropOff(3)

pickUp(3)
dropOff(4)