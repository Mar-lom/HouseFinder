import json
import requests
from bs4 import BeautifulSoup
import datetime
import time
import smtplib
import os
from email.message import EmailMessage
import re

website_url = "https://www.thunderbayhouses.com/"
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_TO = [EMAIL_ADDRESS] ## change this to the emails you and to send too
def website_call(url)-> str:
    # Call the website
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def json_convert(add_soup):
    soup_dict = json.loads(add_soup.text)
    return soup_dict

def modify_json_listing_date(house_soup): #convert the listing date to a integer for sorting.
    for house in house_soup:
        if house['Listing Date']:
            remove_hyph = re.sub("-", "", house['Listing Date'])
            blah = int(remove_hyph[:8]) ##removes the first 8 characters of the string
            house['Listing Date'] = blah
    return house_soup
def sort_houses(sorted_soup):
    sorted_houses = sorted(sorted_soup,  key=lambda x: x['Listing Date'], reverse=True)
    return sorted_houses

def houses_to_list(json) -> str:
    all_houses = []
    for house in json:
        if house["Property Status"] == "New":
            #all_houses.append(website_url + house['Thumbnail'])
            all_houses.append(house["Address"])
            all_houses.append(house['Price'])
            all_houses.append(website_url + house['Permalink'])
            all_houses.append("House Status: " + house['Property Status'])
            all_houses.append('\n')
    return all_houses

def houses_list_to_string(house_list):
    house_content = '\n'.join(house_list)
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
    json_file = json_convert(website_raw_data)
    modified_file = modify_json_listing_date(json_file)
    sorted_houses = sort_houses(modified_file)
    houses_ready_to_send = houses_list_to_string(houses_to_list(sorted_houses))
    send_email(EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_TO, houses_ready_to_send)

if __name__ == "__main__":
        main()

