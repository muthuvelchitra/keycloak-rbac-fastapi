from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    UnauthorizedException,
    ForbiddenException,
    ResourceNotFoundException,
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(
        request: Request,
        exc: UnauthorizedException
    ):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": exc.message,
                "data": None,
            },
        )

    @app.exception_handler(ForbiddenException)
    async def forbidden_handler(
        request: Request,
        exc: ForbiddenException
    ):
        return JSONResponse(
            status_code=403,
            content={
                "success": False,
                "message": exc.message,
                "data": None,
            },
        )

    @app.exception_handler(ResourceNotFoundException)
    async def not_found_handler(
        request: Request,
        exc: ResourceNotFoundException
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": exc.message,
                "data": None,
            },
        )