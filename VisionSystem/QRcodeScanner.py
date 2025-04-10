import cv2
# from matplotlib import pyplot as plt
from pyzbar.pyzbar import decode

from VisionSystem.VisionSystem import VisionSystem


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


VisionSystem = CameraSystem(contourDetection=False)

while True:
    _, frame, _ = VisionSystem.run()  # Capture frame
    if frame is None:
        continue

    detect_and_decode_barcode(frame)
    cv2.imshow("Barcode Detection", frame)
    cv2.waitKey(1)
