from fastapi import HTTPException, status


class CustomException(Exception):
    def __init__(self, detail: str, status_code: int):
        self.detail = detail
        self.status_code = status_code


class RecordNotFoundError(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )
