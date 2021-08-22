1. Create a PayPal account
2. Create 2 Sandbox accounts(1 personal, 1 business) on https://www.sandbox.paypal.com/buttons/
3. Create PayPal button at https://www.sandbox.paypal.com/buttons/
    - 3.1 It's also possible to use the PayPal IPN Simulator to send the message from the PayPal sandbox account to the URL which the listener is running.
4. Add button to HTML page
5. Create paypal_listener route on your app.
6. As Paypal does not allow test the IPN in your local machine. You can create a "tunnel" application called [NGROK](https://ngrok.com/) that gives you a test domain.
7. Install NGROK to your local machine.
    - unzip /path/to/ngrok.zip
    - ./ngrok authtoken 1wwrK25FtnKLMBylWVajPHvGcDz_mTc1TEoUX72XEQafMSPd
8. Run NGROK to redirect to your localhost.

```
    ngrok http -host-header=localhost 5000
```

9. That will give two domains where you can find by typing in your browser:
    - http://localhost:4040
10. In the business sandbox account where you created your button, in the third step (Step 3: Customize advanced features (optional)) add a notify variable in the advanced box:

```
    notify_url=<the domain you got from NGROK>/<the route of your listener>
```

11. How to get data received in flask request
    -   https://stackoverflow.com/a/16664376
12. You will get an ImmutableMultiDict and have to modify it into a dictionary with the built-in method `to_dict`.
13. Add a new key and value to the dictionary.

```
params['cmd'] = '_notify_validate'
```

14. Send it back to PayPal.

```
r = requests.post(VERIFY_URL, params=params, headers=headers, verify=True)
```

15. With the 'VERIFIED' message back it will mean everything worked fine and you are able to continue.
