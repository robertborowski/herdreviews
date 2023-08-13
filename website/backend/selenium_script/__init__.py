# ------------------------ imports start ------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
import time
from website.models import RedditPostsObj
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
  # ------------------------ get votes count if available start ------------------------
  try:
    element_i_post_media_container_arr = element_all_posts_arr[i_post].find_elements(By.CSS_SELECTOR,'[slot="post-media-container"]') # type: list
    element_i_post_faceplate_number_arr = element_i_post_media_container_arr[0].find_elements(By.TAG_NAME,'faceplate-number') # type: list
    reddit_total_votes = int(element_i_post_faceplate_number_arr[0].text)
  except:
    pass
  # ------------------------ get votes count if available end ------------------------
  # ------------------------ get comments count if available start ------------------------
  # print(' ------------- 1 ------------- ')
  # print(' ------------- 1 ------------- ')
  # ------------------------ get comments count if available end ------------------------
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
def reddit_scrape_function():
  # ------------------------ webdriver open start ------------------------
  # ------------------------ incognito start ------------------------
  options = webdriver.ChromeOptions()
  options.add_argument("--incognito")
  options.add_argument("start-maximized")
  # ------------------------ incognito end ------------------------
  driver = webdriver.Chrome(options=options)
  driver.get('https://www.reddit.com/user/smile-thank-you')
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
      # db_reddit_post_obj = pull_create_update_reddit_post_function(data_captured_dict, element_all_posts_arr, i_post)
      # ------------------------ pull/create reddit post from db end ------------------------
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