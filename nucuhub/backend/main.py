import uvicorn
from nucuhub.backend.routes import get_default_routes
from nucuhub.config import ApplicationConfig
from starlette.applications import Starlette


def get_app():
    debug = ApplicationConfig.BACKEND_DEBUG
    default_routes = get_default_routes()
    return Starlette(debug=debug, routes=default_routes)


if __name__ == "__main__":
    app = get_app()
    uvicorn.run(app)
