from pydantic import BaseModel

class UserPayload(BaseModel):
  sub: str
  exp: str
