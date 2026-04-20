import json
from typing import Any

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import record_exception_log


def build_error_response(
    *,
    status_code: int,
    code: int,
    message: str,
    data: Any | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "code": code,
            "message": message,
            "data": data,
        },
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    await record_exception_log(
        level="ERROR",
        message=f"Validation error on {request.method} {request.url.path}",
        error_stack=str(exc.errors()),
    )
    safe_errors: Any = json.loads(json.dumps(exc.errors(), default=str))
    return build_error_response(
        status_code=422,
        code=4000,
        message="validation error",
        data=safe_errors,
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    detail = exc.detail if isinstance(exc.detail, str) else "request failed"
    await record_exception_log(
        level="ERROR" if exc.status_code >= 500 else "WARNING",
        message=f"HTTP exception on {request.method} {request.url.path}: {detail}",
        error_stack=f"status_code={exc.status_code}",
    )
    return build_error_response(
        status_code=exc.status_code,
        code=exc.status_code,
        message=detail,
    )


async def fastapi_http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    return await http_exception_handler(request, exc)


async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    await record_exception_log(
        level="ERROR",
        message="Unhandled application exception",
        error_stack=str(exc),
    )
    return build_error_response(
        status_code=500,
        code=5000,
        message="internal server error",
    )
