from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException

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
    service.login(user)
    return {"message": "Logged in successfully"}
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
