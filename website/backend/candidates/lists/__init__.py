# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import datetime
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_arr_associated_index_function(input_arr):
  arr_index = []
  total_activities = len(input_arr)
  for i in range(total_activities):
    arr_index.append(i)
  return arr_index
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def make_arr_dict_function(arr, arr_index):
  dict_one = {
    'arr': arr,
    'arr_index': arr_index
  }
  return dict_one
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_team_building_activities_list_function():
  activities_list = [
    'Trivia',
    'Picture quizzes',
    'Icebreakers',
    'Employee surveys',
    'Personality tests',
    'Colleague birthday trivia',
    'Most likely to',
    'This or that',
    'Watercooler starters',
    'Word games',
    '2 player games',
    'Create custom questions'
  ]
  activities_list_index = get_arr_associated_index_function(activities_list)
  return activities_list, activities_list_index
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_marketing_list_function():
  temp_list = [
    'Google',
    'Colleague shared team link',
    'LinkedIn',
    'TikTok',
    'X (Twitter)',
    'Facebook',
    'Instagram',
    'Word of mouth'
  ]
  temp_list_index = get_arr_associated_index_function(temp_list)
  return temp_list, temp_list_index
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_marketing_list_v2_function():
  temp_list = [
    'Google',
    'Word of mouth',
    'Podcast',
    'YouTube',
    'X (Twitter)',
    'Reddit',
    'TikTok',
    'LinkedIn',
    'Facebook',
    'Instagram',
    'Other'
  ]
  temp_list_index = get_arr_associated_index_function(temp_list)
  return temp_list, temp_list_index
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_month_days_years_function():
  months_arr = [1,2,3,4,5,6,7,8,9,10,11,12]
  days_arr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
  month_day_dict = {
    '1': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    '2': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
    '3': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    '4': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    '5': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    '6': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    '7': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    '8': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    '9': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    '10': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    '11': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
    '12': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
  }
  # ------------------------ get years start ------------------------
  current_year = datetime.datetime.now().year
  years_arr = list(range(current_year, 1940, -1))
  # ------------------------ get years end ------------------------
  return months_arr, days_arr, years_arr, month_day_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_favorite_questions_function():
  questions_arr = [
    "type of music or band?",
    "movie or TV show?",
    "type of food or cuisine?",
    "book or author?",
    "hobby or pastime?",
    "place to visit on vacation?",
    "season or time of year?",
    "sport or sports team?",
    "thing to do on weekends?",
    "memory from childhood?",
    "form of exercise or physical activity?",
    "way to unwind after a long day?",
    "technology gadget or device?",
    "motivational quote or saying?",
    "app or online tool that helps you stay organized?",
    "board game or card game?",
    "inspirational or self-help book?",
    "productivity hack or time-saving technique?",
    "way to stay updated on current events or news?",
    "podcast or audiobook?",
    "website or online resource for learning new things?",
    "way to handle stress or pressures?",
    "method for brainstorming or generating creative ideas?",
    "team-building activity or icebreaker game?",
    "TED Talk or public speaking presentation?",
    "professional achievement or milestone in your career?",
    "color?",
    "animal?",
    "movie genre?",
    "holiday?",
    "dessert?",
    "season of the year?",
    "hobby?",
    "book genre?",
    "type of exercise?",
    "travel destination?",
    "social media platform?",
    "childhood memory?",
    "type of art?",
    "way to relax?",
    "type of weather?",
    "subject in school?",
    "type of transportation?",
    "type of cuisine?",
    "type of technology?",
    "type of clothing?"
  ]
  questions_arr_index = get_arr_associated_index_function(questions_arr)
  return questions_arr, questions_arr_index
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_dashboard_accordian_function():
  activity_a_accordian_arr = [
    ["collapseOne","trivia"],
    ["collapseTwo","picture_quiz"]
   ]
  activity_b_accordian_arr = [
    ["collapseThree","icebreakers"]
   ]
  return activity_a_accordian_arr, activity_b_accordian_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_activity_a_products_function():
  activity_a_products_list = ["trivia","picture_quiz"]
  return activity_a_products_list
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_activity_b_products_function():
  activity_products_list = ["icebreakers"]
  return activity_products_list
# ------------------------ individual function end ------------------------