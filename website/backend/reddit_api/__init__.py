# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import praw
import os
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def reddit_api_function():
  # ------------------------ set variables start ------------------------
  reddit_username = os.environ.get('REDDIT_USERNAME')
  reddit_app_id = os.environ.get('REDDIT_APP_ID_WEB_APP')
  reddit_app_secret = os.environ.get('REDDIT_APP_SECRET_WEB_APP')
  # ------------------------ set variables end ------------------------
  # ------------------------ connect to reddit start ------------------------
  reddit_connection = praw.Reddit(
    client_id=reddit_app_id,
    client_secret=reddit_app_secret,
    user_agent=reddit_username,
    username=reddit_username,
  )
  # ------------------------ connect to reddit end ------------------------
  # ------------------------ get all posts from user start ------------------------
  # Retrieve the user's submissions (posts)
  user = reddit_connection.redditor(reddit_username)
  submissions = user.submissions.new(limit=3)  # Set 'limit' to None to get all submissions

  # Extract and print the URLs of the user's submissions
  for i in submissions:
    localhost_print_function(f"i | type: {type(i)} | {i}")
    localhost_print_function(dir(i))
    localhost_print_function(' ')
  # ------------------------ get all posts from user end ------------------------
  return True
# ------------------------ individual function end ------------------------