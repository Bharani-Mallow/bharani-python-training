from database import SessionLocal, get_db_connection
from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from exception import BadRequestError


class DBSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

    async def dispatch(self, request: Request, call_next):

        try:
            db = get_db_connection()
            request.state.db = next(db)
            response = await call_next(request)
        except ValidationError as error:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"message": error.errors()},
            )
        except BadRequestError as error:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": error.errors()},
            )
        finally:
            request.state.db.close()
        return response
