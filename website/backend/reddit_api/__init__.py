# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import praw
import os
import pprint
from website.models import RedditPostsObj, RedditCommentsObj
from website import db
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
import json
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
  submissions = user.submissions.new(limit=200)
  # ------------------------ get all posts from user end ------------------------
  # ------------------------ create all posts dict start ------------------------
  all_posts_dict = {}
  for i_post in submissions:
    # ------------------------ get post info, set/assign variables start ------------------------
    if i_post.subreddit.display_name not in all_posts_dict:
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
    # ------------------------ check if post removed start ------------------------
    all_posts_dict[i_post.subreddit.display_name][i_post.url]['post_removed'] = False
    if i_post.removed_by_category != None:
      all_posts_dict[i_post.subreddit.display_name][i_post.url]['post_removed'] = True
    # ------------------------ check if post removed end ------------------------
    # ------------------------ get post info, set/assign variables end ------------------------
  # ------------------------ create all posts dict end ------------------------
  # ------------------------ loop through posts and insert to db start ------------------------
  for k,v in all_posts_dict.items():
    # k = community
    # v = 'url of post' : 'info about post'
    for k2,v2 in v.items():
      # k2 = 'url of post'
      # v2 = 'col key' : 'col val'
      # ------------------------ check if in db start ------------------------
      db_post_obj = RedditPostsObj.query.filter_by(post_url=k2).first()
      if db_post_obj == None or db_post_obj == []:
        # ------------------------ insert to db start ------------------------
        new_row = RedditPostsObj(
          id=create_uuid_function('reddit_post_'),
          created_timestamp=create_timestamp_function(),
          community=k,
          title=v2['title'],
          total_votes=v2['total_vote_count'],
          total_comments=v2['num_comments'],
          post_url=k2,
          total_upvotes=v2['ups'],
          upvote_ratio=v2['upvote_ratio'],
          total_views=v2['view_count'],
          poll_data_obj=json.dumps(v2['poll_data_dict']),
          post_removed=v2['post_removed']
        )
        db.session.add(new_row)
        db.session.commit()
        # ------------------------ insert to db end ------------------------
      # ------------------------ check if in db end ------------------------
      # ------------------------ check existing reddit post obj start ------------------------
      else:
        # ------------------------ compare post data changes start ------------------------
        change_found = False
        if db_post_obj.community != k:
          db_post_obj.community = k
          change_found = True
        if db_post_obj.title != v2['title']:
          db_post_obj.title = v2['title']
          change_found = True
        if int(db_post_obj.total_votes) != int(v2['total_vote_count']):
          db_post_obj.total_votes = int(v2['total_vote_count'])
          change_found = True
        if int(db_post_obj.total_comments) != int(v2['num_comments']):
          db_post_obj.total_comments = int(v2['num_comments'])
          change_found = True
        if int(db_post_obj.total_upvotes) != int(v2['ups']):
          db_post_obj.total_upvotes = int(v2['ups'])
          change_found = True
        if float(db_post_obj.upvote_ratio) != float(v2['upvote_ratio']):
          db_post_obj.upvote_ratio = float(v2['upvote_ratio'])
          change_found = True
        if db_post_obj.total_views != v2['view_count']:
          db_post_obj.total_views = v2['view_count']
          change_found = True
        if db_post_obj.post_removed != v2['post_removed']:
          db_post_obj.post_removed = v2['post_removed']
          change_found = True
        # ------------------------ compare vote counts start ------------------------
        current_poll_data_dict = None
        try:
          current_poll_data_dict = json.loads(v['poll_data_dict'])
        except:
          pass
        if v2['poll_data_dict'] != None:
          for k3,v3 in v2['poll_data_dict'].items():
            # k3 = poll choice title
            # v3 = poll choice vote count
            try:
              if current_poll_data_dict[k3] != v3:
                db_post_obj.poll_data_obj = json.dumps(v2['poll_data_dict'])
                change_found = True
                break
            except:
              db_post_obj.poll_data_obj = json.dumps(v2['poll_data_dict'])
              change_found = True
              break
        # ------------------------ compare vote counts end ------------------------
        if change_found == True:
          db.session.commit()
        # ------------------------ compare post data changes end ------------------------
      # ------------------------ check existing reddit post obj end ------------------------
  # ------------------------ loop through posts and insert to db end ------------------------
  # localhost_print_function(' ------------- 50 ------------- ')
  # localhost_print_function(pprint.pformat(all_posts_dict, indent=2))
  # localhost_print_function(' ------------- 50 ------------- ')
  return True
# ------------------------ individual function end ------------------------