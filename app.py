import requests
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to fetch the current price of cryptocurrency
def get_crypto_price(crypto_id='bitcoin', currency='usd'):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={currency}'
    response = requests.get(url)
    data = response.json()
    return data[crypto_id][currency]