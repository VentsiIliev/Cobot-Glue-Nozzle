from tkinter import messagebox
from API.Constants import RESPONSE_STATUS_SUCCESS, RESPONSE_STATUS_WARNING, RESPONSE_STATUS_ERROR
from API.Response import Response
class ResponseHandler():
    def __init__(self):
        pass

    def handleResponse(self, response:Response):
        """
        Handles the response from the server.

        :param response: The response from the server.
        """
        if response.status == RESPONSE_STATUS_SUCCESS:
            print("Message: ", response.message)
            messagebox.showinfo("Success",response.message)
        elif response.status == RESPONSE_STATUS_WARNING:
            messagebox.showwarning("Warning",response.message)
        elif response.status == RESPONSE_STATUS_ERROR:
            messagebox.showerror("Error",response.message)
        else:
            raise ValueError(f"Invalid response status: {response.status}")

        return response