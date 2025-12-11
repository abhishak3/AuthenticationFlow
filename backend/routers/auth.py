from typing import Annotated
from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from jwt import ExpiredSignatureError

from core.security import generate_access_token, generate_refresh_token, decode_token
from core.config import settings
from services.auth import AuthService, UserAlreadyExists, UserNotFound, InvalidLogin
from models.user import CreateUser, LoginUser

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: CreateUser, service: Annotated[AuthService, Depends()]):
  try:
    service.signup(user)
    return {"message": "User created successfully"}
  except UserAlreadyExists:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail="User with email id already exists"
    )

@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: LoginUser, service: Annotated[AuthService, Depends()]):
  try:
    user = service.login(user)
  except UserNotFound:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User with provided email not found"
    )
  except InvalidLogin:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid credentials"
    )
  
  access_token = generate_access_token({"sub": user.email})
  refresh_token = generate_refresh_token({"sub": user.email})

  response = JSONResponse({
    "access_token": access_token,
    "token_type": "bearer" # NOTE: can explore this further
  })

  response.set_cookie(
    key="refresh_token",
    value=refresh_token,
    httponly=True,
    samesite="lax",
    secure=True,
    max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
  )

  return response

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout():
  response = JSONResponse({ "message": "Logged out successfully" })
  response.delete_cookie("refresh_token")
  return response

@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh(request: Request):
  refresh_token = request.cookies.get("refresh_token")

  if not refresh_token:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Request token is missing"
    )
  
  try:
    payload = decode_token(refresh_token)
  except ExpiredSignatureError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Refresh token is expired"
    )
  except Exception:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid refresh token"
    )
  
  if payload.get("type") != "refresh":
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid refresh token"
    )
  
  new_access_token = generate_access_token({"sub": payload["sub"]})

  # rotate refresh token
  new_refresh_token = generate_refresh_token({"sub": payload["sub"]})

  response = JSONResponse({
    "access_token": new_access_token,
    "token_type": "bearer" # NOTE: can explore this further
  })

  response.set_cookie(
    key="refresh_token",
    value=new_refresh_token,
    httponly=True,
    samesite="lax",
    secure=True,
    max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
  )

  return response
