from pydantic import BaseModel, Field
from typing import Optional

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error description")
    code: Optional[str] = Field(None, description="Error code")

class BadRequestError(ErrorResponse):
    pass

class UnauthorizedError(ErrorResponse):
    pass

class ForbiddenError(ErrorResponse):
    pass

class NotFoundError(ErrorResponse):
    pass

class RateLimitExceededError(ErrorResponse):
    detail: str = "Rate limit exceeded"

class InternalServerError(ErrorResponse):
    detail: str = "Internal server error"
