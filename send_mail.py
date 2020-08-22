import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from boto.s3.connection import S3Connection
from flask import Flask, render_template, url_for, request, redirect, flash



env = "dev"

def send_mail(receiver, link):
    

    api_key = os.environ.get('SENDGRID_API_KEY')
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

