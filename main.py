from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from database import create_db_and_tables
from routers.event_router import router as event_router
from routers.camera_router import router as camera_router
from routers.area_router import router as area_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=JSONResponse)
async def read_root(request: Request):
    base_url = str(request.base_url)
    return {
        "message": "Welcome to the FastAPI User Management API",
        "docs": {
            "Swagger UI": {
                "description": "Interactive API documentation and testing",
                "link": base_url + "docs"
            },
            "ReDoc": {
                "description": "Alternative API documentation",
                "link": base_url + "redoc"
            }
        }
    }

create_db_and_tables()
app.include_router(event_router)
app.include_router(camera_router)
app.include_router(area_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)