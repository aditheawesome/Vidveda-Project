import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from boto.s3.connection import S3Connection
from flask import Flask, render_template, url_for, request, redirect, flash


env = "dev"


def send_app_mail(name, gender, age, email, issue, date):

    api_key = os.environ.get('SENDGRID_API_KEY')
    sender = "no-reply@vidveda.com"
    message = Mail(
        from_email=(sender, "VID VEDA"),
        to_emails=[email, "support@vidveda.com"],
        subject=f'Hi! {name}, Your Appointment is confirmed',
        html_content=f'<strong> Hi {name}! Your appointment for date {date} is confirmed, Please review your details <strong> <br> Name: {name} <br> email: {email} <br> Age: {age} <br> gender: {gender} <br> issue: {issue} <br> date: {date} <p> Please note that you will be charged $20 for the consultation, You can pay the amount via venmo after the consultation call. We also schedule medicine delivery service if needed as per your request for extra cost<p> <br> <br> Team VIDVEDA')
    sg = SendGridAPIClient(api_key)

    try:
        response = sg.send(message)
        print('Email Sent')
        return redirect('/schedule')
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print(e)
        return redirect('/schedule')
