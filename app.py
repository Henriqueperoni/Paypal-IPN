import os
from flask import Flask, render_template, request

import sys
import urllib.parse
import requests


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
    print('Sending request back')
    # Post back to PayPal for validation

    headers = {'content-type': 'application/x-www-form-urlencoded',
               'user-agent': 'Python-IPN-Verification-Script'}
    r = requests.post(VERIFY_URL, params=params, headers=headers, verify=True)
    r.raise_for_status()
    print("Getting final response")
    print(f'Text: {r.text}')
    # Check return message and take action as needed
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
