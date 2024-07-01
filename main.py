from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from database import create_db_and_tables
from routers.event_router import router as event_router
from routers.camera_router import router as camera_router
from routers.area_router import router as area_router
from routers.eventType_router import router as eventType_router
from routers.stream_router import router as stream_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/", response_class=JSONResponse)
# async def read_root(request: Request):
#     base_url = str(request.base_url)
#     return {
#         "message": "Welcome to the FastAPI User Management API",
#         "docs": {
#             "Swagger UI": {
#                 "description": "Interactive API documentation and testing",
#                 "link": base_url + "docs"
#             },
#             "ReDoc": {
#                 "description": "Alternative API documentation",
#                 "link": base_url + "redoc"
#             }
#         }
#     }

create_db_and_tables()
app.include_router(event_router)
app.include_router(camera_router)
app.include_router(area_router)
app.include_router(eventType_router)
app.include_router(stream_router)

app.mount("/", StaticFiles(directory="static",html=True))


import asyncio
from asyncio.windows_events import ProactorEventLoop
from uvicorn import Config, Server
class ProactorServer(Server):
    def run(self, sockets=None):
        loop = ProactorEventLoop()
        asyncio.set_event_loop(loop)
        asyncio.run(self.serve(sockets=sockets))



if __name__ == "__main__":
    #uvicorn.run(app, host="0.0.0.0", port=8000)
    config = Config(app=app, host="0.0.0.0", port=8000, reload=False)
    server = ProactorServer(config=config)
    server.run()

