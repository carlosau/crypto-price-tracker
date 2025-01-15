import requests
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Function to fetch the current price of cryptocurrency
def get_crypto_price(crypto_id='bitcoin', currency='usd'):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={currency}'
    response = requests.get(url)
    data = response.json()
    return data[crypto_id][currency]

# Function to send email alert
def send_email_alert(crypto, price, threshold):
    # Email credentials
    sender_email = os.getenv('SENDER_EMAIL')
    password = os.getenv('PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    
    subject = f'{crypto.capitalize()} Price Alert!'
    body = f'The price of {crypto} has exceeded your threshold of {threshold}. Current price: ${price}.'

    # Create the email
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, "plain"))

    # Connect to Gmail SMTP Server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f'Alert sent to {receiver_email}')
    except Exception as e:
        print(f'Error sending email: {e}')

# Function to check price and alert if necessary
def check_and_alert(crypto='bitcoin', threshold=50000):
    try:
        price = get_crypto_price(crypto)
        print(f'Current {crypto} price: ${price}')
        if price >= threshold:
            send_email_alert(crypto, price, threshold)
    except Exception as e:
        print(f'Error fetching data: {e}')

# Schedule the task to check prices every 5 minutes
schedule.every(5).minutes.do(check_and_alert, crypto='bitcoin', threshold=50000)

# Run the script continuously
while True:
    print('checking prices...')
    schedule.run_pending()
    time.sleep(1)