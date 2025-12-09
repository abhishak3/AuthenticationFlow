"""Security utilities for token creation.

This module provides helpers for working with JSON Web Tokens (JWTs)
used by the authentication flow.
"""

import jwt
from datetime import datetime, timedelta, timezone

from core.config import settings

def generate_access_token(data: dict):
  to_encode = data.copy()

  # adding expiration time
  expire = (datetime.now(timezone.utc)
        + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))

  # "exp" and some others keys are already claimed by jwt
  # https://pyjwt.readthedocs.io/en/stable/usage.html#registered-claim-names
  to_encode["exp"] = expire

  encoded_jwt = jwt.encode(
    to_encode,
    settings.JWT_SECRET,
    algorithm=settings.JWT_ALGORITHM,
  )

  return encoded_jwt

def decode_access_token(token: str) -> dict:
  return jwt.decode(
    token,
    settings.JWT_SECRET,
    algorithms=[settings.JWT_ALGORITHM]
  )
