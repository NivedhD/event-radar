# Event Radar

A Python app that automatically scrapes websites for new 
tour events, stores them in a SQLite database, and sends 
an email notification when a new event is found.

## Features
- Scrapes websites automatically at a configurable interval
- Stores events in a local SQLite database
- Avoids duplicate notifications using database checks
- Sends email alert with event details when new event found
- Logs all activity to scraper.log

## Setup
1. Clone the repo
2. pip install requests selectorlib python-dotenv
3. Create a `.env` file based on `.env.example`
4. Generate a Gmail App Password at
   myaccount.google.com → Security → App Passwords
5. Add your credentials to `.env`

## Usage
# Start the scraper
python main.py

# View all stored events
python view_events.py

Press Ctrl+C to stop.
