from starlette.endpoints import HTTPEndpoint
from starlette.responses import UJSONResponse


class SensorsEndpoint(HTTPEndpoint):
    async def get(self, request):
        return UJSONResponse("hello world")
