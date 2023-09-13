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
        # real_name = app.client.users_info(user=react['user'])['user']['real_name']
        try:
            # print(react['reactions'])
            if react['reactions'][0]['name'] in separated_reactions_count_dict:
                separated_reactions_count_dict[react['reactions'][0]['name']]['amount'] = \
                    separated_reactions_count_dict[react['reactions'][0]['name']]['amount'] + 1
            if react['reactions'][0]['name'] not in separated_reactions_count_dict:
                separated_reactions_count_dict[react['reactions'][0]['name']] = {'amount': 1, 'user': react['user']}

        except Exception as e:
            # print(e)
            pass

    print(separated_reactions_count_dict)
    leaderboard_score = dict(sorted(separated_reactions_count_dict.items(), key=lambda x: x[0][0], reverse=True))
    print(leaderboard_score)
    # data_list = [f':{key}: {value}\n' for key, value in leaderboard_score.items()]
    # print(data_list)
    # ------------------------------------------------------------------------------------------

    blocks = generate_blocks(leaderboard_score)

    # say(blocks=blocks, text=" ".join(data_list))
    # say(blocks=blocks, text="The Leaderboard")
    say(blocks=blocks, text="_")


def generate_blocks(data):
    medals = {1: ":first_place_medal:", 2: ":second_place_medal:", 3: ":third_place_medal:", 4: ":four:"}
    mrkstring = '''
    Rank      Name                             Score\n
    
    '''.strip()
    for i, (key, value) in enumerate(data.items()):
        user_info = app.client.users_info(user=value['user'])
        mrkstring += "\n"+str(i + 1) + " - " + medals[i + 1] + "    :" + key + ":  " + user_info['user'][
            'real_name'] + "    -    " + str(
            value['amount']) + "\n"

    blocks_obj = []
    # for key, value in data.items():
    #     user_info = app.client.users_info(user=value['user'])
    blocks_obj.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": mrkstring
        }
    })
    blocks_obj.append({"type": "divider"})

    new_blocks = [{"type": "header", "text": {"type": "plain_text", "text": ":trophy: The Leaderboard"}},
                  {"type": "divider"}] + blocks_obj
    return new_blocks


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

{
    "type": "header",
    "text": {
        "type": "plain_text",
        "text": ":trophy: The Leaderboard"
    }
}
