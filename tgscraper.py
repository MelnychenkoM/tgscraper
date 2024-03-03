from telethon import TelegramClient

from datetime import datetime, timezone
import pandas as pd

class TgScraper:
    def __init__(self, username: str, api_id: int, api_hash: str) -> pd.DataFrame:
        self.__username = username
        self.__api_id = api_id
        self.__api_hash = api_hash


    def scrape_messages(self, chat_url: str, 
                        key_search : str= None, 
                        send_message: bool = False, 
                        date_from=None, # "year/month/day"
                        date_to=None, # "year/month/day"
                        save_to_excel=False,
                        output_filename="scraped_messages.xlsx"):
        
        messages_data = []
        match = 0
        with TelegramClient(self.__username, self.__api_id, self.__api_hash) as client:

            chat_entity = client.loop.run_until_complete(client.get_entity(chat_url))
            chat_name = chat_entity.title

            for message in client.iter_messages(chat_url, search=key_search):
                if date_from and date_to:

                    date_start = datetime(*[int(num) for num in date_from.split('/')], 
                                         tzinfo=timezone.utc)
                    date_end = datetime(*[int(num) for num in date_to.split('/')], 
                                       tzinfo=timezone.utc)

                    if date_start <= message.date <= date_end:
                        messages_data.append(self._process_message(message))
                        match += 1

                    if send_message:
                        client.loop.run_until_complete(message.forward_to('me'))
                else:
                    messages_data.append(self._process_message(message))
                    match += 1

                    if send_message:
                        client.loop.run_until_complete(message.forward_to('me'))

        header = "CHAT SCRAPING"
        output_str = f'Your search with the key "{key_search}" in "{chat_name}" has been completed.\nFound total {match} matches.'
        print_boxed_output(output_str, header)

        df = pd.DataFrame(messages_data)

        if save_to_excel:
            df['Message Date'] = df['Message Date'].dt.tz_convert(None)
            df.to_excel(output_filename)

        return df
    
    def get_all_groups(self, save_to_excel=False,
                       output_filename='all_groups.xlsx') -> pd.DataFrame:

        chat_names = []
        chat_ids = []

        with TelegramClient(self.__username, self.__api_id, self.__api_hash) as client:
            for dialog in client.iter_dialogs():
                if dialog.is_group:
                    chat_names.append(dialog.name)
                    chat_ids.append(str(dialog.id))
            
        df = pd.DataFrame({
            "Chat name": chat_names,
            "Chat id": chat_ids
        })

        if save_to_excel:
            df.to_excel(output_filename)

        header = "GETTING ALL CHATS"
        output_str = f"The search has been completed, and {len(df)} chats have been found."
        print_boxed_output(output_str, header)

        return df
    
    def get_participants(self, chat_url: str,
                         save_to_excel=False,
                         output_filename='participants.xlsx') -> pd.DataFrame:

        user_list = []

        with TelegramClient(self.__username, self.__api_id, self.__api_hash) as client:
            users = client.loop.run_until_complete(client.get_participants(chat_url))
            chat_entity = client.loop.run_until_complete(client.get_entity(chat_url))
            chat_name = chat_entity.title
        
        for user in users:
            sender_username = "@" + user.username if user.username else None
            sender_first_name = user.first_name if user.first_name else None
            sender_last_name = user.last_name if user.last_name else None
            phone = user.phone if user.phone else None

            user_list.append({
                "Username": sender_username,
                "First Name": sender_first_name,
                "Last Name": sender_last_name,
                "Phone Number": phone
            })

        df = pd.DataFrame(user_list)
        if save_to_excel:
            df.to_excel(output_filename)

        header = "GETTING ALL PARTICIPANTS"
        output_str = f"The search has been completed.\nThe number of participants in {chat_name} is {len(df)}"
        print_boxed_output(output_str, header)

        return df

    def _process_message(self, message) -> dict:
            chat_id = str(message.chat_id)[4:]
            message_link = f"https://t.me/c/{chat_id}/{message.id}"

            user = message.sender

            if user:
                sender_username = "@" + user.username if user.username else None
                sender_first_name = user.first_name if user.first_name else None
                sender_last_name = user.last_name if user.last_name else None
                phone = user.phone if user.phone else None
            else:
                sender_username = None
                sender_first_name = None
                sender_last_name = None
                phone = None

            return {
                'MessageID': message.id,
                'Message Date': message.date,
                'Text': message.message,
                'Sender ID': message.sender_id,
                'Sender Username': sender_username,
                'Message Link': message_link,
                'First Name': sender_first_name,
                'Last Name': sender_last_name,
                'Phone Number': phone
            }
    
def print_boxed_output(string, header):
    length = max(len(line) for line in string.split('\n'))
    header_padding = (length - len(header)) // 2
    print("┌" + "─" * (length + 2) + "┐")
    print(f"│ {' ' * header_padding}{header}{' ' * (length - len(header) - header_padding)} │")
    print("├" + "─" * (length + 2) + "┤")
    for line in string.split('\n'):
        print(f"│ {line.ljust(length)} │")
    print("└" + "─" * (length + 2) + "┘")