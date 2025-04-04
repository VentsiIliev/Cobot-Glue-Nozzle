class BrightnessController(Settings):
    def __init__(self,data:dict=None):
        super().__init__()
        # Initialize default brightness settings
        self.set_value("brightness", 0)
        self.set_value("contrast", 0)
        self.set_value("saturation", 0)
        self.set_value("hue", 0)