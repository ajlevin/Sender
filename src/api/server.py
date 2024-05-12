from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import user, admin, climbing, routes
import json
import logging
import sys
from starlette.middleware.cors import CORSMiddleware

description = """

"""

app = FastAPI(
    title="Rock Climbing",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Andrew Martinez",
        "email": "amart531@calpoly.edu",
    },
)

app.include_router(admin.router)
app.include_router(user.router)
app.include_router(climbing.router)
app.include_router(routes.router)


@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Welcome."}
