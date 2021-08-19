1. Create a PayPal account
2. Create a Developer account
3. Create Sandbox accounts(1 personal, 1 business).
4. Star Flask application
5. Create PayPal button at https://www.sandbox.paypal.com/buttons/
6. Add button to HTML page
7. Create paypal_listener route on your app.py
8. As Paypal does not allow test the IPN in your local machine. You can create a "tunnel" application called [NGROK](https://ngrok.com/) that gives you a test domain.
9. Install NGROK to your local machine.
    - unzip /path/to/ngrok.zip
    - ./ngrok authtoken 1wwrK25FtnKLMBylWVajPHvGcDz_mTc1TEoUX72XEQafMSPd
10. Run NGROK to redirect to you localhost.
    - > ngrok http -host-header=localhost 5000
11. That will give two domains where you can find by typoing in your browser:
    - http://localhost:4040
12. In business sandbox account where you created your button, in the third step (Step 3: Customize advanced features (optional)) add a notify variable in the advanced box:
    - notify_url=<the domain you got from NGROK>/<the route of your listener>
13. How to get data received in flask request
    - https://stackoverflow.com/a/16664376
