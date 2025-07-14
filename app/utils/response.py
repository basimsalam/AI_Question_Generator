from fastapi.responses import JSONResponse
from fastapi import status
from typing import Any, Dict


def success_response(body: Dict[str, Any], message: str = "Success", status_code: int = status.HTTP_200_OK):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "message": message,
            "body": body
        }
    )


def error_response(message: str = "Something went wrong", body: Dict[str, Any] = None, status_code: int = status.HTTP_400_BAD_REQUEST):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message,
            "body": body or {}
        }
    )
