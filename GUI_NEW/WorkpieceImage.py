from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt, QPoint

class WorkpieceImage(QFrame):
    def __init__(self, parent, image: QPixmap):
        """
        Initializes the WorkpieceImage class, accepts a QPixmap image object
        and initializes the UI.
        """
        super().__init__(parent)
        self.parent = parent
        self.setFixedSize(850, 400)  # Set a fixed size for the frame
        self.image = image  # Directly assign the QPixmap image
        self.setMouseTracking(True)  # Allow mouse tracking (to capture the mouse movement)
        self.clickPoints = []  # Store the click points

    def paintEvent(self, event):
        """
        This method is used to draw the image on the QFrame.
        """
        painter = QPainter(self)
        # Draw the image centered in the frame
        rect = self.rect()
        image_rect = self.image.rect()
        painter.drawPixmap(rect.center() - image_rect.center(), self.image)

    def mousePressEvent(self, event):
        """
        This method captures mouse click events within the frame.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            # Handle the mouse click here
            click_position = event.pos()
            self.clickPoints.append(click_position)
            # draw lines between points
            if len(self.clickPoints) > 1:
                for i in range(len(self.clickPoints) - 1):
                    self.drawLine(self.clickPoints[i], self.clickPoints[i + 1])
            print(f"Mouse clicked at: {click_position}")
            self.handleClick(click_position)

    def handleClick(self, position: QPoint):
        """
        Custom function to handle the click event inside the image frame.
        You can customize this method to process the click as needed.
        """
        print(f"Click processed at: {position}")
        # For example, you can perform any action based on the click position
