def performWorkpiecesNesting(self, workpieces, callback=None):
    xOffsetBetweenWorkpieces = 30
    yOffsetBetweenWorkpieces = 30

    velocity, tool, workpiece, acceleration, blendR = self.getMotionParams()

    minDropOffX = -150
    maxDropOffX = 300
    maxDropOffY = 600
    dropOffPositionX = minDropOffX  # Start position for drop-off (left side)
    dropOffPositionY = maxDropOffY  # Initial Y coordinate for the first row

    toolXoffset = 0
    toolYoffset = 0

    if callback is not None:
        validationPos = [-350, 650, 450, 180, 0, 90]
        self.moveToPosition(validationPos, 0, 0, 100, 30, waitToReachPosition=True)
        callback()

    paths = []
    grippers = []
    for item in workpieces:
        gripper = int(item.gripperID.value)
        print("Gripper: ", gripper)
        print("Current gripper: ", self.currentGripper)

        if gripper == Gripper.SINGLE.value and self.currentGripper == None:
            grippers.append(0)
            print("appending 0")
        elif gripper == Gripper.DOUBLE.value and self.currentGripper == None:
            print("appending 0")
            grippers.append(4)
        else:
            if self.currentGripper is not None:
                if self.currentGripper != gripper:
                    print("appending gripper ", gripper)
                    grippers.append(gripper)
                else:
                    print("appending currentGripper ", self.currentGripper)
                    grippers.append(self.currentGripper)
            else:
                print("appending gripper ", gripper)
                grippers.append(gripper)

        cnt = item.contour
        cntObject = Contour(cnt)
        # Get the orientation angle for the contour
        # angle = utils.get_orientation(cnt) + 5
        angle = cntObject.getOrientation()
        # angle = angle +5
        centroid = cntObject.getCentroid()

        height = self.pump.zOffset + item.height

        path = self.__getNestingMoves(angle, centroid, dropOffPositionX, dropOffPositionY,
                                      tool,
                                      velocity, workpiece, height)
        paths.append(path)

        # Step 4: Translate and rotate contour
        # angle = angle - 5  # Adjust angle to account for previous offset
        angle = angle  # Adjust angle to account for previous offset
        cntObject.rotate(-angle, centroid)

        # Apply the rotation to the spray pattern if exists
        sprayPattern = item.sprayPattern
        sprayPatternObj = Contour(sprayPattern)
        if self._isValid(sprayPattern):
            sprayPatternObj.rotate(-angle, centroid)

        # Calculate the offset to align the contour at the drop-off position
        centroid = cntObject.getCentroid()
        xOffset = dropOffPositionX - (centroid[0])
        yOffset = dropOffPositionY - (centroid[1])

        # Apply the translation to the contour
        cntObject.translate(xOffset, yOffset)

        # Apply the translation to the spray pattern if exists
        if self._isValid(sprayPattern):
            sprayPatternObj.translate(xOffset, yOffset)

        # Update the contour and spray pattern in the workpiece object
        item.contour = cntObject.get_contour_points()
        item.sprayPattern = sprayPatternObj.get_contour_points()

        # Prepare the contour for bounding box calculation
        bbox = cv2.boundingRect(np.array(cntObject.get_contour_points(), dtype=np.int32))
        width, height = bbox[2], bbox[3]

        # Step 6: Update drop-off position for the next workpiece
        dropOffPositionX += width + xOffsetBetweenWorkpieces  # Move to the right for the next workpiece

        # Step 7: If drop-off position exceeds the workspace, move to a new row
        # Step 7: If drop-off position exceeds the workspace, move to a new row
        if dropOffPositionX > maxDropOffX:  # Once we hit x = 300, move to the next row
            dropOffPositionX = minDropOffX  # Reset X to -300 for the new row
            dropOffPositionY -= height + yOffsetBetweenWorkpieces  # Move down the row

    for gripperId, path in zip(grippers, paths):
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

        self.pump.turnOn(self.robot)
        for point in path:
            self.robot.moveCart(point, tool, workpiece, vel=velocity, acc=40)
        self.pump.turnOff(self.robot)

    # if self.currentGripper is not None:
    #   result,message = self.dropOffGripper(self.currentGripper,callback)
    #  if not result:
    #     return False,message

    return True, None