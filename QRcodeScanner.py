import cv2
# from matplotlib import pyplot as plt
from pyzbar.pyzbar import decode

from VisionSystem.VisionSystem import VisionSystem
# from VisionSystem.VisionSystem import CameraSystem


def detect_and_decode_barcode(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect barcodes in the grayscale image
    barcodes = decode(gray)
    print("Barcodes Found:", len(barcodes))
    # Loop over detected barcodes
    for barcode in barcodes:
        # Extract barcode data and type
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type

        # Draw a rectangle around the barcode
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Put barcode data and type on the image
        cv2.putText(image, f"{barcode_data} ({barcode_type})",
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        if barcode_data is not None:
            return barcode_data
    return None


import cv2
import numpy as np

VisionSystem = VisionSystem()

slotIds = [10, 11, 12, 13, 14,15,16,17,18,19]  # Slot markers
toolIds = [0, 1, 2, 3, 4,5,6,7,8,9]  # Tool markers
validIds = set(slotIds + toolIds)  # Combine slot & tool IDs into a valid set
expected_mapping = dict(zip(slotIds, toolIds))  # Expected slot-to-tool mapping

X_TOLERANCE = 150  # Allowable X-offset between slot and tool

while True:
    _, frame, _ = VisionSystem.run()  # Capture frame
    if frame is None:
        continue
    # flip image horizontally

    # Detect ArUco markers
    arucoCorners, arucoIds, image = VisionSystem.detectArucoMarkers(flip = True)

    if arucoIds is None or len(arucoIds) == 0:
        print("No ArUco markers detected!")
        cv2.imshow("Barcode Detection", frame)
        cv2.waitKey(1)
        continue

    arucoIds = arucoIds.flatten()  # Convert to a flat list

    # 🔹 Strict filtering: Only process markers in slotIds or toolIds
    image_height = 720
    validMarkers = [(id, corners) for id, corners in zip(arucoIds, arucoCorners)
                    if id.item() in validIds and np.mean(corners[0][:, 1]) > image_height / 2]

    filteredIds = [id for id, _ in validMarkers]  # Only valid IDs

    if not validMarkers:
        print("No valid markers detected!")
        cv2.imshow("Barcode Detection", frame)
        cv2.waitKey(1)
        continue

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

    print("\n🔍 DEBUG: Detected Slot-Tool Mapping:")
    for slot_id, slot_x, slot_y in detected_slots:
        # Find the nearest tool below the slot
        matching_tool = -1  # Default if no tool is found

        for tool_id, tool_x, tool_y in detected_tools:
            if abs(slot_x - tool_x) < X_TOLERANCE and tool_y > slot_y:  # X alignment + tool below slot
                matching_tool = tool_id
                break  # Stop after finding the first valid tool

        detected_mapping[slot_id] = matching_tool  # Store detected slot-tool pairs

        print(f"   - Slot {slot_id} → Detected Tool: {matching_tool} (Expected: {expected_mapping[slot_id]})")

        # Validate slot-tool match (allowing -1 but NOT incorrect tools)
        expected_tool = expected_mapping.get(slot_id)
        if matching_tool != -1 and expected_tool != matching_tool:
            correct_placement = False
            print(f"❌ ERROR: Wrong tool under slot {slot_id}: Expected {expected_tool}, Found {matching_tool}")
            misplaced_tools.append(matching_tool)  # Store misplaced tool for red box drawing

    if correct_placement:
        print("✅ All tools are correctly placed (or missing but allowed)!")
    else:
        print(f"❌ Incorrect placement detected! Mapping: {detected_mapping}")

    # Draw only valid ArUco markers on the frame (removing unwanted markers like 90)

    filteredCorners = [corners for id, corners in validMarkers]  # Filtered corners for valid markers
    cv2.aruco.drawDetectedMarkers(frame, filteredCorners, np.array(filteredIds, dtype=np.int32))

    # Draw red rectangles around misplaced tools
    for tool_id in misplaced_tools:
        if tool_id in marker_positions:
            corners = marker_positions[tool_id].astype(int)
            cv2.polylines(frame, [corners], isClosed=True, color=(0, 0, 255), thickness=3)  # Red bounding box


    # robotService.moveToPosition()

    cv2.imshow("Barcode Detection", frame)
    cv2.waitKey(1)









