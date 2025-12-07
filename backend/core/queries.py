CREATE_USER = """
  INSERT INTO WEBUSER (FirstName, LastName, Email, HashedPassword, Salt)
  VALUES(%s, %s, %s, %s, %s)
"""

GET_USER = """
  SELECT FirstName, LastName, Email, HashedPassword, Salt
  FROM WEBUSER
  WHERE Email = %s;
"""