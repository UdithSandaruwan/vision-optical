from flask import Flask, render_template, request, redirect, url_for, session, send_file
from database import add_user_data_to_db, get_user_auth_data, add_appointment_data_to_db
from firebase import SignUp_user_auth
import database
import authlib
from authlib.integrations.flask_client import OAuth 
import json 
import os
import sender, sender2

app = Flask(__name__)

user={'name':"logged-in-user",
      'email':'login@user.com',
      'password':''
    }

appConf = {
  "client_id": str(os.getenv("client_id")),
  "client_secret":str(os.getenv("client_secret")),
  "meta_url":"https://accounts.google.com/.well-known/openid-configuration",
  "flask_secret":str(os.getenv("flask_secret")),
  "port":5000
}

app.secret_key = appConf["flask_secret"]

oauth = OAuth(app)
oauth.register("visiopOptical",
               client_id=appConf["client_id"],
               client_secret=appConf["client_secret"],
               meta_url=appConf["meta_url"],
               client_kwargs={"scope": "openid email profile https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read"},
               authorize_url="https://accounts.google.com/o/oauth2/auth",
               token_uri="https://oauth2.googleapis.com/token"
              )

Name=None
Email=None
Password=None
Phone=None
Category=None
Message=None

@app.route("/down")
def down():
  return render_template('down.html')

@app.route('/download')
def download_file():
    file_path = 'static/mint.iso'
    return send_file(file_path, as_attachment=True, download_name='mint.iso')


@app.route("/", endpoint='index')
def Home():
  return render_template('index.html')
  
@app.route("/sign-in")
def SignIn():
  pretty=json.dumps(session.get("user"), indent=4)
  return render_template('sign-in.html', session=session.get("user"), pretty=pretty)

@app.route("/google-login")
def googleLogin():
  return oauth.visiopOptical.authorize_redirect(redirect_uri=url_for("googleCallBack", _external=True))

@app.route("/signin-google")
def googleCallBack():
  token = oauth.visiopOptical.authorize_access_token()
  session["user"] =token
  return redirect(url_for("test"))
  
@app.route("/test")
def test():
  return  render_template('test.html', session=session.get("user"), pretty=json.dumps(session.get("user"), indent=4))


@app.route("/sign-up")
def SignUp():
  return render_template('sign-up.html')

@app.route("/user/reg/new", methods=['POST'])
def SignUp_user():
  global Name
  Name=request.form['name']
  global Email
  Email=request.form['email']
  global Password
  Password=request.form['password']
  
  add_user_data_to_db(Name, Email, Password)
  SignUp_user_auth(Name, Email, Password)

  sender2.send(Name, Email)
  return redirect(url_for('SignIn'))

user_name = None
user_email = None
user_password = None

@app.route("/user/rec", methods=['POST'], endpoint='sign_in_user')  
def SignIn_user():
  global Email 
  Email=request.form['email']
  global Password
  Password=request.form['password']
  done=redirect(url_for('admin_dashboard'))

  out=redirect(url_for('SignIn'))
  get_user_auth_data(Email)
  
  done_u = redirect(url_for('user_dashboard'))

  user_email=database.user_data["Email"]
  user_password=database.user_data["Password"]

  if user_email==Email and user_password==Password:
    if "vo" in user_password.lower():
      return done
    else:
      return done_u
  else:
    return out

@app.route("/adminPanel")
def admin_dashboard():
  database.get_user_data()
  user_count = database.user_count
  return render_template('adminPanel.html',user_count=user_count)
  
@app.route("/user/")
def user_dashboard():
  return render_template('single_user.html')

@app.route("/user/reg/appointment", methods=['POST'])  
def Set_Appointment():
  global Name
  Name=request.form['name']
  global Phone
  Phone=request.form['phone']
  global Category
  Category=request.form.get('category')
  global Email
  Email=request.form['email']
  global Message
  Message=request.form['message']
  add_appointment_data_to_db(Name, Phone, Category, Email, Message)
  sender.send(Name, Email)
  return redirect(url_for('index'))

@app.route("/user-pro")
def user_profile():
  return render_template('profile.html')

@app.route("/privacy-policy")
def privacy_policypolicy():
  return render_template('privacypolicy.html')

@app.route("/appointments")
def Appointments():
  user_appointment_list=database.get_user_appointment_data()
  appointment_count = database.appointment_count
  return render_template('appointments.html',user_appointment_list=user_appointment_list, appointment_count=appointment_count)

@app.route("/appointments/u")
def Appointments_u():
  appointment_list=database.user_appointment_data(Email)
  appointment_count = database.appointment_count_u
  return render_template('appointments.html',appointment_list=appointment_list, appointment_count=appointment_count)

@app.route("/users")
def Users():
  user_data_list=database.get_user_data()
  user_count = database.user_count
  return render_template('users.html',user_data_list=user_data_list, user_count=user_count)

@app.route('/user/<email>', methods=['POST'])
def update_status(email):
  Email = email
  database.user_appointment_data(Email)
  return redirect(request.referrer)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)

