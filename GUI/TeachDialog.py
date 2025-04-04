import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

from GlueDispensingApplication.tools.enums.GlueType import GlueType
from GlueDispensingApplication.tools.enums.Program import Program
from GlueDispensingApplication.tools.enums.ToolID import ToolID


class TeachDialog:
    def __init__(self, parent, estimatedHeight, image):
        self.image = image
        self.originalSize = image.shape[:2]  # Store the original size (height, width)
        self.displaySize = [800, 450]
        self.estimatedHeight = estimatedHeight
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Teach Mode")
        self.click_points = []

        # Create input fields and dropdowns
        ttk.Label(self.dialog, text="Workpiece ID").grid(row=0, column=0, padx=5, pady=5)
        self.workpieceIdEntry = ttk.Entry(self.dialog)
        self.workpieceIdEntry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.dialog, text="Name").grid(row=1, column=0, padx=5, pady=5)
        self.nameEntry = ttk.Entry(self.dialog)
        self.nameEntry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.dialog, text="Description").grid(row=2, column=0, padx=5, pady=5)
        self.descriptionEntry = ttk.Entry(self.dialog)
        self.descriptionEntry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.dialog, text="Tool").grid(row=3, column=0, padx=5, pady=5)
        self.toolDropdown = ttk.Combobox(self.dialog, values=[method.value for method in ToolID])
        self.toolDropdown.grid(row=3, column=1, padx=5, pady=5)
        self.toolDropdown.set(ToolID.Tool1.value)

        ttk.Label(self.dialog, text="Glue Type").grid(row=4, column=0, padx=5, pady=5)
        self.glueTypeDropdown = ttk.Combobox(self.dialog, values=[method.value for method in GlueType])
        self.glueTypeDropdown.grid(row=4, column=1, padx=5, pady=5)
        self.glueTypeDropdown.set(GlueType.TypeA.value)

        ttk.Label(self.dialog, text="Program").grid(row=5, column=0, padx=5, pady=5)
        self.programDropdown = ttk.Combobox(self.dialog, values=[method.value for method in Program])
        self.programDropdown.grid(row=5, column=1, padx=5, pady=5)
        self.programDropdown.set(Program.TRACE)

        ttk.Label(self.dialog, text="Offset").grid(row=6, column=0, padx=5, pady=5)
        self.offsetEntry = ttk.Entry(self.dialog)
        self.offsetEntry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self.dialog, text="Material Type").grid(row=7, column=0, padx=5, pady=5)
        self.materialTypeEntry = ttk.Entry(self.dialog)
        self.materialTypeEntry.grid(row=7, column=1, padx=5, pady=5)

        # set initial value estimatedHeight
        ttk.Label(self.dialog, text="Height").grid(row=8, column=0, padx=5, pady=5)
        self.heightEntry = ttk.Entry(self.dialog)
        self.heightEntry.grid(row=8, column=1, padx=5, pady=5)
        self.heightEntry.insert(0, str(self.estimatedHeight))



        submitButton = ttk.Button(self.dialog, text="Submit", command=self.onSubmit)
        submitButton.grid(row=11, column=0, columnspan=2, pady=10)

        # Display image with contours
        self.imageLabel = ttk.Label(self.dialog)
        self.imageLabel.grid(row=12, column=0, columnspan=2, padx=5, pady=5)
        self.displayImage(image)

        # Bind the click event to capture the click position
        self.imageLabel.bind("<Button-1>", self.onImageClick)

        self.dialog.transient(parent)
        self.dialog.grab_set()
        parent.wait_window(self.dialog)

    def displayImage(self, image):
        # Define original and display sizes
        self.originalSize = (1280, 720)  # Original resolution
        self.displaySize = (800, 450)  # Resized resolution

        # Resize the image to 800x450
        resized_image = cv2.resize(image.copy(), self.displaySize, interpolation=cv2.INTER_AREA)

        # Convert the resized image to a format suitable for Tkinter
        image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        self.cropped_image = Image.fromarray(image_rgb)
        self.cropped_image = ImageTk.PhotoImage(self.cropped_image)

        # Display the image in the label
        self.imageLabel.imgtk = self.cropped_image
        self.imageLabel.configure(image=self.cropped_image)

    def onImageClick(self, event):
        # Correct scale calculation
        scale_x = self.originalSize[0] / self.displaySize[0]  # 1280 / 800 = 1.6
        scale_y = self.originalSize[1] / self.displaySize[1]  # 720 / 450 = 1.6

        # Convert click coordinates to original image scale
        original_x = int(event.x * scale_x)
        original_y = int(event.y * scale_y)

        # Store the mapped original coordinates
        self.click_points.append([original_x, original_y])

        # Convert the displayed image back to a NumPy array
        cropped_image_pil = ImageTk.getimage(self.cropped_image)
        cropped_image_np = np.array(cropped_image_pil)

        # Convert the image to BGR format for OpenCV
        cropped_image_np = cv2.cvtColor(cropped_image_np, cv2.COLOR_RGB2BGR)

        # Scale points down for drawing on resized image
        scaled_points = [(int(p[0] / scale_x), int(p[1] / scale_y)) for p in self.click_points]

        # Draw lines between points
        if len(scaled_points) > 1:
            for i in range(len(scaled_points) - 1):
                cv2.line(cropped_image_np, scaled_points[i], scaled_points[i + 1], (255, 0, 0), 2)

        # Convert the numpy array back to PhotoImage for Tkinter display
        cropped_image_np = cv2.cvtColor(cropped_image_np, cv2.COLOR_BGR2RGB)
        self.cropped_image = ImageTk.PhotoImage(image=Image.fromarray(cropped_image_np))
        self.imageLabel.imgtk = self.cropped_image
        self.imageLabel.configure(image=self.cropped_image)

    def onSubmit(self):
        self.workpieceId = self.workpieceIdEntry.get()
        self.name = self.nameEntry.get()
        self.description = self.descriptionEntry.get()

        tool_id_str = self.toolDropdown.get()
        self.toolId = ToolID(tool_id_str)

        glue_type_str = self.glueTypeDropdown.get()
        self.glueType = GlueType(glue_type_str)

        program_name_str = self.programDropdown.get()
        self.program = Program(program_name_str)

        self.materialType = self.materialTypeEntry.get()
        self.offset = self.offsetEntry.get()
        self.height = self.heightEntry.get()

        self.validateData()
        self.destroy()

    def destroy(self):
        self.dialog.destroy()

    def validateData(self):
        if not self.workpieceId or not self.name or not self.description or not self.materialType or not self.offset or not self.height:
            raise Exception("All fields must be filled out")

        workpieceId = self.workpieceId
        if not workpieceId.isdigit():
            raise Exception("Workpiece ID must be a number")

        offset = self.offset
        if not offset.replace(".", "", 1).isdigit():
            raise Exception("Offset must be a number")
        height = self.height
        if not height.replace(".", "", 1).isdigit():
            raise Exception("Height must be a number")

    def getData(self):
        # Get selected nozzles
        # selected_tools = [tools for tools, var in self.tool_vars.items() if var.get()]
        selected_tools = []
        print("Selected tool:", selected_tools)
        data = [int(self.workpieceId), self.name, self.description, self.toolId, self.glueType, self.program,
                self.materialType, int(self.offset), float(self.height), selected_tools, self.click_points]
        return data
