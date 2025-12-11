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

  return jwt.encode(
    to_encode,
    settings.JWT_SECRET,
    algorithm=settings.JWT_ALGORITHM,
  )

def generate_refresh_token(data: dict):
  to_encode = data.copy()

  # adding expiration time
  expire = (datetime.now(timezone.utc)
        + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS))
  
  to_encode["exp"] = expire
  to_encode["type"] = "refresh"

  return jwt.encode(
    to_encode,
    settings.JWT_SECRET,
    algorithm=settings.JWT_ALGORITHM,
  )

def decode_token(token: str) -> dict:
  return jwt.decode(
    token,
    settings.JWT_SECRET,
    algorithms=[settings.JWT_ALGORITHM]
  )
