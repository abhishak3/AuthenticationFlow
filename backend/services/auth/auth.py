import bcrypt
from fastapi import Depends, HTTPException, status

from models.user import CreateUser, LoginUser
from repositories.user import UserRepository

from .exceptions import InvalidLogin, UserAlreadyExists, UserNotFound

class AuthService:
  def __init__(self, repo: UserRepository = Depends()):
    self.repo = repo

  def signup(self, user: CreateUser):
    # check if user already exists
    current_user = self.repo.get_user_by_email(user.email)
    if current_user:
      raise UserAlreadyExists()

    # generate hashed password and salt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode(), salt)

    # create new user
    self.repo.create_user(
      user.first_name,
      user.last_name,
      user.email,
      hashed_password.decode()
    )

  def login(self, user: LoginUser):
    current_user = self.repo.get_user_by_email(user.email)

    # check if user exists through email
    if not current_user:
      raise UserNotFound()
    
    # authenticate password
    is_authenticated = bcrypt.checkpw(user.password.encode(), current_user.hashed_password.encode())
    if not is_authenticated:
      raise InvalidLogin()
    
    return current_user
