from tgscraper import TgScraper

username: str = "@username"                                   
api_id: int = 234324324324
api_hash: str = 'api_hash'

scraper = TgScraper(username, api_id, api_hash)

scraper.get_all_groups()
scraper.get_participants(chat_id)
scraper.scrape_messages(chat_id, "car", save_in_exel=True)
