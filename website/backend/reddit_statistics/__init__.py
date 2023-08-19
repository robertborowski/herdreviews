# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import pprint
from website.models import RedditMappingObj, RedditPostsObj, RedditCommentsObj
from website import db
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_reddit_statistics_function(page_dict, passed_current_user_obj):
  # ------------------------ set variables start ------------------------
  page_dict['poll_reddit_dict'] = {}
  # ------------------------ set variables end ------------------------
  # ------------------------ get all mapped reddit posts start ------------------------
  obj_reddit_mapped = RedditMappingObj.query.filter_by(fk_poll_id=page_dict['url_poll_id']).all()
  # ------------------------ get all mapped reddit posts end ------------------------
  # ------------------------ if no reddit post start ------------------------
  if obj_reddit_mapped == None or obj_reddit_mapped == []:
    page_dict['poll_reddit_dict'] = None
    return page_dict
  # ------------------------ if no reddit post end ------------------------
  # ------------------------ loop through posts start ------------------------
  for i_map_obj in obj_reddit_mapped:
    page_dict['poll_reddit_dict'][i_map_obj.fk_reddit_post_id] = {}
    obj_reddit_post = RedditPostsObj.query.filter_by(id=i_map_obj.fk_reddit_post_id).first()
    # ------------------------ reddit post information start ------------------------
    page_dict['poll_reddit_dict'][i_map_obj.fk_reddit_post_id]['community'] = obj_reddit_post.community
    page_dict['poll_reddit_dict'][i_map_obj.fk_reddit_post_id]['title'] = obj_reddit_post.title
    page_dict['poll_reddit_dict'][i_map_obj.fk_reddit_post_id]['total_votes'] = obj_reddit_post.total_votes
    page_dict['poll_reddit_dict'][i_map_obj.fk_reddit_post_id]['total_comments'] = int(obj_reddit_post.total_comments)
    page_dict['poll_reddit_dict'][i_map_obj.fk_reddit_post_id]['post_url'] = obj_reddit_post.post_url
    # ------------------------ reddit post information end ------------------------
    # ------------------------ reddit post comments information start ------------------------
    page_dict['poll_reddit_dict'][i_map_obj.fk_reddit_post_id]['all_comments_dict'] = {}
    if page_dict['poll_reddit_dict'][i_map_obj.fk_reddit_post_id]['total_comments'] == 0:
      page_dict['poll_reddit_dict'][i_map_obj.fk_reddit_post_id]['all_comments_dict'] = None
    else:
      obj_reddit_comments = RedditCommentsObj.query.filter_by(fk_reddit_post_id=obj_reddit_post.id).order_by(RedditCommentsObj.upvotes.desc()).all()
      for i_comment_obj in obj_reddit_comments:
        page_dict['poll_reddit_dict'][i_map_obj.fk_reddit_post_id]['all_comments_dict'][i_comment_obj.id] = {}
        page_dict['poll_reddit_dict'][i_map_obj.fk_reddit_post_id]['all_comments_dict'][i_comment_obj.id]['author'] = i_comment_obj.author
        page_dict['poll_reddit_dict'][i_map_obj.fk_reddit_post_id]['all_comments_dict'][i_comment_obj.id]['comment'] = i_comment_obj.comment
        page_dict['poll_reddit_dict'][i_map_obj.fk_reddit_post_id]['all_comments_dict'][i_comment_obj.id]['upvotes'] = i_comment_obj.upvotes
    # ------------------------ reddit post comments information end ------------------------
  # ------------------------ loop through posts end ------------------------
  localhost_print_function(' ------------- 50 ------------- ')
  localhost_print_function(pprint.pformat(page_dict, indent=2))
  localhost_print_function(' ------------- 50 ------------- ')
  return page_dict
# ------------------------ individual function end ------------------------