import traceback

from API import Constants
from API.Response import Response
from API.Request import Request
class GlueNozzleController:

    def __init__(self, glueNozzleService:'GlueNozzleService'):
        self.glueNozzleService = glueNozzleService

    def handleExecuteRequest(self,request:'Request'):
        # HANDLE GLUE ON
        if request.action == Constants.ACTION_START:
            try:
                self.glueNozzleService.sendCommand(request.data)
                return Response(Constants.RESPONSE_STATUS_SUCCESS, message="Glue turned on").to_dict()
            except Exception as e:
                traceback.print_exc()
                return Response(Constants.RESPONSE_STATUS_ERROR,
                                message=f"Error turning glue on: {e}").to_dict()

        # HANDLE GLUE OFF
        elif request.action == Constants.ACTION_STOP:
            try:
                self.glueNozzleService.stopGlueDispensing()
                return Response(Constants.RESPONSE_STATUS_SUCCESS, message="Glue turned off").to_dict()
            except Exception as e:
                traceback.print_exc()
                return Response(Constants.RESPONSE_STATUS_ERROR,
                                message=f"Error turning glue off: {e}").to_dict()

