# create class VacuumPump
import time


class VacuumPump:
    ON_VALUE = 1
    OFF_VALUE = 0
    def __init__(self):
        self.xOffset = 0  # x offset from the main tooltip
        self.yOffset = 0  # y offset from the main tooltip
        self.zOffset = 105 # z offset from the main tooltip
        self.digitalOutput = 3
        self.vacuumPump = None

    def turnOn(self, robot):
        print("Turning on vacuum pump")
        result = robot.setDigitalOutput(self.digitalOutput, self.ON_VALUE)  # Open the control box DO
        print("Vacuum pump turned on: ", result)

    def turnOff(self, robot):
        result = robot.setDigitalOutput(self.digitalOutput, self.OFF_VALUE)  # Open the control box DO
        result = robot.setDigitalOutput(2, 1)
        time.sleep(0.3)
        result = robot.setDigitalOutput(2, 0)

