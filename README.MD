# Python Telegram Scraping
This module scrapes the data from selected telegram channels or chats using Telethon library. It also includes simple functions for counting words and visualizing their distribution.
## How to get
```
pip install -r requirements.txt
```
You can get your api_id and api_hash here: https://my.telegram.org/apps. \
Set the necessary parameters:
```
username: str = "@username"                                   
api_id: int = 00000
api_hash: str = 'api_hash'

y_max, m_max, d_max = (2024, 3, 1) # maximum date --> year/month/day
y_min, m_min, d_min = (2021, 1, 27)   # minimum date --> year/month/day
 
chat_url: str = "chat url" # Chat url
key_search: str = "search_word" # Your key word or None

output_filename = 'result.xlsx' # None or filename.xlsx
forward_message: bool = False # If true it will save all of the messages in "saved messages" in telegram
```
# Word of caution
**This Telegram scraper is provided for educational and research purposes only.** \
**The developer does not endorse or support any misuse of this tool.**