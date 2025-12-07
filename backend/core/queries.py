CREATE_USER = """
  INSERT INTO WEBUSER (FirstName, LastName, Email, HashedPassword, Salt)
  VALUES(%s, %s, %s, %s, %s)
"""
