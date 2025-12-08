from typing import Optional
from fastapi import HTTPException

from core.database import get_connection
from models.user import User

class UserRepository:
  def get_user_by_email(self, email: str) -> Optional[User]:
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            GET_USER_BY_EMAIL = (
              "SELECT FirstName, LastName, Email, HashedPassword " +
              "FROM WEBUSER WHERE Email = %s;"
            )

            cur.execute(GET_USER_BY_EMAIL, (email,))

            row = cur.fetchone()

            if not row:
                return None
            
            user_dict = {
              "first_name": row[0],
              "last_name": row[1],
              "email": row[2],
              "hashed_password": row[3]
            }

            return User(**user_dict)
    finally:
        conn.close()
  
  def create_user(self, first_name: str, last_name: str, email: str, hashed_password: str) -> None:
    conn = get_connection()

    try:
      with conn.cursor() as cur:
           CREATE_USER = (
            "INSERT INTO WEBUSER (FirstName, LastName, Email, HashedPassword)" +
            "VALUES(%s, %s, %s, %s)"
           )

           cur.execute(CREATE_USER, (
              first_name,
              last_name,
              email,
              hashed_password
           ))

           conn.commit()
    except Exception:
       raise HTTPException(status_code=500, detail="DB insertion failed")
    finally:
      conn.close()
