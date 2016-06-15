import os
import time
import math
import constants
from slackclient import SlackClient
from random import randint
import random
from datetime import datetime, timedelta

BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@{bot_id}>:".format(bot_id=str(BOT_ID))
EXAMPLE_COMMAND = "go"

current_lord = None # Who is the current lord?
last_selection_time = None

# instantiate Slack & Twilio clients
slack_client = SlackClient(constants.SLACK_BOT_TOKEN)

APPLICANTS = [
    'Celina',
    'Ann',
    'Mike',
    'Seb',
    'Tom',
    'Eddie',
    'Elaine',
    'Julie',
    'Chris',
    'David',
    'Gleb',
    'Shane',
    'Greg',
    'Eric',
    'Clarissa',
    'Christine',
    'Heejin',
    'Makenna',
    'Clarissa'
]

def get_new_lord():
    # START------
    # Jules: This is how you locally modify a global value. This is typically not done and is generally frowned upon.
    # The better option would be to pass whatever you need into the method and store it somewhere around the while loop below
    # For now, no biggie though
    global current_lord
    global last_selection_time
    # END -------

    msg = "Lord has not changed"
    if current_lord is None:
        # Just return random
        last_selection_time = datetime.now()
        current_lord = random.choice(APPLICANTS)
        msg = "New lord has been chosen"
    else:
        # Check if enough time has passed
        current_time = datetime.now()
        if last_selection_time is not None:
            if current_time > (last_selection_time + timedelta(hours=24)):
                current_lord = random.choice(APPLICANTS)
                msg = "New lord has been chosen"
        else:
            msg = "Not enough time has passed; keeping same lord"

    return current_lord, msg

def handle_command(command, channel):
    """ Receives commands directed at the bot and determines if they are valid commands. If so, then acts on commands. If not, returns back what it needs for clarification. """

    # response = "Type *" + EXAMPLE_COMMAND + "* or I won't understand you. You also have to wait %d until you can select a new sonos lord.".format(time_assignment())
    if command.startswith(EXAMPLE_COMMAND):
        name, msg = get_new_lord()
        response = "The Lord of the Sonos is: {name} ({msg}) !".format(name=name, msg=msg)
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """ The Slack Real Time Messaging API is an events firehose. This parsing function returns None unless a message is directed at the Bot, based on its ID. """

    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                #return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("SonosBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            print command, channel
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
