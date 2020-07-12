from nucuhub.backend.endpoints import SensorsEndpoint
from starlette.routing import Route


def get_default_routes():
    routes = [
        Route("/", SensorsEndpoint),
        Route("/api/v1/sensors", SensorsEndpoint),
    ]
    return routes
