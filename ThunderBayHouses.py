import requests
from bs4 import BeautifulSoup
import time
import smtplib
import os
from email.message import EmailMessage

## Call the website
URL = "https://www.thunderbayhouses.com/viewhouses"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

houses = soup.find_all("div", id="search-results")

print(houses)

# def house_loop(houses_class_variable):
#     house_link = []
#     for house in houses_class_variable:
#         get_house_link = house.find("a", href=True)
#         house_link.append(get_house_link['href'])
#     return house_link
#
# while True:
#     #get original house data
#     og_houses = house_loop(houses)
#     print("Current Houses Houses")
#     #wait 10 minutes and call again
#     time.sleep(600)
#     new_houses = house_loop(houses)
#     #compare those values
#     nValues = [item for item in new_houses if item not in og_houses]
#     if nValues:
#         #append all list values from nValue to list_of_items
#         list_of_items = "\n".join(nValues)
#         EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
#         EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
#         msg = EmailMessage()
#         msg['Subject'] = 'New House on the Market!'
#         msg['From'] = EMAIL_ADDRESS
#         msg['To'] = EMAIL_ADDRESS
#         msg.set_content(list_of_items)
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#             smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#             smtp.send_message(msg)