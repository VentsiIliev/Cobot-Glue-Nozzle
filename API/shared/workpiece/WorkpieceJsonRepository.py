import os
import json
import numpy as np
import datetime
from enum import Enum
from typing import Type
import copy

from API.shared.workpiece.Workpiece import WorkpieceField
from API.shared.interfaces.JsonSerializable import JsonSerializable


class WorkpieceJsonRepository:
    DATE_FORMAT = "%Y-%m-%d"
    TIMESTAMP_FORMAT = "%Y-%m-%d_%H-%M-%S-%f"
    FOLDER_NAME = "workpieces"
    WORKPIECE_FILE_SUFFIX = "_workpiece.json"  # Ensure the files have this suffix

    def __init__(self, baseDir, fields, dataClass):

        if not issubclass(dataClass, JsonSerializable):
            raise TypeError("dataClass must be a subclass of JsonSerializable")



        self.directory = os.path.join(baseDir, self.FOLDER_NAME)
        self.dataClass = dataClass
        self.fields = fields
        # check if dataClass is JsonSerializable

        self.data = self.loadData()
        self.visited_dirs = set()  # Track visited directories to avoid repetition
        if not os.path.exists(self.directory):
            print(f"Directory {self.directory} does not exist.")
            raise FileNotFoundError(f"Directory {self.directory} not found.")


    def loadData(self):
        """
        Recursively iterates over all directories inside the base directory, deserializes all JSON files,
        and returns a list of objects of the provided class type (e.g., Workpiece).
        """
        objects = []

        # Check if the base directory exists
        if not os.path.exists(self.directory):
            print(f"Directory {self.directory} does not exist.")
            return objects
        else:
            print(f"Directory exists: {self.directory}")
        print(f"Directory: {self.directory}")
        # Walk through all subdirectories and files
        for root, _, files in os.walk(self.directory):
            print(f"Root: {root}")
            for file in files:
                print(f"File: {file}")
                file_path = os.path.join(root, file)
                print(f"File Path: {file_path}")  # Debugging: check the full file path
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)  # Load JSON data
                        print(f"Loaded Data: {data}")  # Debugging: Show the loaded data
                        # Deserialize the data using the provided class
                        obj = self.dataClass.deserialize(data)  # Deserialize into the appropriate object
                        print(f"Deserialized Object: {obj}")  # Debugging: Show the deserialized object
                        objects.append(obj)
                except Exception as e:
                    print(f"Error loading object from {file_path}: {e}")
                    raise Exception(f"Error loading object: {e}")

        return objects

    def saveWorkpiece(self, workpiece):
        # Get today's date and timestamp
        today_date = datetime.datetime.now().strftime(self.DATE_FORMAT)
        timestamp = datetime.datetime.now().strftime(self.TIMESTAMP_FORMAT)

        # Full path based on today's date
        date_dir = os.path.join(self.directory, today_date)
        timestamp_dir = os.path.join(date_dir, timestamp)

        # Check if the folder for today's date exists, if not, create it
        if not os.path.exists(date_dir):
            os.makedirs(date_dir)

        # Create the folder with the timestamp if it doesn't exist
        os.makedirs(timestamp_dir, exist_ok=True)

        # Serialize the workpiece
        serialized_data = json.dumps(self.dataClass.serialize(copy.deepcopy(workpiece)), indent=4)

        # Define the file path
        file_path = os.path.join(timestamp_dir, f"{timestamp}{self.WORKPIECE_FILE_SUFFIX}")

        try:
            # Save the workpiece to the file
            with open(file_path, 'w') as file:
                file.write(serialized_data)
            # workpiece.sprayPattern = np.array(workpiece.sprayPattern).reshape(-1, 1, 2).astype(np.int32)
            self.data.append(workpiece)
            print(f"Workpiece saved to {file_path}")

            return True,"Workpiece saved successfully"
        except Exception as e:
            raise Exception(e)
            # print(f"Error saving workpiece: {e}")







