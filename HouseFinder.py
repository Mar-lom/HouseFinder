import json
import requests
from bs4 import BeautifulSoup
import datetime
import time
import smtplib
import os
from email.message import EmailMessage

website_url = "https://www.thunderbayhouses.com/"
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_TO = [EMAIL_ADDRESS] ## change this to the emails you and to send too
def website_call(url)-> str:
    # Call the website
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def houses_to_list(raw_scraped_data) -> str:
    load_json = json.loads(raw_scraped_data.text)
    house_picture = []
    house_address = []
    house_price = []
    house_website_link = []
    all_houses = []
    for house in load_json:
        if house["Property Status"] == 'New':
            #all_houses.append(website_url + house['Thumbnail'])
            all_houses.append(house["Address"])
            all_houses.append(house['Price'])
            all_houses.append(website_url + house['Permalink'])
            all_houses.append("House Status: " + house['Property Status'])
            all_houses.append('\n')
    house_content = '\n'.join(all_houses)
    return house_content
def send_email(email_from, email_password, email_to, houses_string):
    msg = EmailMessage()
    msg['Subject'] = 'Good Morning Homie 🏡🤖'
    msg['From'] = email_from
    msg['To'] = email_to
    msg.set_content(houses_string)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
def main():
    website_raw_data = website_call("https://www.thunderbayhouses.com/cache/listings.json?nocache")
    houses_list = houses_to_list(website_raw_data)
    send_email(EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_TO, houses_list)

if __name__ == "__main__":
        main()

