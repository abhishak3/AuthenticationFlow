from fastapi import FastAPI

from core.database import get_connection

app = FastAPI()

@app.get("/")
def home():
  conn = get_connection()
  cur = conn.cursor()
  cur.execute("SELECT NOW();")
  result = cur.fetchone()
  cur.close()
  conn.close()
  return {"Hello": result}
