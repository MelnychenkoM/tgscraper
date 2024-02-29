from telethon import TelegramClient

from datetime import datetime, timezone
import pandas as pd

# REDO WITH ASYNCIO LATER

# =================== PARAMETERS =========================

username: str = "@username"                                   
api_id: int = 00000
api_hash: str = 'api_hash'

y_max, m_max, d_max = (2024, 3, 1) # maximum date --> year/month/day
y_min, m_min, d_min = (2021, 1, 27)   # minimum date --> year/month/day

chat_url: str = "chat url" 
key_search: str = "search_word"

# --------------------------------------------------------

output_filename = 'result.xlsx' # None or example.xlsx
forward_message: bool = False

# ========================================================

def find_key_in_chat(chat_url: str, key_search: str, send_message: bool = False):
    
    """ Find messages containing key word. """
    index = 0
    messages_id = []
    messages_date = []
    messages = []
    messages_sender_id = []
    messages_sender_username = []
    message_links = []
    first_names = []
    last_names = []
    phone_numbers = []

    with TelegramClient(username, api_id, api_hash) as client:

        match = 0

        for message in client.iter_messages(chat_url, key_search):

            chat_id = str(message.chat_id)[4:]

            if message.date < datetime(y_max, m_max, d_max, tzinfo=timezone.utc) and message.date > datetime(y_min, m_min, d_min, tzinfo=timezone.utc):

                match += 1

                message_link = f"https://t.me/c/{chat_id}/{message.id}"

                messages_id.append(message.id)
                messages_date.append(message.date)
                messages.append(message.message)
                messages_sender_id.append(message.sender_id)
                message_links.append(message_link)

                user = message.sender

                if user:
                    sender_username = "@" + user.username if user.username else "None"
                    sender_first_name = user.first_name if user.first_name else "None"
                    sender_last_name = user.last_name if user.last_name else "None"
                    phone = user.phone if user.phone else "None"

                else:
                    sender_username = 'None'
                    sender_first_name = 'None'
                    sender_last_name = 'None'
                    phone = 'None'

                messages_sender_username.append(sender_username)
                first_names.append(sender_first_name)
                last_names.append(sender_last_name)
                phone_numbers.append(phone)

                if send_message:
                    client.loop.run_until_complete(message.forward_to('me'))

    
    df = pd.DataFrame({
        "Date": messages_date,
        # "Message ID": messages_id,
        "Message": messages,
        # "Sender ID": messages_sender_id,
        "Username": messages_sender_username,
        "First Name": first_names,
        "Last Name": last_names,
        "Phone Number": phone_numbers,
        "Message Link": message_links
    })

    print("=" * 80)
    print(f'Your search with the key "{key_search}" in "{chat_url}" has been completed.')
    print(f"Found total {match} matches.")
    print("=" * 80)

    return df


def save_to_excel(df: pd.DataFrame, filename: str):
    df['Date'] = df['Date'].dt.tz_convert(None)
    df.to_excel(filename, index=False)

if __name__ == '__main__':
    df = find_key_in_chat(chat_url, key_search, forward_message)

    if output_filename is not None:
        save_to_excel(df, output_filename)



