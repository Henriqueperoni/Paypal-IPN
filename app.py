import os
from os import path
if path.exists("env.py"):
    import env
from flask import Flask, render_template, request
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/paypal_listener", methods=["GET", "POST"])
def paypal_listener():
    VERIFY_URL_PROD = 'https://ipnpb.paypal.com/cgi-bin/webscr'
    VERIFY_URL_TEST = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'

    # Switch as appropriate
    VERIFY_URL = VERIFY_URL_TEST

    print('Receiving IPN')
    # Read and parse query string
    params = (request.form).to_dict()

    # Add '_notify-validate' parameter
    params['cmd'] = '_notify-validate'
    print(params)

    print('Sending request back')
    # Post back to PayPal for validation

    headers = {'content-type': 'application/x-www-form-urlencoded',
               'user-agent': 'Python-IPN-Verification-Script'}

    r = requests.post(VERIFY_URL, params=params, headers=headers, verify=True)
    # r.raise_for_status()
    print("Getting final response")
    print(f'Text: {r.text}')
    print('Sending email')
    # Check return message and take action as needed

    # PayPal response variables
    payerFirstName = params['first_name']
    payerLastName = params['last_name']
    payer_email = params['payer_email']
    item_name = params['item_name']
    quantity = params['quantity']
    price = params['mc_gross']
    currency = params['mc_currency']
    invoice = params['invoice']

    """
    Sending confirmation email adapted from:
    #https://realpython.com/python-send-email/ and
    https://stackoverflow.com/a/882770
    """
    # Email variables
    sender_email = os.environ.get('EMAIL_HOST_USER')
    receiver_email = payer_email
    password = os.environ.get('PASSWORD')

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Payment confirmation of invoice {invoice} on PayPal"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = f"""\
Hi {payerFirstName},

Thanks for choosing PayPal for your payment method.
The payment of the {item_name} has been verified and \
successfully completed for {currency}{price}.


Regards,
PayPal Team
"""

    # Turn these into plain/ MIMEText objects
    messageBody = MIMEText(text, "plain")

    # Add plain-text parts to MIMEMultipart message
    message.attach(messageBody)

    # Send the message via local SMTP server.
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )

    if r.text == 'VERIFIED':
        print('VERIFIED')

    elif r.text == 'INVALID':
        print('INVALID')
    else:
        pass
    return 'paypal'


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
