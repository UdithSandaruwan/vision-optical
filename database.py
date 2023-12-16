from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()
import os

host= str(os.getenv("DB_HOST"))
user=str(os.getenv("DB_USERNAME"))
passwd= str(os.getenv("DB_PASSWORD"))
db= str(os.getenv("DB_NAME"))

db_connection_string = "mysql+pymysql://" + user + ":" + passwd + "@" + host + "/" + db + "?charset=utf8mb4"


engine = create_engine(db_connection_string, connect_args={"ssl": {"ssl_ca": "/etc/ssl/cert.pem"}})

def add_user_data_to_db(name, email, password):
    with engine.connect() as conn:
        query = text("INSERT INTO flaskdevelopment.userprofiles (name, email, password) VALUES(:name, :email, :password)")
        conn.execute(query, {"name": name, "email": email, "password": password})

user_data = {}  

def get_user_auth_data(email):
    with engine.connect() as conn:
        query = text("SELECT name, email, password FROM flaskdevelopment.userprofiles WHERE email = :email")
        result = conn.execute(query, {"email": email})

        

        for row in result:
          user_data["Name"] = row[0]
          user_data["Email"] = row[1]
          user_data["Password"] = row[2]
      
        return user_data

def add_appointment_data_to_db(name, phone, category, email, message):
  with engine.connect() as conn:
      query = text("INSERT INTO flaskdevelopment.appointments VALUES(:name, :phone, :category, :email, :message)")
      conn.execute(query, {"name": name, "phone": phone, "category": category, "email": email, "message": message})


