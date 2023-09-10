from slack_bolt import App, Say, Ack
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv
import json
import datetime
import time

load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

app = App(token=SLACK_BOT_TOKEN)


@app.event("app_mention")
def mention_handler(body, say):
    print("heelelel")
    say('Hello World!')


@app.command("/get_emoji")
def partybot_report(ack, say, command):
    ack()  # acknowledge command request
    # print(command)
    user_name = command['user_name']
    user_id = command['user_id']
    channel_id = command['channel_id']

    # FILTERING DATETIME IN UNIX TIMESTAMP START
    today_date_time = datetime.datetime.now()
    # print("first day Date:", today_date_time.day - today_date_time.day + 1)
    # latest_date_time
    latest_date_unix_time = time.mktime(today_date_time.timetuple())
    print("latest UNIX timestamp:", latest_date_unix_time)

    # oldest_date_time
    oldest_date_time = datetime.datetime(year=today_date_time.year, month=today_date_time.month,
                                         day=1, hour=0, minute=0, second=1)
    oldest_date_unix_time = time.mktime(oldest_date_time.timetuple())
    print("oldest UNIX timestamp:", oldest_date_unix_time)
    # FILTERING DATETIME IN UNIX TIMESTAMP END

    messages = app.client.conversations_history(channel=channel_id, latest=latest_date_unix_time,
                                                oldest=oldest_date_unix_time, limit=700)
    # print(messages)
    # ------------------------------------------------------------------------------------------
    separated_reactions_count_dict = {}
    for react in messages['messages']:
        try:
            # print(react['reactions'])
            if react['reactions'][0]['name'] in separated_reactions_count_dict:
                separated_reactions_count_dict[react['reactions'][0]['name']] = separated_reactions_count_dict[
                                                                                    react['reactions'][0]['name']] + 1
            if react['reactions'][0]['name'] not in separated_reactions_count_dict:
                separated_reactions_count_dict[react['reactions'][0]['name']] = 1

        except Exception as e:
            # print(e)
            pass

    print(separated_reactions_count_dict)
    data_list = [f':{key}: {value}' for key, value in separated_reactions_count_dict.items()]
    # ------------------------------------------------------------------------------------------
    say(" ".join(data_list))


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
