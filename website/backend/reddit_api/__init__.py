# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import praw
import os
import pprint
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
  user = reddit_connection.redditor(reddit_username)
  submissions = user.submissions.new(limit=3)
  all_posts_dict = {}
  for i_post in submissions:
    # ------------------------ get post info, set/assign variables start ------------------------
    all_posts_dict[i_post.subreddit.display_name] = {}
    all_posts_dict[i_post.subreddit.display_name][i_post.url] = {}
    all_posts_dict[i_post.subreddit.display_name][i_post.url]['title'] = i_post.title
    all_posts_dict[i_post.subreddit.display_name][i_post.url]['num_comments'] = i_post.num_comments
    all_posts_dict[i_post.subreddit.display_name][i_post.url]['ups'] = i_post.ups
    all_posts_dict[i_post.subreddit.display_name][i_post.url]['upvote_ratio'] = i_post.upvote_ratio
    all_posts_dict[i_post.subreddit.display_name][i_post.url]['view_count'] = i_post.view_count
    all_posts_dict[i_post.subreddit.display_name][i_post.url]['total_vote_count'] = 0
    all_posts_dict[i_post.subreddit.display_name][i_post.url]['poll_data_dict'] = {}
    # ------------------------ get post poll options text + vote counts start ------------------------
    try:
      all_posts_dict[i_post.subreddit.display_name][i_post.url]['total_vote_count'] = i_post.poll_data.total_vote_count
      for i in range(len(i_post.poll_data.options)):
        poll_option_text = i_post.poll_data.options[i].text
        poll_option_vote_count = 0
        try:
          poll_option_vote_count = i_post.poll_data.options[i].vote_count
        except:
          poll_option_vote_count = 'wip'
        all_posts_dict[i_post.subreddit.display_name][i_post.url]['poll_data_dict'][poll_option_text] = poll_option_vote_count
    except:
      all_posts_dict[i_post.subreddit.display_name][i_post.url]['poll_data_dict'] = None
    # ------------------------ get post poll options text + vote counts end ------------------------
    # ------------------------ get post info, set/assign variables end ------------------------
  # ------------------------ get all posts from user end ------------------------
  localhost_print_function(' ------------- 50 ------------- ')
  localhost_print_function(pprint.pformat(all_posts_dict, indent=2))
  localhost_print_function(' ------------- 50 ------------- ')
  return True
# ------------------------ individual function end ------------------------