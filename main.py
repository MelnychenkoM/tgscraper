from telethon import TelegramClient
from datetime import datetime, timezone
import pandas as pd
import argparse

# =================== PARAMETERS =========================

username: str = "@username"                                   
api_id: int = 000000000
api_hash: str = 'api_hash'

y_max, m_max, d_max = (2024, 3, 1) # maximum date --> year/month/day
y_min, m_min, d_min = (2024, 2, 27)   # minimum date --> year/month/day

chat_url: str = "chat_url" 
key_search: str = "машина"

# --------------------------------------------------------

save_in_excel: bool = False
search: str = "group" # group or channel
output_filename = None # None or example.xlsx
forward_message: bool = True

# ========================================================

def find_key_in_channel(channel: str, key_search: str, send_message: bool = True):
    index = 0
    messages_id = []
    messages_date = []
    messages = []
    message_links = []

    with TelegramClient(username, api_id, api_hash) as client:

        # current_time = datetime.now()
        # client.loop.run_until_complete(client.send_message('me', f'Hello, myself! {current_time:%H:%M:%S}'))
        
        for message in client.iter_messages(channel, search=key_search):
            if message.date < datetime(y_max, m_max, d_max, tzinfo=timezone.utc) and message.date > datetime(y_min, m_min, d_min, tzinfo=timezone.utc):
                print(message.id, message.date, message.message[:20], message.post_author)
                messages_id.append(message.id)
                messages_date.append(message.date)
                messages.append(message.message)

                message_link = f"{channel}/{message.id}"
                message_links.append(message_link)

                if send_message:
                    client.loop.run_until_complete(message.forward_to('me'))

                index += 1

    df = pd.DataFrame({
        "DATE": messages_date,
        "MESSAGE_ID": messages_id,
        "MESSAGE": messages,
        "LINK": message_link
    })

    print("=" * 80)
    print(f'Your query with a search key: "{key_search}" in "{chat_url}" has finished.')
    print(f"Found total {index} matches.")
    print("=" * 80)

    
    return df

def find_key_chat(chat_url: str, key_search: str, send_message: bool = True):
    index = 0
    messages_id = []
    messages_date = []
    messages = []
    messages_sender_id = []
    message_links = []

    with TelegramClient(username, api_id, api_hash) as client:

        # current_time = datetime.now()
        # client.loop.run_until_complete(client.send_message('me', f'Hello, myself! {current_time:%H:%M:%S}'))

        for message in client.iter_messages(chat_url, search=key_search):
            if message.date < datetime(y_max, m_max, d_max, tzinfo=timezone.utc) and message.date > datetime(y_min, m_min, d_min, tzinfo=timezone.utc):
                
                message_link = f"{chat_url}/{message.id}"

                messages_id.append(message.id)
                messages_date.append(message.date)
                messages.append(message.message)
                messages_sender_id.append(message.from_id)
                message_links.append(message_link)

                index += 1

                if send_message:
                    client.loop.run_until_complete(message.forward_to('me'))
    
    df = pd.DataFrame({
        "DATE": messages_date,
        "MESSAGE_ID": messages_id,
        "MESSAGE": messages,
        "SENDER_ID": messages_sender_id,
        "LINK": message_link
    })

    print("=" * 80)
    print(f'Your query with a search key: "{key_search}" in "{chat_url}" has finished.')
    print(f"Found total {index} matches.")
    print("=" * 80)

    return df


def save_to_excel(df: pd.DataFrame, filename: str):

    df['DATE'] = df['DATE'].dt.tz_convert(None)
    df.to_excel(filename, index=False)

    # workbook = load_workbook(filename)

    # sheet = workbook.active

    # for i, url in enumerate(df['LINK'], start=2):
    #     cell = sheet.cell(row=i, column=df.columns.get_loc('LINK') + 1)
    #     cell.value = "URL"
    #     cell.hyperlink = url

    # workbook.save(filename)
    # workbook.close()

if __name__ == '__main__':

    choose_function = {
        "group": find_key_chat,
        "channel": find_key_in_channel
    }

    find_messages = choose_function[search]
    df = find_messages(chat_url, key_search, forward_message)

    if output_filename is not None:
        save_to_excel(df, output_filename)


