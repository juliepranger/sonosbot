import os
import time
import math
from slackclient import SlackClient
from random import randint


print math


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")
print(BOT_ID)

# constants
os.environ['SLACK_BOT_TOKEN'] = 'xoxb-49975763140-CLCZr0SF5bQU8kL6maPM5KpG'
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "sonos"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
print(os.environ.get('SLACK_BOT_TOKEN'))

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

sonos_lord = APPLICANTS[randint(0,len(APPLICANTS))]
print sonos_lord

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they are valid commands. If so, then acts on commands. If not, returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "The Lord of the Sonos is: {} !".format(sonos_lord)
        sonos_lord = APPLICANTS[randint(0,len(APPLICANTS))]
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose. This parsing function returns None unless a message is directed at the Bot, based on its ID.
    """
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
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
