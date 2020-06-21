from starlette.routing import Route

from nucuhub.backend.endpoints import SensorsEndpoint


def get_default_routes():
    routes = [
        Route("/", SensorsEndpoint),
        Route("/api/v1/sensors", SensorsEndpoint),
    ]
    return routes
