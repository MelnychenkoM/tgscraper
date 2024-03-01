# Python Telegram Scraping
This module scrapes the data from selected telegram channels or chats using Telethon library. It also includes simple functions for counting words and visualizing their distribution.
## How to use
```
git clone https://github.com/MelnychenkoM/tgscraper.git
cd tgscraper
pip install -r requirements.txt
```
You can get your api_id and api_hash here: https://my.telegram.org/apps. \
Set the necessary parameters:
```
username: str = "@username"                                   
api_id: int = 00000
api_hash: str = 'api_hash'

y_min, m_min, d_min = (2021, 1, 27)   # from date --> year/month/day
y_max, m_max, d_max = (2024, 3, 1) # to date (excluding) --> year/month/day
 
chat_url: str = "chat url" # String with chat url or int chat id
key_search: str = "search_word" # Your keyword or None

output_filename = 'result.xlsx' # None or filename.xlsx
forward_message: bool = False # If true, it will save all of the messages in the 'Saved Messages' section inside the Telegram app.
get_chats = False # Creates an excel spreadsheet with all your groups
```
## Word of caution
**This Telegram scraper is provided for educational and research purposes only.** \
**The developer does not endorse or support any misuse of this tool.**