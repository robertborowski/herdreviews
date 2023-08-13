# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_name_function(element_all_posts_arr, i_post):
  # ------------------------ get name start ------------------------
  element_i_post_credits_arr = element_all_posts_arr[i_post].find_elements(By.CSS_SELECTOR,'[slot="credit-bar"]') # type: list
  element_i_post_spans_arr = element_i_post_credits_arr[0].find_elements(By.TAG_NAME,'span') # type: list
  for i2 in range(len(element_i_post_spans_arr)):
    # ------------------------ pull i_post subreddit name start ------------------------
    try:
      if 'r/' in element_i_post_spans_arr[i2].text:
        str_multi_line = element_i_post_spans_arr[i2].text
        str_lines_arr = str_multi_line.splitlines()
        subreddit_name = str_lines_arr[0]
        return subreddit_name
    except:
      pass
    # ------------------------ pull i_post subreddit name end ------------------------
  # ------------------------ get name end ------------------------
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_title_function(driver, i_post):
  try:
    element_i_post_title_arr = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'post-title-')]")
    subreddit_title = element_i_post_title_arr[i_post].text
    return subreddit_title
  except:
    return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def reddit_scrape_function():
  # ------------------------ webdriver open start ------------------------
  # ------------------------ incognito start ------------------------
  options = webdriver.ChromeOptions()
  options.add_argument("--incognito")
  # ------------------------ incognito end ------------------------
  driver = webdriver.Chrome(options=options)
  driver.get('https://www.reddit.com/user/smile-thank-you')
  driver.maximize_window()
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
      # ------------------------ init variables for each post start ------------------------
      # ------------------------ init variables for each post end ------------------------
      # ------------------------ check in/add to dict start ------------------------
      if element_all_posts_arr[i_post] in data_captured_dict:
        continue
      if i_post not in data_captured_dict:
        data_captured_dict[element_all_posts_arr[i_post]] = {}
      # ------------------------ check in/add to dict end ------------------------
      # ------------------------ pull/assign variables start ------------------------
      data_captured_dict[element_all_posts_arr[i_post]]['subreddit_name'] = get_name_function(element_all_posts_arr, i_post)
      data_captured_dict[element_all_posts_arr[i_post]]['subreddit_title'] = get_title_function(driver, i_post)
      # ------------------------ pull/assign variables end ------------------------
      print(f'0) i_post index: {i_post}')
      print(f"1) subreddit_name: {data_captured_dict[element_all_posts_arr[i_post]]['subreddit_name']}")
      print(f"2) subreddit_title: {data_captured_dict[element_all_posts_arr[i_post]]['subreddit_title']}")
      print(' ')
    # ------------------------ TESTING ONLY fail safe start ------------------------
    if len(element_all_posts_arr) >= 40:
      break
    # ------------------------ TESTING ONLY fail safe end ------------------------
  print(' ------------- 0 ------------- ')
  # ------------------------ recurring end ------------------------
  localhost_print_function(' ------------- 100-data_captured_dict start ------------- ')
  data_captured_dict = dict(sorted(data_captured_dict.items(),key=lambda x:x[0]))
  for k,v in data_captured_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-data_captured_dict end ------------- ')
  # ------------------------ webdriver close start ------------------------
  driver.close()
  # ------------------------ webdriver close end ------------------------
  return True
# ------------------------ individual function end ------------------------