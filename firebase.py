import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import random

feedback_auth_signin=None

cred = credentials.Certificate("dsefinalproject-vision-optical-firebase-sdk.json")
firebase_admin.initialize_app(cred)

random_number = ''.join(random.choices('0123456789', k=10))

def SignUp_user_auth(n, e, p):
  email = e
  password = p
  name = n
  try:
    user = auth.create_user(email = email, password = password)
    feedback_auth_signup=1
  except:
    exceptionmsg="Already Exists"
    feedback_auth_signin=0
  print("user created successfully : {0}".format(user.uid))



