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
from tgscraper import TgScraper

username: str = "@username"                                   
api_id: int = 34534535345
api_hash: str = 'api_hash'


scraper = TgScraper(username, api_id, api_hash)
# You can get all your chats and their corresponding ids using get_all_groups method
scraper.get_all_groups(save_in_excel=True) 
# Find all messsages in the chat containing the key word
scraper.scrape_messages(chat_id, 
                        "car", 
                        date_from="2024/01/01", 
                        date_to="2024/03/02", 
                        save_in_exel=True
                        )


scraper.get_participants(chat_id, save_in_excel=True)
```
## Word of caution
**This Telegram scraper is provided for educational and research purposes only.** \
**The developer does not endorse or support any misuse of this tool.**