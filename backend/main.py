import bcrypt
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from core.database import get_connection
from core.queries import CREATE_USER, GET_USER
from models.user import CreateUser, LoginUser, User

app = FastAPI()

origins = [
  "http://localhost:3000",
  "*"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.post("/signup")
def create_user(user: CreateUser):
  try:
    conn = get_connection()
  except Exception:
    raise HTTPException(
      status_code=500,
      detail="Database connection failed"
    )
  
  try:
    with conn.cursor() as cur:
      salt = bcrypt.gensalt()
      hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)
      cur.execute(
        CREATE_USER,
        (
          user.first_name,
          user.last_name,
          user.email,
          hashed_password.decode(),
          salt
        )
      )
      conn.commit()
  except Exception:
    conn.rollback()
    raise HTTPException(
      status_code=500,
      detail="Database insertion failed"
    )
  finally:
    conn.close()


@app.post("/login")
def login(user: LoginUser):
  try:
    conn = get_connection()
  except Exception:
    raise HTTPException(
      status_code=500,
      detail="Database connection failed"
    )
  
  try:
    with conn.cursor() as cur:
      cur.execute(GET_USER, (user.email,))

      current_user = cur.fetchone()

      # if user does not exist
      if not current_user:
        raise HTTPException(
          status_code=404,
          detail="User not found"
        )
      
      # if password doesn't match
      is_authenticated = bcrypt.checkpw(password=user.password.encode(), hashed_password=current_user[-2].encode())
      if not is_authenticated:
        raise HTTPException(
          status_code=401,
          detail="Password do not match"
        )
      
      return {"success": True}
  except HTTPException as e:
    raise HTTPException(
      status_code=e.status_code,
      detail=e.detail
    )
  except Exception as e:
    print(e)
    raise HTTPException(
      status_code=500,
      detail=repr(e)
    )
  finally:
    conn.close()