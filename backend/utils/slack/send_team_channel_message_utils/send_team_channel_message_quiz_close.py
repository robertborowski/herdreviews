# -------------------------------------------------------------- Imports
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


# -------------------------------------------------------------- Main Function
def send_team_channel_message_quiz_close_function(slack_bot_token, user_channel, user_slack_authed_id):
  print('=========================================== send_team_channel_message_quiz_close_function START ===========================================')
  
  output_text = f":wave: Hi <!here>, your team's weekly Triviafy quiz is now CLOSED!\n:tada: Congrats to this week's Triviafy 'Bragging-Rights-Card' winner: <@{user_slack_authed_id}>!\n:gift: For every 10th win that a person achieves, we send them a free gift-card prize!\n:100: Login and checkout your team's leaderboard at: https://triviafy.com/leaderboard"

  # Set up client with the USER's Bot Access Token. NOT your's from the environment variable
  client = WebClient(token=slack_bot_token)
  # Have the bot send a test message to the channel
  try:
    response = client.chat_postMessage(
      channel=user_channel,
      text=output_text
    )
    print('sent slack message')
  except SlackApiError as e:
    print('did not send message to slack channel')
    print(e.response['error'])

  print('=========================================== send_team_channel_message_quiz_close_function END ===========================================')
  return True, output_text