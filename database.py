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

user_data_list = []
user_count = 0

def get_user_data(): 
    global user_data_list, user_count
    user_data_list.clear()
    user_count = 0

    with engine.connect() as conn:
        query = text("SELECT name, email FROM flaskdevelopment.userprofiles")
        result = conn.execute(query)

        for row in result:
            user_data = {"Name": row[0], "Email": row[1]}
            user_data_list.append(user_data)
            user_count += 1

    return user_data_list

user_appointment_list = []
appointment_count = 0

def get_user_appointment_data(): 
    global user_appointment_list, appointment_count
    user_appointment_list.clear()
    appointment_count = 0

    with engine.connect() as conn:
        query = text("SELECT * FROM flaskdevelopment.appointments")
        result = conn.execute(query)

        for row in result:
            user_data = {"Name": row[0], "Phone": row[1], "Doctor": row[2], "Email": row[3], "Message": row[4], "status": row[5]}
            user_appointment_list.append(user_data)
            if user_data["status"] == 1:
              continue
            else:
              appointment_count += 1

    return user_appointment_list

def update_appointment_status_in_db(email):
    with engine.connect() as conn:
        query = text("UPDATE flaskdevelopment.appointments SET status = :new_status WHERE email = :email")
        conn.execute(query, {"new_status": 1, "email": email})

appointment_list = []
appointment_count_u = 0

def user_appointment_data(email): 
    global appointment_list, appointment_count_u
    appointment_list.clear()
    appointment_count_u = 0

    with engine.connect() as conn:
        query = text("SELECT * FROM flaskdevelopment.appointments WHERE email = :email")
        result = conn.execute(query, {"email": email})

        for row in result:
            user_data = {"Name": row[0], "Phone": row[1], "Doctor": row[2], "Email": row[3], "Message": row[4], "status": row[5]}
            appointment_list.append(user_data)

            if user_data["status"] == 1:
                appointment_count_u += 1

    return appointment_list


    
