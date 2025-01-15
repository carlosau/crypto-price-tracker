import requests
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()
# Email credentials
sender_email = os.getenv('sender_email')
password = os.getenv('password')
receiver_email = os.getenv('receiver_email')

# Function to fetch the current price of cryptocurrency
def get_crypto_price(crypto_id='bitcoin', currency='usd'):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={currency}'
    response = requests.get(url)
    data = response.json()
    return data[crypto_id][currency]

# Function to send email alert
def send_email_alert(crypto, price, threshold):
    subject = f'{crypto.capitalize()} Price Alert!'
    body = f'The price of {crypto} has exceeded your threshold of {threshold}. Current price: ${price}.'

    # Create the email
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, "plain"))

