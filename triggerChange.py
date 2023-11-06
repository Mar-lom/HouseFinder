import requests
from bs4 import BeautifulSoup
import time
import smtplib
import os
from email.message import EmailMessage

## Call the website
URL = "https://www.remax.ca/on/thunder-bay-real-estate?pageNumber=1"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

houses = soup.find_all("div", class_="listing-card_root__UG576 search-gallery_galleryCardRoot__7HbLb")

def house_loop(houses_class_variable):
    house_link = []
    for house in houses_class_variable:
        get_house_link = house.find("a", href=True)
        house_link.append(get_house_link['href'])
    return house_link

while True:
    #get original house data
    og_houses = house_loop(houses)
    print("Current Houses Houses")
    #wait 10 minutes and call again
    time.sleep(600)
    new_houses = house_loop(houses)
    #compare those values
    nValues = [item for item in new_houses if item not in og_houses]
    if nValues:
        EMAIL_ADDRESS = os.environ.get('google_dev_email')
        EMAIL_PASSWORD = os.environ.get('google_dev_password')

        msg = EmailMessage()
        msg['Subject'] = 'NEW HOME ON THE MARKET!'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = 'mlombardo226@gmail.com '
        msg.set_content(nValues)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)




