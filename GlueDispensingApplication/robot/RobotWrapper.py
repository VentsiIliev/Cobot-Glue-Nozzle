import platform

if platform.system() == "Windows":
    from fairino.windows import Robot
elif platform.system() == "Linux":
    print("Linux detected")
    from fairino.linux import Robot
else:
    raise Exception("Unsupported OS")

from enum import Enum
class TestRobotWrapper():
    def __init__(self):
        pass

    def moveCart(self,position, tool, user, vel=100, acc=30):
        print("MoveCart: ", position, tool, user, vel, acc)
        return position

    def moveL(self,position, tool, user, vel, acc, blendR):
        print("MoveL: ", position, tool, user, vel, acc, blendR)
        return position

    def getCurrentPosition(self):
        return [0, 0, 0, 0, 0, 0]

    def getCurrentLinierSpeed(self):
        return 0

    def enable(self):
        pass
    def disable(self):
        pass
    def printSdkVerison(self):
        pass
    def setDigitalOutput(self, portId, value):
        pass

class Axis(Enum):
    X = 1
    Y = 2
    Z = 3
    RX = 4
    RY = 5
    RZ = 6

    def __str__(self):
        return self.name

class Direction(Enum):
    MINUS = 0
    PLUS = 1

    def __str__(self):
        return self.name

class RobotWrapper:
    def __init__(self, ip):
        self.ip = ip
        self.robot = Robot.RPC(self.ip)
        """overSpeedStrategy: over speed handling strategy
        0 - strategy off;
        1 - standard;
        2 - stop on error when over speeding;
        3 - adaptive speed reduction, default 0"""
        self.overSpeedStrategy = 3


    def moveCart(self,position, tool, user, vel=100, acc=30):
        return self.robot.MoveCart(position, tool, user, vel=vel, acc=acc)

    def moveL(self,position, tool, user, vel, acc, blendR):
        return self.robot.MoveL(position, tool, user, vel=vel, acc=acc, blendR=blendR)

    def getCurrentPosition(self):
        return self.robot.GetActualTCPPose()[1]

    def getCurrentLinerSpeed(self):
        return self.robot.GetActualTCPCompositeSpeed()

    def enable(self):
        self.robot.RobotEnable(1)

    def disable(self):
        self.robot.RobotEnable(0)

    def printSdkVersion(self):
        print("Version: ", self.robot.GetSDKVersion())

    def setDigitalOutput(self, portId, value):
        self.robot.SetDO(portId, value)

    def startJog(self,axis,direction,step,vel,acc):
        axis = axis.value
        direction = direction.value
        return self.robot.StartJOG(ref=4,nb=axis,dir=direction,vel=vel,acc=acc,max_dis=step)


    def stopMotion(self):
        print("Stopping Robot")
        return self.robot.StopMotion()

    def resetAllErrors(self):
        print("Resting Errors")
        return self.robot.ResetAllError()
