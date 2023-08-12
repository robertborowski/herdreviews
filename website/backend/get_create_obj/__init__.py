# ------------------------ imports start ------------------------
from website.models import UserObj, ShowsFollowingObj, PlatformsObj, ShowsObj, PollsObj, PollsAnsweredObj
from website.backend.sql_statements.select import select_general_function
from datetime import datetime, date
import random
import re
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_all_shows_following_function(current_user):
  db_shows_following_obj = None
  try:
    db_shows_following_obj = ShowsFollowingObj.query.filter_by(fk_user_id=current_user.id).all()
    if db_shows_following_obj == None or db_shows_following_obj == []:
      return None
  except:
    pass
  return db_shows_following_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_all_platforms_function():
  db_objs = PlatformsObj.query.filter_by(status=True).order_by(PlatformsObj.name.asc()).all()
  if db_objs == None or db_objs == []:
    return None
  return db_objs
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_all_shows_for_platform_function(input_platform_id):
  db_objs = ShowsObj.query.filter_by(fk_platform_id=input_platform_id,status=True).order_by(ShowsObj.name.asc()).all()
  if db_objs == None or db_objs == []:
    return None
  return db_objs
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_show_based_on_name_function(input_platform_id, input_name):
  db_obj = ShowsObj.query.filter_by(fk_platform_id=input_platform_id,name=input_name,status=True).first()
  if db_obj == None or db_obj == []:
    return None
  return db_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_show_based_on_id_and_platform_id_function(input_show_id, input_platform_id):
  db_obj = ShowsObj.query.filter_by(id=input_show_id, fk_platform_id=input_platform_id, status=True).first()
  if db_obj == None or db_obj == []:
    return None
  return db_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_show_based_on_id_function(input_show_id):
  db_obj = ShowsObj.query.filter_by(id=input_show_id).first()
  if db_obj == None or db_obj == []:
    return None
  return db_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_show_percent_of_all_polls_answered_function(fk_user_id, fk_show_id):
  # ------------------------ variables start ------------------------
  user_percent_completed = int(0)
  show_polls_total = int(0)
  show_polls_answered_total = int(0)
  is_complete = False
  # ------------------------ variables end ------------------------
  # ------------------------ show polls total start ------------------------
  db_objs = PollsObj.query.filter_by(fk_show_id=fk_show_id,status_approved=True,status_removed=False).all()
  try:
    show_polls_total = len(db_objs)
  except:
    pass
  # ------------------------ show polls total end ------------------------
  # ------------------------ user answered show polls total start ------------------------
  db_arr_of_dicts = select_general_function('select_query_general_3', fk_show_id, fk_user_id)
  try:
    show_polls_answered_total = len(db_arr_of_dicts)
  except:
    pass
  # ------------------------ user answered show polls total end ------------------------
  # ------------------------ calculation start ------------------------
  try:
    user_percent_completed = float(int(show_polls_answered_total)/int(show_polls_total))
    user_percent_completed = str(int(float(user_percent_completed) * float(100)))
  except:
    pass
  # ------------------------ calculation end ------------------------
  # ------------------------ catch start ------------------------
  if int(user_percent_completed) == int(0):
    user_percent_completed = 1
  # ------------------------ catch end ------------------------
  # ------------------------ complete status start ------------------------
  if int(user_percent_completed) == int(100):
    is_complete = True
  # ------------------------ complete status end ------------------------
  return int(user_percent_completed), is_complete
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_total_polls_created_today_by_user_for_one_show_function(input_user_id, input_show_id):
  # ------------------------ set variables start ------------------------
  today_date = date.today()
  count_today = int(0)
  # ------------------------ set variables end ------------------------
  # ------------------------ pull data start ------------------------
  db_obj = PollsObj.query.filter_by(fk_user_id=input_user_id,fk_show_id=input_show_id).order_by(PollsObj.created_timestamp.desc()).all()
  if db_obj == None or db_obj == []:
    return int(0)
  # ------------------------ pull data end ------------------------
  # ------------------------ loop + count today start ------------------------
  for i_obj in db_obj:
    i_obj_date = i_obj.created_timestamp.date()
    if i_obj_date == today_date:
      count_today += 1
  # ------------------------ loop + count today end ------------------------
  return int(count_today)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_poll_based_on_id_function(input_id):
  db_obj = PollsObj.query.filter_by(id=input_id,status_removed=False).first()
  if db_obj == None or db_obj == []:
    return None
  return db_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_all_polls_based_on_show_id_function(fk_show_id):
  db_objs = PollsObj.query.filter_by(fk_show_id=fk_show_id,status_approved=True,status_removed=False).order_by(PollsObj.created_timestamp.desc()).all()
  if db_objs == None or db_objs == []:
    db_objs = None
  return db_objs
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def check_at_least_one_poll_answer_submitted_function(current_user, poll_id):
  db_obj = PollsAnsweredObj.query.filter_by(fk_poll_id=poll_id,fk_user_id=current_user.id).order_by(PollsAnsweredObj.created_timestamp.desc()).first()
  if db_obj == None or db_obj == []:
    return False
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def check_if_currently_following_show_function(current_user, input_show_id, input_platform_id):
  db_obj = ShowsFollowingObj.query.filter_by(fk_user_id=current_user.id, fk_show_id=input_show_id, fk_platform_id=input_platform_id).first()
  if db_obj == None or db_obj == []:
    return None
  return db_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_platform_based_on_name_function(input_name):
  db_obj = PlatformsObj.query.filter_by(name=input_name,status=True).first()
  if db_obj == None or db_obj == []:
    return None
  return db_obj
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_age_demographics_function():
  # ------------------------ identify generations in arr start ------------------------
  generation_arr_silent = list(range(1928, 1945+1))
  generation_arr_boomers = list(range(1946, 1964+1))
  generation_arr_gen_x = list(range(1965, 1980+1))
  generation_arr_millenial = list(range(1981, 1996+1))
  generation_arr_gen_z = list(range(1997, 2012+1))
  generation_arr_gen_alpha = list(range(2013, 2023+1))
  # ------------------------ identify generations in arr end ------------------------
  # ------------------------ map generations to dict start ------------------------
  year_generation_dict = {}
  for i in generation_arr_silent:
    year_generation_dict[str(i)] = 'Silent'
  for i in generation_arr_boomers:
    year_generation_dict[str(i)] = 'Boomers'
  for i in generation_arr_gen_x:
    year_generation_dict[str(i)] = 'Gen X'
  for i in generation_arr_millenial:
    year_generation_dict[str(i)] = 'Millenials'
  for i in generation_arr_gen_z:
    year_generation_dict[str(i)] = 'Gen Z'
  for i in generation_arr_gen_alpha:
    year_generation_dict[str(i)] = 'Gen Alpha'
  # ------------------------ map generations to dict end ------------------------
  # ------------------------ generation options start ------------------------
  generation_options_arr = ['Silent','Boomers','Gen X','Millenials','Gen Z','Gen Alpha']
  # ------------------------ generation options end ------------------------
  return year_generation_dict, generation_options_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_age_group_function():
  # ------------------------ generation options start ------------------------
  age_group_options_arr = ["18-20's","30's","40's","50's","60's +"]
  # ------------------------ generation options end ------------------------
  return age_group_options_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_starting_arr_function(fk_poll_id):
  get_arr = []
  db_obj = PollsObj.query.filter_by(id=fk_poll_id).first()
  if db_obj == None or db_obj == []:
    return None
  else:
    get_str = db_obj.answer_choices
    get_arr = get_str.split('~')
  return get_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def default_chart_colors_function():
  colors_arr = [
    # primary, secondary
    ['rgb(13 110 253)','rgb(158 197 254 / 50%)','blue','blue_light'],
    ['rgb(13 202 240)','rgb(158 234 249 / 50%)','cyan','cyan_light'],
    ['rgb(25 135 84)','rgb(163 207 187 / 50%)','green','green_light'],
    ['rgb(253 126 20)','rgb(254 203 161 / 50%)','orange','orange_light'],
    ['rgb(214 51 132)','rgb(239 173 206 / 50%)','pink','pink_light'],
    ['rgb(111 66 193)','rgb(197 179 230 / 50%)','purple','purple_light'],
    ['rgb(220 53 69)','rgb(241 174 181 / 50%)','red','red_light'],
    ['rgb(32 201 151)','rgb(166 233 213 / 50%)','teal','teal_light'],
    ['rgb(255 193 7)','rgb(255 230 156 / 50%)','yellow','yellow_light']
  ]
  random_choice = random.choice(colors_arr)
  return random.choice(colors_arr)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_alphabet_arr_function():
  return ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_percent_mins_dict_function(url_show_id):
  limits_dict = {
    'Male': {
      'show_f467c480-b3ca-42cb-bfde-e27a3e49e285': float(0.20),
      'show_e2d3b89c-68dd-45cf-8b21-d25c24fa067e': float(0.20)
    },
    'Female': {
      'show_dbfdbe75-4d63-470a-83b4-bbbb161a55d6': float(0.27),
      'show_10553fd3-dbf4-48ad-bcea-3bbcb4b4f0c3': float(0.12)
    },
    'Other': {url_show_id: float(0.05)},
    'Other (please specify)': {url_show_id: float(0.05)},
    "I skipped/didn't like this episode (why?)": {url_show_id: float(0.05)},
    '$0k-$50k': {url_show_id: float(0.04)},
    '$201k-$250k':{url_show_id: float(0.05)},
    '$251k-$300k':{url_show_id: float(0.03)},
    '$300k+': {url_show_id: float(0.02)},
    'Blue collar ': {
      'show_10553fd3-dbf4-48ad-bcea-3bbcb4b4f0c3': float(0.25)
    },
    'No for religious reasons': {url_show_id: float(0.075)},
    'Ph. D.': {url_show_id: float(0.04)},
    'No formal education': {url_show_id: float(0.04)},
    'Student': {url_show_id: float(0.19)},
    'Retired': {url_show_id: float(0.01)},
    'Unemployed': {url_show_id: float(0.06)},
    'Silent': {url_show_id: float(0.01)},
    'Gen Alpha': {url_show_id: float(0.01)},
    'Boomers': {url_show_id: float(0.07)},
    'Living with parents or relatives': {url_show_id: float(0.08)},
    'Widowed': {url_show_id: float(0.05)},
    'Tennis': {url_show_id: float(0.07)}
  }
  return limits_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def rgb_to_hex_function(input_rgb_str):
  # rgb(220 53 69)
  numbers = re.findall(r'\d+', input_rgb_str)
  if len(numbers) == 3:
    r, g, b = map(int, numbers)
  return "#{:02x}{:02x}{:02x}".format(r, g, b)
# ------------------------ individual function end ------------------------