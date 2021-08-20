import os
from flask import Flask, render_template, request
import requests
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)


@app.route("/")
def index():
    import sys
    print(sys.path)
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
    payerFirstName = params['first_name']
    payerLastName = params['last_name']
    payer_email = params['payer_email']
    item_name = params['item_name']
    quantity = params['quantity']
    price = params['mc_gross']
    invoice = params['invoice']

    sender_email = "henriqueperoni94@gmail.com"
    receiver_email = payer_email
    password = ''

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = """\
    <html>
    <body>
        <p>Hi,<br>
        How are you?<br>
        <a href="http://www.realpython.com">Real Python</a>
        has many great tutorials.
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    message = f'Hi {payerFirstName} Your purchase went all good\
        \n\n{payerLastName} that is your last name and\nYou bough \
        {quantity}x €{item_name} at {price}\n\
            That is your invoice ID: {invoice}'

    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # print('email sent')
    # server.starttls()
    # print('email sent1')
    # server.login("henriqueperoni94@gmail.com", "")
    # print('email sent2')
    # server.sendmail("henriqueperoni94@gmail.com", payer_email, message)
    # print('email sent3')
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
