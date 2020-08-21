import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



def send_mail(receiver, link):
    if env == "dev" :
        api_key = os.environ.get('SENDGRID_API_KEY')
    else:
        api_key = process.env.SENDGRID_API_KEY
        sender = "no-reply@vidveda.com"
        message = Mail(
            from_email=(sender,"VID VEDA") ,
            to_emails=receiver,
            subject='TEST MAIL',
            html_content=f'<strong>Hi {receiver}! The link is {link} </strong>')
        try:
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)
            flash('Email Sent')
            return redirect('/forgot')
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            flash('Sorry, but the email linked to this account is invalid')
            return redirect('/forgot')
