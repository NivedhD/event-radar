import requests
import selectorlib
import smtplib
import ssl
import os
import time
import sqlite3
import logging
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

URLS = [
    "http://programmer100.pythonanywhere.com/tours/",
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/39.0.2171.95 Safari/537.36'}

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        band TEXT,
        city TEXT,
        date TEXT
    )
""")
connection.commit()

def scrape(url):
    """Scrape the page source from the url"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source

def extract(source):
    """Extract the data from the page source using selectorlib"""
    extractor =selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def send_email(message):
    """Send email notification for new tour event"""
    host = "smtp.gmail.com"
    port = 465
    username = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")
    context = ssl.create_default_context()

    email_message = EmailMessage()
    email_message["Subject"] = "New Tour Event Found!"
    email_message["From"] = username
    email_message["To"] = receiver
    email_message.set_content(message)

    try:
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, email_message.as_string())
        print("Email sent!")
        logging.info("Email notification sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        logging.error(f"Email failed: {e}")

def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor.execute("INSERT INTO events VALUES (?,?,?)", row)
    connection.commit()
    logging.info(f"New event stored: {extracted}")
    print(f"Stored: {extracted}")

def read(extracted): 
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor.execute(
        "SELECT * FROM events WHERE band = ? AND city = ? AND date = ?",
        (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows

if __name__ == "__main__":
    logging.info("Scraper started")
    print("Scraper started...")

    try:
        while True:
            try:
                for url in URLS:
                    scraped = scrape(url)
                    extracted = extract(scraped)
                    print(extracted)

                    if extracted != "No upcoming tours":
                        logging.info(f"Event found: {extracted}")
                        row = read(extracted)
                        if not row:
                            store(extracted)
                            send_email(message=f"Hey, New event was found!: {extracted}")
                    else:
                        logging.info("No upcoming tours found")

            except Exception as e:
                print(f"Error during scrape cycle: {e}")            
                logging.error(f"Scrape cycle error: {e}")

            time.sleep(int(os.getenv("SCRAPE_INTERVAL", 60)))  

    except KeyboardInterrupt:
        print("\nScraper stopped.")
        logging.info("Scraper stopped by user")
        connection.close() 