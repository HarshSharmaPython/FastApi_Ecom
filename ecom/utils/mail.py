from email.message import EmailMessage
import ssl
import smtplib

def send_mail(from_email, to_email, body, password, subject):
    msg = EmailMessage()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.set_content(body, subtype='html')

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP('smtp.zoho.in', 587) as smtp:
            smtp.starttls(context=context)
            smtp.login(from_email, password)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# send_mail(from_email="charvi@fglawkit.com",
#           to_email="2003jaindarshan@gmail.com",
#           body="<p>This is a sample body</p>",
#           password="casiosa78",
#           subject="This is a subject")

