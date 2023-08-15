# ------------------------ imports start ------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
import time
from website.models import RedditPostsObj, RedditCommentsObj
from website import db
from website.backend.dict_manipulation import arr_of_dict_all_columns_single_item_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_general_info_function(element_all_posts_arr, i_post):
  # ------------------------ init variables start ------------------------
  reddit_community = ''
  reddit_posted_time_ago = ''
  reddit_title = ''
  reddit_total_votes = int(0)
  reddit_total_comments = int(0)
  # ------------------------ init variables end ------------------------
  # ------------------------ get community and time ago start ------------------------
  element_i_post_credits_arr = element_all_posts_arr[i_post].find_elements(By.CSS_SELECTOR,'[slot="credit-bar"]') # type: list
  element_i_post_spans_arr = element_i_post_credits_arr[0].find_elements(By.TAG_NAME,'span') # type: list
  for i2 in range(len(element_i_post_spans_arr)):
    try:
      if 'r/' in element_i_post_spans_arr[i2].text and reddit_community == '':
        str_multi_line = element_i_post_spans_arr[i2].text
        str_lines_arr = str_multi_line.splitlines()
        reddit_community = str_lines_arr[0]
        reddit_posted_time_ago = str_lines_arr[2]
    except:
      pass
  # ------------------------ get community and time ago end ------------------------
  # ------------------------ get title start ------------------------
  try:
    element_i_post_title_arr = element_all_posts_arr[i_post].find_elements(By.CSS_SELECTOR, "[id^='post-title-']")
    reddit_title = element_i_post_title_arr[0].text
  except:
    pass
  # ------------------------ get title end ------------------------
  # ------------------------ get count if available - votes start ------------------------
  try:
    element_i_post_media_container_arr = element_all_posts_arr[i_post].find_elements(By.CSS_SELECTOR,'[slot="post-media-container"]') # type: list
    element_i_post_faceplate_number_arr = element_i_post_media_container_arr[0].find_elements(By.TAG_NAME,'faceplate-number') # type: list
    reddit_total_votes = int(element_i_post_faceplate_number_arr[0].text)
  except:
    pass
  # ------------------------ get count if available - votes end ------------------------
  # ------------------------ get count if available - comments start ------------------------
  shadow_root = element_all_posts_arr[i_post].shadow_root
  element_button = shadow_root.find_elements(By.CSS_SELECTOR,'button[name="comments-action-button"]')
  element_i_post_faceplate_number_arr = element_button[0].find_elements(By.TAG_NAME,'faceplate-number')
  reddit_total_comments = int(element_i_post_faceplate_number_arr[0].text)
  # ------------------------ get count if available - comments end ------------------------
  return reddit_community, reddit_posted_time_ago, reddit_title, reddit_total_votes, reddit_total_comments
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def pull_create_update_reddit_post_function(data_captured_dict, element_all_posts_arr, i_post):
  db_obj = RedditPostsObj.query.filter_by(community=data_captured_dict[element_all_posts_arr[i_post]]['reddit_community'],title=data_captured_dict[element_all_posts_arr[i_post]]['reddit_title']).order_by(RedditPostsObj.created_timestamp.desc()).first()
  if db_obj == None or db_obj == []:
    # ------------------------ insert to db start ------------------------
    new_row = RedditPostsObj(
      id=create_uuid_function('reddit_post_'),
      created_timestamp=create_timestamp_function(),
      community=data_captured_dict[element_all_posts_arr[i_post]]['reddit_community'],
      title=data_captured_dict[element_all_posts_arr[i_post]]['reddit_title'],
      total_votes=data_captured_dict[element_all_posts_arr[i_post]]['reddit_total_votes'],
      total_comments=data_captured_dict[element_all_posts_arr[i_post]]['reddit_total_comments']
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ insert to db end ------------------------
    db_obj = RedditPostsObj.query.filter_by(community=data_captured_dict[element_all_posts_arr[i_post]]['reddit_community'],title=data_captured_dict[element_all_posts_arr[i_post]]['reddit_title']).order_by(RedditPostsObj.created_timestamp.desc()).first()
  else:
    # ------------------------ update existing if change in total votes start ------------------------
    if int(db_obj.total_votes) != int(data_captured_dict[element_all_posts_arr[i_post]]['reddit_total_votes']):
      db_obj.total_votes = int(data_captured_dict[element_all_posts_arr[i_post]]['reddit_total_votes'])
      db.session.commit()
    # ------------------------ update existing if change in total votes end ------------------------
    # ------------------------ update existing if change in total comments start ------------------------
    if int(db_obj.total_comments) != int(data_captured_dict[element_all_posts_arr[i_post]]['reddit_total_comments']):
      db_obj.total_comments = int(data_captured_dict[element_all_posts_arr[i_post]]['reddit_total_comments'])
      db.session.commit()
    # ------------------------ update existing if change in total comments end ------------------------
  return db_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_all_comments_from_post_function(data_captured_dict, element_all_posts_arr, i_post, driver):
  view_more_comments_button = True
  while view_more_comments_button == True:
    # ------------------------ scroll to bottom of the page start ------------------------
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    # ------------------------ scroll to bottom of the page end ------------------------
    # ------------------------ check if view more comments button exists start ------------------------
    all_spans_arr = driver.find_elements(By.TAG_NAME,'span')
    found_count = 0
    for i in range(len(all_spans_arr) -1, -1, -1):
      try:
        if all_spans_arr[i].text == 'View more comments':
          found_count += 1
          all_spans_arr[i].click()
      except:
        pass
    if found_count == 0:
      view_more_comments_button = False
    # ------------------------ check if view more comments button exists end ------------------------
  # ------------------------ commentary per post start ------------------------
  data_captured_dict[element_all_posts_arr[i_post]]['reddit_post_comments'] = {}
  # ------------------------ commentary per post end ------------------------
  element_comment_tree_arr = driver.find_elements(By.CSS_SELECTOR,'[id="comment-tree"]')
  try:
    element_all_comments_arr = element_comment_tree_arr[0].find_elements(By.TAG_NAME,'shreddit-comment')
    for i in range(len(element_all_comments_arr)):
      author = element_all_comments_arr[i].get_attribute("author")
      comment_element = element_all_comments_arr[i].find_elements(By.TAG_NAME,'p')
      comment = comment_element[0].text
      if author not in data_captured_dict[element_all_posts_arr[i_post]]['reddit_post_comments']:
        data_captured_dict[element_all_posts_arr[i_post]]['reddit_post_comments'][author] = []
      if comment not in data_captured_dict[element_all_posts_arr[i_post]]['reddit_post_comments'][author]:
        data_captured_dict[element_all_posts_arr[i_post]]['reddit_post_comments'][author].append(comment)
  except:
    pass
  return data_captured_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def add_commentary_to_db_function(data_captured_dict, element_all_posts_arr, i_post, db_reddit_post_obj):
  for k,v in data_captured_dict[element_all_posts_arr[i_post]]['reddit_post_comments'].items():
    i_author = k
    i_comments_arr = v
    for i_comment in i_comments_arr:
      db_obj = RedditCommentsObj.query.filter_by(fk_reddit_post_id=db_reddit_post_obj.id,community=data_captured_dict[element_all_posts_arr[i_post]]['reddit_community'],title=data_captured_dict[element_all_posts_arr[i_post]]['reddit_title'],author=i_author,comment=i_comment).order_by(RedditCommentsObj.created_timestamp.desc()).first()
      if db_obj == None or db_obj == []:
        # ------------------------ insert to db start ------------------------
        new_row = RedditCommentsObj(
          id=create_uuid_function('reddit_comment_'),
          created_timestamp=create_timestamp_function(),
          fk_reddit_post_id=db_reddit_post_obj.id,
          community=data_captured_dict[element_all_posts_arr[i_post]]['reddit_community'],
          title=data_captured_dict[element_all_posts_arr[i_post]]['reddit_title'],
          author=i_author,
          comment=i_comment
        )
        db.session.add(new_row)
        db.session.commit()
        # ------------------------ insert to db end ------------------------
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def reddit_scrape_function():
  # ------------------------ webdriver open start ------------------------
  # ------------------------ incognito start ------------------------
  options = webdriver.ChromeOptions()
  options.add_argument("--incognito")
  options.add_argument("start-maximized")
  # ------------------------ incognito end ------------------------
  driver = webdriver.Chrome(options=options)
  driver.get('https://www.reddit.com/user/smile-thank-you/submitted/')
  # ------------------------ webdriver open end ------------------------
  # ------------------------ set variables start ------------------------
  data_captured_dict = {}
  running_check = True
  run_count = -1
  # ------------------------ set variables end ------------------------
  # ------------------------ recurring start ------------------------
  print(' ------------- 0 ------------- ')
  while running_check == True:
    run_count += 1
    # ------------------------ scroll to bottom of the page start ------------------------
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # ------------------------ scroll to bottom of the page end ------------------------
    # ------------------------ get lists/variables start ------------------------
    element_all_posts_arr = driver.find_elements(By.CSS_SELECTOR,'[view-type="cardView"]') # type: list
    # ------------------------ get lists/variables end ------------------------
    for i_post in range(len(element_all_posts_arr)): # type: <class 'selenium.webdriver.remote.webelement.WebElement'>
      # ------------------------ check in/add to dict start ------------------------
      if element_all_posts_arr[i_post] in data_captured_dict:
        continue
      if i_post not in data_captured_dict:
        data_captured_dict[element_all_posts_arr[i_post]] = {}
      # ------------------------ check in/add to dict end ------------------------
      # ------------------------ pull/assign variables start ------------------------
      data_captured_dict[element_all_posts_arr[i_post]]['reddit_community'], data_captured_dict[element_all_posts_arr[i_post]]['reddit_posted_time_ago'], data_captured_dict[element_all_posts_arr[i_post]]['reddit_title'], data_captured_dict[element_all_posts_arr[i_post]]['reddit_total_votes'], data_captured_dict[element_all_posts_arr[i_post]]['reddit_total_comments'] = get_general_info_function(element_all_posts_arr, i_post)
      # ------------------------ pull/assign variables end ------------------------
      # ------------------------ pull/create reddit post from db start ------------------------
      db_reddit_post_obj = pull_create_update_reddit_post_function(data_captured_dict, element_all_posts_arr, i_post)
      # ------------------------ pull/create reddit post from db end ------------------------
      # ------------------------ new commentary check start ------------------------
      new_commentary_db_check = False
      db_comments_obj = RedditCommentsObj.query.filter_by(fk_reddit_post_id=db_reddit_post_obj.id).all()
      if len(db_comments_obj) < int(db_reddit_post_obj.total_comments):
        new_commentary_db_check = True
      # ------------------------ new commentary check end ------------------------
      # ------------------------ get new comments start ------------------------
      if new_commentary_db_check == True:
        post_link = 'https://www.reddit.com' + element_all_posts_arr[i_post].get_attribute("permalink")
        driver.get(post_link)
        data_captured_dict = get_all_comments_from_post_function(data_captured_dict, element_all_posts_arr, i_post, driver)
        # ------------------------ collect all comments from post end ------------------------
        # ------------------------ add to db start ------------------------
        add_commentary_to_db_function(data_captured_dict, element_all_posts_arr, i_post, db_reddit_post_obj)
        # ------------------------ add to db end ------------------------
        driver.get('https://www.reddit.com/user/smile-thank-you/submitted/')
        time.sleep(3)
        break
      # ------------------------ get new comments end ------------------------
    # ------------------------ TESTING ONLY fail safe start ------------------------
    if len(element_all_posts_arr) >= 20:
      break
    # ------------------------ TESTING ONLY fail safe end ------------------------
  print(' ------------- 0 ------------- ')
  # ------------------------ recurring end ------------------------
  # ------------------------ webdriver close start ------------------------
  driver.close()
  # ------------------------ webdriver close end ------------------------
  # localhost_print_function(' ------------- 100-data_captured_dict start ------------- ')
  # for k,v in data_captured_dict.items():
  #   localhost_print_function(f"k: {k} | v: {v}")
  #   pass
  # localhost_print_function(' ------------- 100-data_captured_dict end ------------- ')
  return True
# ------------------------ individual function end ------------------------