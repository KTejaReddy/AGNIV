from fastapi import Request
from fastapi.responses import JSONResponse
from .logging import logger

class AGNIVException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, AGNIVException):
        logger.error(f"AGNIV Exception: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": True, "message": exc.message},
        )
    logger.exception(f"Unhandled Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": "Internal Server Error", "details": str(exc)},
    )
