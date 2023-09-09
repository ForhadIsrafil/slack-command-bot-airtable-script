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
    print(command)
    user_name = command['user_name']
    user_id = command['user_id']
    channel_id = command['channel_id']

    # Filtering Datetime in Unix Timestamp start
    today_date_time = datetime.datetime.now()
    print("first day Date:", today_date_time.day - today_date_time.day + 1)
    # latest_date_time
    latest_date_time = time.mktime(today_date_time.timetuple())
    print("latest UNIX timestamp:", latest_date_time)
    # oldest_date_time
    oldest_date_time = datetime.datetime(year=today_date_time.year, month=today_date_time.month,
                                         day=today_date_time.day - today_date_time.day + 1, hour=1, minute=1, second=1)
    print("oldest UNIX timestamp:", time.mktime(oldest_date_time.timetuple()))
    # Filtering Datetime in Unix Timestamp end

    messages = app.client.conversations_history(channel=channel_id, oldest=oldest_date_time, limit=1000)
    print(messages)
    say("hey")


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
