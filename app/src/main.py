from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .endpoints.register_endpoints import register_routers
import os

def create_app() -> FastAPI:
    app = FastAPI()
    
    # Mount static files
    # Assuming run from root of the project
    static_dir = os.path.join(os.getcwd(), "static")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/")
    async def read_root():
        return FileResponse(os.path.join(static_dir, "index.html"))

    register_routers(app)
    
    return app

app = create_app()
