import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from icecream import ic
from pymongo import MongoClient
import certifi 
from dotenv import load_dotenv
import os
import schedule
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''

def send_email(receiver_email, subject, body):
    try:
        # Set up the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Email body
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Replace with your email provider's SMTP server
            server.starttls()  # Start TLS encryption
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Log in to the email account
            print("Logged in successfully")
            server.send_message(msg)  # Send the email

        print(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# send_email("souravsharma7976@gmail.com", "Test Email", "This is a test email from Python")


# Connect to MongoDB with SSL Certificate
try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    # exit()

# Database and collection
db = client["amazon_product"] # Replace with your database name
collection = db["update_daily"] # Replace with your collection name


def scrape_and_track():
    driver = webdriver.Chrome()  # Replace with the correct path to your chromedriver

    driver.get("https://www.amazon.in/s?bbn=1388921031&rh=n%3A1388921031%2Cp_89%3AboAt&_encoding=UTF8&content-id=amzn1.sym.82b20790-8877-4d70-8f73-9d8246e460aa&pd_rd_r=8783cbcc-a3cd-4c85-b0c2-84f18738af10&pd_rd_w=OQITD&pd_rd_wg=WcHBy&pf_rd_p=82b20790-8877-4d70-8f73-9d8246e460aa&pf_rd_r=EFQ9BDGH3D19AP3P9H8N&ref=pd_hp_d_atf_unk")  # Replace with Facebook URL if needed
    time.sleep(5)

    try:
        prices = driver.find_elements(By.XPATH, "//span[@class='a-price']")
        names = driver.find_elements(By.XPATH, "//h2[@class='a-size-base-plus a-spacing-none a-color-base a-text-normal']")
        links = driver.find_elements(By.XPATH, "//a[@class='a-link-normal s-line-clamp-4 s-link-style a-text-normal']")

        for index, (price, name, link) in enumerate(zip(prices, names, links), start=1):
            price_text = price.text.strip()
            name_text = name.text.strip()
            link_text = link.get_attribute("href")

            print(f"{index} Name: {name_text}, Price: {price_text}, Link: {link_text}")

            # Check if the document already exists
            existing_document = collection.find_one({"name": name_text})

            if existing_document:
                if existing_document["price"] != price_text:
                    # If price is different, update it
                    # print(f"Alert: Price change detected for '{name_text}'. Current price is {price_text} and previous price was {existing_document['price']}")
                    send_email("souravsharma7976@gmail.com", "Price Change Alert", f"Price change detected for '{name_text}'. Current price is {price_text} and previous price was {existing_document['price']} and product link is {link_text}")
                    collection.update_one(
                        {"name": name_text},  # Filter criteria
                        {"$set": {"price": price_text}}  # Update operation
                        # {"link": link_text} # Update link
                    )
                    print("Data updated successfully in the database")
                else:
                    print("Data already exists with the same price. No update needed.")
            else:
                # If the document doesn't exist, insert new data
                collection.insert_one({"name": name_text, "price": price_text})  #, "link": link_text
                print("Data inserted successfully")
    except Exception as e:
        print(f"Error occurred: {e}")

schedule.every().day.at("15:33").do(scrape_and_track)

while True:
    schedule.run_pending()
    time.sleep(1)

# scrape_and_track()
