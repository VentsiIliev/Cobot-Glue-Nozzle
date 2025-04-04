# Importing the required libraries
import queue
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

# Importing the required classes from the GUI package
from GUI.TeachDialog import TeachDialog
from GUI.SettingsDialog import SettingsDialog
from GUI.TeachDialog import TeachDialog
from GUI.ResponseHandler import ResponseHandler

# Importing the required classes from the API package
from API.Action import Action
from API.Request import Request
from API.Response import Response
from API import Constants
from API.RequestSender import RequestSender


class MainWindow:
    def __init__(self, root, requestSender: RequestSender):
        self.requestSender = requestSender
        self.root = root
        self.root.title("PL Project")
        self.root.geometry("1280x720")
        self.root.minsize(1280, 720)  # Prevent extreme resizing issues
        # self.root.resizable(False, False)

        self.bindKeys()

        self.frameQueue = queue.Queue()

        self.init_styles()
        self.initUI()

        self.responseHandler = ResponseHandler()
        self.updateCameraLabel()

    def bindKeys(self):
        self.root.bind("<Control-s>", self.openSettings)
        self.root.bind("<o>", self.glueOn)
        self.root.bind("<p>", self.glueOff)

    def init_styles(self):
        """Initialize custom styles for UI components."""
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("Side.TFrame", background="#282A36")
        style.configure("Main.TFrame", background="#E9E9E9")
        style.configure("TopBar.TFrame", background="#44475A")
        style.configure("TopBar.TLabel", font=("Arial", 14, "bold"), foreground="white", background="#44475A")

    def initUI(self):
        """Create and configure the main UI layout."""
        # Main container
        self.mainFrame = ttk.Frame(self.root, style="Main.TFrame")
        self.mainFrame.pack(fill="both", expand=True)

        # Top Bar
        self.topBar = ttk.Frame(self.mainFrame, style="TopBar.TFrame", height=25)
        self.topBar.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.topBar.grid_propagate(False)

        self.create_topbar_content()

        # Sidebar for buttons
        self.sideMenu = ttk.Frame(self.mainFrame, style="Side.TFrame", width=220)
        self.sideMenu.grid(row=1, column=0, sticky="ns")
        self.sideMenu.grid_propagate(False)

        self.create_sidebar_buttons()

        # Camera Frame
        self.cameraFrame = ttk.Frame(self.mainFrame, style="Main.TFrame")
        self.cameraFrame.grid(row=1, column=1, sticky="nsew")

        self.cameraLabel = tk.Label(self.cameraFrame, bg="white")
        self.cameraLabel.pack(expand=True, fill="both")

        # Configure grid layout for responsiveness
        self.mainFrame.columnconfigure(1, weight=1)
        self.mainFrame.rowconfigure(1, weight=1)

    def create_topbar_content(self):
        """Add title and exit button to the top bar."""
        title_label = ttk.Label(self.topBar, text="PL Project", style="TopBar.TLabel")
        title_label.pack(side="left", padx=20, pady=10)

        # exit_button = ttk.Button(self.topBar, text="Exit", command=self.root.quit, style="TButton")
        # exit_button.pack(side="right", padx=20, pady=10)

    def create_sidebar_buttons(self):
        """Create buttons in the sidebar with consistent styling."""
        buttons = [
            ("Start", lambda: self.sendRequest(Constants.ACTION_START)),
            ("Calibrate Camera", lambda: self.sendRequest(Constants.ACTION_CALIBRATE)),
            ("Create Workpiece", lambda: self.sendRequest(Constants.ACTION_CREATE_WORKPIECE)),
        ]

        for text, command in buttons:
            btn = ttk.Button(self.sideMenu, text=text, command=command, style="TButton")
            btn.pack(pady=15, padx=20, fill="x")

    def sendRequest(self, command):
        request = Request(req_type=Constants.REQUEST_TYPE_EXECUTE, action=command)
        print("Sending Request: ", request)
        self.requestSender.sendRequest(request)
        # self.actionManager.handleRequest(request)

    def updateCameraLabel(self):
        """Continuously update the camera feed."""
        try:
            # frame = self.actionManager.getLatestFrame()
            request = Request(req_type=Constants.REQUEST_TYPE_GET,
                              action=Constants.CAMERA_ACTION_GET_LATEST_FRAME, resource=Constants.REQUEST_RESOURCE_CAMERA)
            # response = self.actionManager.handleRequest(request)
            response = self.requestSender.sendRequest(request)
            response = Response.from_dict(response)
            if response.status != Constants.RESPONSE_STATUS_SUCCESS:
                self.responseHandler.handleResponse(response)
            frame = response.data['frame']

            if frame is not None:
                # convert back to array
                # frame = np.array(frame, dtype=np.uint8)
                img = Image.fromarray(frame)
                img_tk = ImageTk.PhotoImage(image=img)

                self.cameraLabel.configure(image=img_tk)
                self.cameraLabel.image = img_tk  # Prevent garbage collection
        except queue.Empty:
            pass

        self.root.after(33, self.updateCameraLabel)  # Update at ~30 FPS

    def manageCallback(self, action: Action, *args, **kwargs):
        if action == Action.OPEN_TEACH_DIALOG:
            estimatedHeight = kwargs.get('estimatedHeight', 0)
            image = kwargs.get('image', None)
            return TeachDialog(self.root, estimatedHeight, image)


    def openSettings(self, event):
        settingsDialog = SettingsDialog(self.root, self.requestSender, self.responseHandler)

    """
    This section contains temporary glue on/off functions
    """

    # Temporary glue on/off functions
    def glueOn(self, event=None):
        # data = [1, 16, 4, 20, 30, 24000, 0, 3000, 0]
        request = Request(req_type=Constants.REQUEST_TYPE_EXECUTE, action=Constants.ACTION_STOP,
                          resource=Constants.REQUEST_RESOURCE_GLUE_NOZZLE)
        # response = self.actionManager.handleRequest(request)
        response = self.requestSender.sendRequest(request)
        print(response)
        response = Response.from_dict(response)
        if response.status != Constants.RESPONSE_STATUS_SUCCESS:
            self.responceHandler.handleResponse(response)

    def glueOff(self, event=None):
        data = [0, 16, 4, 20, 30, 24000, 0, 3000, 0]
        request = Request(req_type=Constants.REQUEST_TYPE_EXECUTE, action=Constants.ACTION_START,
                          resource=Constants.REQUEST_RESOURCE_GLUE_NOZZLE,
                          data=data)
        # response = self.actionManager.handleRequest(request)
        response = self.requestSender.sendRequest(request)
        print(response)
        response = Response.from_dict(response)
        if response.status != Constants.RESPONSE_STATUS_SUCCESS:
            self.responceHandler.handleResponse(response)
