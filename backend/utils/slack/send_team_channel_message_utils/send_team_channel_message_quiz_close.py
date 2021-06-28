# -------------------------------------------------------------- Imports
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def send_team_channel_message_quiz_close_function(slack_bot_token, user_channel, user_slack_authed_id):
  localhost_print_function('=========================================== send_team_channel_message_quiz_close_function START ===========================================')
  
  if user_slack_authed_id == 'No Winner':
    output_text = f":wave: Hi <!here>, your team's weekly Triviafy quiz is now CLOSED!\n:ghost: This week there was {user_slack_authed_id}!\n:gift: For every 10th win that a person achieves, we send them a free gift card prize!\n:100: Login and checkout your team's leaderboard at: https://triviafy.com/leaderboard"
  else:
    output_text = f":wave: Hi <!here>, your team's weekly Triviafy quiz is now CLOSED!\n:tada: Congrats to this week's Triviafy 'Bragging-Rights-Card' winner: <@{user_slack_authed_id}>!\n:gift: For every 10th win that a person achieves, we send them a free gift card prize!\n:100: Login and checkout your team's leaderboard at: https://triviafy.com/leaderboard"


  # Set up client with the USER's Bot Access Token. NOT your's from the environment variable
  client = WebClient(token=slack_bot_token)
  # Have the bot send a test message to the channel
  try:
    response = client.chat_postMessage(
      channel=user_channel,
      text=output_text
    )
    localhost_print_function('sent slack message')
  except SlackApiError as e:
    localhost_print_function('did not send message to slack channel')
    print(e.response['error'])

  localhost_print_function('=========================================== send_team_channel_message_quiz_close_function END ===========================================')
  return True, output_text