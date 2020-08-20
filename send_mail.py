import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



print(os.environ.get('SENDGRID_API_KEY'))

env = "dev"

if env == "dev" :
    api_key = os.environ.get('SENDGRID_API_KEY')
else:
    api_key = process.env.SENDGRID_API_KEY


receiver = "asmita016@gmail.com"
sender = "no-reply@vidveda.com"
message = Mail(
    from_email=(sender,"VID VEDA") ,
    to_emails=receiver,
    subject='TEST MAIL',
    html_content=f'<strong>HI! {receiver} are you getting this? </strong>')
try:
    sg = SendGridAPIClient(api_key)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)



