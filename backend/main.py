import bcrypt
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from core.database import get_connection
from core.queries import CREATE_USER
from models.user import CreateUser

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
      print(salt)
      hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)
      cur.execute(
        CREATE_USER,
        (
          user.first_name,
          user.last_name,
          user.email,
          hashed_password,
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