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
from website.backend.dates import unix_timestamp_to_est_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def reddit_all_posts_dict_function(submissions):
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
  return all_posts_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def reddit_all_posts_to_db_function(all_posts_dict):
  for k,v in all_posts_dict.items():
    # k = community
    # v = 'url of post' : 'info about post'
    for k2,v2 in v.items():
      # k2 = 'url of post'
      # v2 = 'col key' : 'col val'
      # ------------------------ check if in db start ------------------------
      db_post_obj = RedditPostsObj.query.filter_by(post_url=k2).first()
      if db_post_obj == None or db_post_obj == []:
        fk_reddit_post_id = create_uuid_function('reddit_post_')
        # ------------------------ insert to db start ------------------------
        new_row = RedditPostsObj(
          id=fk_reddit_post_id,
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
        all_posts_dict[k][k2]['fk_reddit_post_id'] = fk_reddit_post_id
      # ------------------------ check if in db end ------------------------
      # ------------------------ check existing reddit post obj start ------------------------
      else:
        all_posts_dict[k][k2]['fk_reddit_post_id'] = db_post_obj.id
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
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def reddit_all_post_commentary_function(reddit_connection, all_posts_dict):
  for k,v in all_posts_dict.items():
    # k = community
    # v = 'url of post' : 'info about post'
    for k2,v2 in v.items():
      all_posts_dict[k][k2]['comments_dict'] = {}
      # k2 = 'url of post'
      # v2 = 'col key' : 'col val'
      submission = reddit_connection.submission(url=k2)
      comments = submission.comments
      for i_comment in comments:
        # ------------------------ assign variables start ------------------------
        i_comment_url = 'https://www.reddit.com'
        try:
          i_comment_url = 'https://www.reddit.com' + i_comment.permalink
        except:
          continue
        comment_created_at = unix_timestamp_to_est_function(i_comment.created)
        # ------------------------ assign variables end ------------------------
        # ------------------------ author exception start ------------------------
        author_fix = '[deleted]'
        try:
          author_fix = i_comment.author.name
        except:
          pass
        # ------------------------ author exception end ------------------------
        # ------------------------ comment length exception start ------------------------
        comment_fix = i_comment.body
        if len(comment_fix) > 1000:
          comment_fix = comment_fix[:1000]
        # ------------------------ comment length exception end ------------------------
        # ------------------------ insert/update db start ------------------------
        db_comment_obj = RedditCommentsObj.query.filter_by(comment_url=i_comment_url).first()
        if db_comment_obj == None or db_comment_obj == []:
          # ------------------------ insert to db start ------------------------
          new_row = RedditCommentsObj(
            id=create_uuid_function('reddit_comment_'),
            created_timestamp=create_timestamp_function(),
            fk_reddit_post_id=v2['fk_reddit_post_id'],
            author=author_fix,
            comment=comment_fix,
            upvotes=i_comment.ups,
            downvotes=i_comment.downs,
            created_at=comment_created_at,
            comment_url=i_comment_url
          )
          db.session.add(new_row)
          db.session.commit()
          # ------------------------ insert to db end ------------------------
        else:
          # ------------------------ update db start ------------------------
          change_found = False
          if db_comment_obj.author != author_fix:
            db_comment_obj.author = author_fix
            change_found = True
          if db_comment_obj.comment != comment_fix:
            db_comment_obj.comment = comment_fix
            change_found = True
          if int(db_comment_obj.upvotes) != int(i_comment.ups):
            db_comment_obj.upvotes = int(i_comment.ups)
            change_found = True
          if int(db_comment_obj.downvotes) != int(i_comment.downs):
            db_comment_obj.downvotes = int(i_comment.downs)
            change_found = True
          if db_comment_obj.created_at != comment_created_at:
            db_comment_obj.created_at = comment_created_at
            change_found = True
          if change_found == True:
            db.session.commit()
          # ------------------------ update db end ------------------------
        # ------------------------ insert/update db end ------------------------
  return True
# ------------------------ individual function end ------------------------

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
  all_posts_dict = reddit_all_posts_dict_function(submissions)
  # ------------------------ create all posts dict end ------------------------
  # ------------------------ loop through posts and insert to db start ------------------------
  reddit_all_posts_to_db_function(all_posts_dict)
  # ------------------------ loop through posts and insert to db end ------------------------
  # ------------------------ get commentary for each post start ------------------------
  reddit_all_post_commentary_function(reddit_connection, all_posts_dict)
  # ------------------------ get commentary for each post end ------------------------
  # localhost_print_function(' ------------- 50 ------------- ')
  # localhost_print_function(pprint.pformat(all_posts_dict, indent=2))
  # localhost_print_function(' ------------- 50 ------------- ')
  return True
# ------------------------ individual function end ------------------------