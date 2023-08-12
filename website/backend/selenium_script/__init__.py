# ------------------------ imports start ------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
# ------------------------ imports end ------------------------


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
  
  
  
  # ------------------------ scroll to bottom of the page start ------------------------
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  # ------------------------ scroll to bottom of the page end ------------------------
  # ------------------------ find all posts start ------------------------
  # ------------------------ get lists/variables start ------------------------
  element_indvidual_posts_arr = driver.find_elements(By.CSS_SELECTOR,'[view-type="cardView"]') # type: list
  # ------------------------ get lists/variables end ------------------------
  print(' ------------- 0 ------------- ')
  for i in range(len(element_indvidual_posts_arr)): # type: <class 'selenium.webdriver.remote.webelement.WebElement'>
    # ------------------------ set variables for each post start ------------------------
    subreddit_name = ''
    # ------------------------ set variables for each post end ------------------------
    # ------------------------ get name start ------------------------
    element_i_post_credits_arr = element_indvidual_posts_arr[i].find_elements(By.CSS_SELECTOR,'[slot="credit-bar"]') # type: list
    element_spans_arr = element_i_post_credits_arr[0].find_elements(By.TAG_NAME,'span') # type: list
    print(' ------------- 1 ------------- ')
    for i2 in range(len(element_spans_arr)):
      # ------------------------ pull subreddit name start ------------------------
      try:
        if 'r/' in element_spans_arr[i2].text:
          str_multi_line = element_spans_arr[i2].text
          str_lines_arr = str_multi_line.splitlines()
          subreddit_name = str_lines_arr[0]
          print(f"subreddit_name | type: {type(subreddit_name)} | {subreddit_name}")
          print('found')
          break
      except:
        pass
      # ------------------------ pull subreddit name end ------------------------
    print(' ------------- 1 ------------- ')
    # ------------------------ get name end ------------------------
    # ------------------------ TESTING ONLY fail safe start ------------------------
    if i >= 3:
      break
    # ------------------------ TESTING ONLY fail safe end ------------------------
  print(' ------------- 0 ------------- ')
  # ------------------------ find all posts end ------------------------
  
  
  
  # ------------------------ webdriver close start ------------------------
  driver.close()
  # ------------------------ webdriver close end ------------------------
  return True
# ------------------------ individual function end ------------------------