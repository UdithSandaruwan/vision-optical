from dbm import _Database
from email.message import EmailMessage
import random
import ssl
import smtplib
from datetime import datetime, timedelta
from fpdf import FPDF
from io import BytesIO
from flask import make_response
import schedule
import time
from sqlalchemy import create_engine, text

# Replace these with your actual credentials
email_sender = "binanceworkspace0@gmail.com"
email_password = "npny fonr kcvv wujd"

# Database connection
engine = create_engine("your_database_connection_string")

def generate_appointment_id():
    return random.randrange(10**7, 10**8)

def send_appointment_report(name, email, pdf_content):
    email_receiver_name = name
    email_receiver = email

    email_subject = "Daily Appointment Report"

    email_body = f"""
    Dear {email_receiver_name},

    Attached is the daily appointment report for {name}.

    Best regards,
    Your Clinic
    """

    msg = EmailMessage()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = email_subject
    msg.set_content(email_body)

    # Attach the PDF
    msg.add_attachment(pdf_content, maintype='application', subtype='pdf', filename=f'report_for_{name}.pdf')

    # Set the context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(msg)

    print(f"Email sent successfully to {email_receiver}!")

def generate_pdf(selected_doctor, appointment_data):
    pdf = FPDF(orientation='L')
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, f"Report of {selected_doctor}", ln=True, align='C')

    header = ["Name", "Phone", "Doctor", "Email", "Message", "status"]
    max_widths = [pdf.get_string_width(col) for col in header]

    for row in appointment_data:
        for i, col in enumerate(header):
            max_widths[i] = max(max_widths[i], pdf.get_string_width(str(row[col])))

    for i, col in enumerate(header):
        pdf.cell(max_widths[i] + 6, 10, col, border=1)
    pdf.ln()

    for row in appointment_data:
        for i, col in enumerate(header):
            pdf.cell(max_widths[i] + 6, 10, str(row[col]), border=1)
        pdf.ln()

    pdf_output = BytesIO(pdf.output(dest='S').encode('latin1'))
    return pdf_output

def job():
    doctors = ["B Balalla", "K Hettiarachchi", "Naveen Herath"]  # Add all the doctors you want to include
    for doctor in doctors:
        appointment_data = _Database.doc_appointment_data(doctor)
        if appointment_data:
            pdf_content = generate_pdf(doctor, appointment_data)
            send_appointment_report(doctor, "admin@gmail.com", pdf_content)

# Schedule the job to run daily at 8:00 PM
schedule.every().day.at("20:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
