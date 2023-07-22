# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import re
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_email_function(user_input_email, is_signup='false'):
  desired_regex_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
  if(re.fullmatch(desired_regex_pattern, user_input_email)):
    # Check email for personal tags
    if is_signup == 'true':
      user_input_email = check_email_personal_tags_function(user_input_email)
    return user_input_email
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
# ------------------------ block email list start ------------------------
blocked_email_arr = [
  '@gartner.com',
  '@gmail.com',
  '@gmail',
  '@yahoo.',
  '@ymail.com',
  '@mail.com',
  '@msn.',
  '@aol.',
  '@fb.com',
  '@hotmail.',
  '@outlook.',
  '@topmail.ws',
  '@iopmail.com',
  '@mailinator.com',
  '@onmicrosoft.com',
  '@bingzone.net',
  '@msgsafe.io',
  '@sharklasers.com',
  '@ttirv.com',
  '@pm.me',
  '@protonmail.com',
  '@qq.com',
  '@gamil.com',
  '@gmal.com',
  '@me.com',
  '@yopmail.com',
  '@hey.com',
  '@icloud.com',
  '@fastmail.fm',
  '@mail.ru',
  '@web.de',
  '@ya.ru',
  '@vp.pl',
  '@inboxbear.com',
  '@tuks.co.za',
  '@kiabws.com',
  '@cikuh.com',
  '@relay.firefox.com',
  '@citromail.hu',
  '@mailpoof.com',
  '@biyac.com',
  '@byom.de',
  '@yandex.ru',
  '@naver.com',
  '@ukr.net',
  '@cuoly.com',
  '@zohomail.in',
  '@sltn.net',
  '@laposte.sn',
  '.edu']
# ------------------------ block email list end ------------------------
def check_email_personal_tags_function(user_input_email):
  for i_email in blocked_email_arr:
    if i_email in user_input_email.lower():
      return False
  return user_input_email
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_password_archive_v1_function(user_input_password):
  desired_regex_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
  if(re.fullmatch(desired_regex_pattern, user_input_password)):
    return user_input_password
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_password_function(user_input_password):
  if len(user_input_password) > 150 or len(user_input_password) < 4:
    return False
  return user_input_password
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_account_text_inputs_function(user_input):
  desired_regex_pattern = "^[\w\s-]{0,20}$"
  if(re.fullmatch(desired_regex_pattern, user_input)):
    return user_input
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_desired_langs_text_inputs_function(user_input):
  desired_regex_pattern = "^[\w\s,-]{1,150}$"
  if(re.fullmatch(desired_regex_pattern, user_input)):
    return user_input
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_account_text_inputs_large_function(user_input):
  if len(user_input) == 0:
    return False
  desired_regex_pattern = "^[\w\s-]{1,50}$"
  if(re.fullmatch(desired_regex_pattern, user_input)):
    return user_input
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_candidate_ui_answer_text_function(user_input):
  if len(user_input) == 0:
    return False
  desired_regex_pattern = "^[*]{1,100}$"
  if(re.fullmatch(desired_regex_pattern, user_input)):
    return user_input
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_question_categories_function(user_input):
  if len(user_input) == 0 or len(user_input) > 50:
    return False
  return user_input
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_char_count_1_function(user_input):
  if len(user_input) == 0 or len(user_input) > 100:
    return False
  return user_input
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_question_question_function(user_input):
  if len(user_input) == 0 or len(user_input) > 750:
    return False
  return user_input
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_question_options_function(user_input):
  if len(user_input) == 0 or len(user_input) > 280:
    return False
  return user_input
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_question_option_e_function(user_input):
  if user_input == None or user_input == '':
    return user_input
  if len(user_input) > 280:
    return False
  return user_input
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_question_answer_function(user_input):
  if len(user_input) == 0 or len(user_input) > 2:
    return False
  allowed_answers_arr = ['a','b','c','d','e']
  if user_input.lower() in allowed_answers_arr:
    return user_input
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_create_question_difficulty_function(user_input):
  if len(user_input) == 0 or len(user_input) > 7:
    return False
  allowed_answers_arr = ['easy','medium','hard']
  if user_input.lower() in allowed_answers_arr:
    return user_input
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_candidate_ui_answer_radio_function(user_input):
  if len(user_input) == 0 or len(user_input) > 2:
    return False
  allowed_answers_arr = ['a','b','c','d','e']
  if user_input.lower() in allowed_answers_arr:
    return user_input
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_loop_check_if_exists_within_arr_function(user_input_arr, correct_master_arr):
  if user_input_arr == None or len(user_input_arr) == 0 or user_input_arr == []:
    return False
  for i_str in user_input_arr:
    if i_str not in correct_master_arr:
      localhost_print_function('user input provided is not an option')
      return False
  return user_input_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_check_if_str_exists_within_arr_function(user_input_str, correct_master_arr):
  if user_input_str == None:
    return False
  if len(user_input_str) == 0:
    return False
  if user_input_str not in correct_master_arr:
    localhost_print_function('user input provided is not an option')
    return False
  return user_input_str
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def check_if_question_id_arr_exists_function(user_input_arr):
  for i in user_input_arr:
    sql_result = select_general_function('select_question_id_actually_exists_v2', i)
    if sql_result == [] or len(sql_result) == 0:
      return False
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_letters_numbers_spaces_only_function(user_input):
  if len(user_input) == 0 or len(user_input) > 100:
    return False
  desired_regex_pattern = "^[a-zA-Z0-9 ]{1,100}$"
  if(re.fullmatch(desired_regex_pattern, user_input)):
    return user_input
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_special_characters_function():
  special_characters_arr = [':',';','<','>','@','|','~','`','%','^','[',']','{','}','(',')']
  return special_characters_arr
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def alert_message_default_function():
  # localhost_print_function('=========================================== alert_message_default_function START ===========================================')
  alert_message_page = ''
  alert_message_type = 'danger'
  # localhost_print_function('=========================================== alert_message_default_function END ===========================================')
  return alert_message_page, alert_message_type
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def alert_message_default_function_v2(redirect_var=None):
  # localhost_print_function('=========================================== alert_message_default_function_v2 START ===========================================')
  # ------------------------ errors start ------------------------
  alert_message_dict = {
      'message':'',
      'type':'danger'
    }
  if redirect_var == None:
    pass
  elif redirect_var == 'e1':
    alert_message_dict = {
      'message':'Please enter a valid work email. No @gmail, @yahoo, etc.',
      'type':'danger'
    }
  elif redirect_var == 'e2':
    alert_message_dict = {
      'message':'Please enter a valid password.',
      'type':'danger'
    }
  elif redirect_var == 'e3':
    alert_message_dict = {
      'message':'Account already created for email.',
      'type':'danger'
    }
  elif redirect_var == 'e4':
    alert_message_dict = {
      'message':'Incorrect username/password.',
      'type':'danger'
    }
  elif redirect_var == 'e5':
    alert_message_dict = {
      'message':'Requested categories should be 1-100 characters long.',
      'type':'danger'
    }
  elif redirect_var == 'e6':
    alert_message_dict = {
      'message':'Invalid inputs.',
      'type':'danger'
    }
  elif redirect_var == 'e7':
    alert_message_dict = {
      'message':'You must select at least 1 category.',
      'type':'danger'
    }
  elif redirect_var == 'e8':
    alert_message_dict = {
      'message':'Your quiz start day/time must be at least 1 hour before your quiz end day/time.',
      'type':'danger'
    }
  elif redirect_var == 'e9':
    alert_message_dict = {
      'message':'You are not an admin.',
      'type':'danger'
    }
  elif redirect_var == 'e10':
    alert_message_dict = {
      'message':'Email invalid.',
      'type':'danger'
    }
  elif redirect_var == 'e11':
    alert_message_dict = {
      'message':'User is the only person within group.',
      'type':'danger'
    }
  elif redirect_var == 'e12':
    alert_message_dict = {
      'message':'Select at least one category that you want to test a candidate on.',
      'type':'danger'
    }
  elif redirect_var == 'e13':
    alert_message_dict = {
      'message':'You are not a subscribed user, see account settings.',
      'type':'danger'
    }
  elif redirect_var == 'e14':
    alert_message_dict = {
      'message':'Subscription required.',
      'type':'danger'
    }
  elif redirect_var == 'e15':
    alert_message_dict = {
      'message':'Invalid answer choice/inputs.',
      'type':'danger'
    }
  elif redirect_var == 'e16':
    alert_message_dict = {
      'message':'Invalid question ID.',
      'type':'danger'
    }
  elif redirect_var == 'e17':
    alert_message_dict = {
      'message':'Please select valid question.',
      'type':'danger'
    }
  elif redirect_var == 'e18':
    alert_message_dict = {
      'message':'Please avoid using special characters in your answer.',
      'type':'danger'
    }
  elif redirect_var == 'e19':
    alert_message_dict = {
      'message':'Please shorten your response.',
      'type':'danger'
    }
  elif redirect_var == 'e20':
    alert_message_dict = {
      'message':'Invalid month.',
      'type':'danger'
    }
  elif redirect_var == 'e21':
    alert_message_dict = {
      'message':'Invalid month/day combination.',
      'type':'danger'
    }
  elif redirect_var == 'e22':
    alert_message_dict = {
      'message':'Prveious team trivia contest discarded.',
      'type':'danger'
    }
  elif redirect_var == 'e23':
    alert_message_dict = {
      'message':'Question replaced.',
      'type':'danger'
    }
  elif redirect_var == 'e24':
    alert_message_dict = {
      'message':'Activity must be defined',
      'type':'danger'
    }
  elif redirect_var == 'e25':
    alert_message_dict = {
      'message':"Your team's free trial has expired. Please select a subscription below and your team will then be able to continue using our automated team building activities.",
      'type':'danger'
    }
  elif redirect_var == 'e26':
    alert_message_dict = {
      'message':"Invalid year/month combination.",
      'type':'danger'
    }
  elif redirect_var == 'e27':
    alert_message_dict = {
      'message':"You cannot select the same question as your previous selection.",
      'type':'danger'
    }
  elif redirect_var == 'e28':
    alert_message_dict = {
      'message':"That is an invalid or expired token.",
      'type':'danger'
    }
  elif redirect_var == 'e29':
    alert_message_dict = {
      'message':"Passwords do not match.",
      'type':'danger'
    }
  elif redirect_var == 'e30':
    alert_message_dict = {
      'message':"You must be 18+ years old to participate in HerdReviews polling.",
      'type':'danger'
    }
  elif redirect_var == 'e31':
    alert_message_dict = {
      'message':"Please select that show from the below selection.",
      'type':'danger'
    }
  elif redirect_var == 'e32':
    alert_message_dict = {
      'message':"Show name not found.",
      'type':'danger'
    }
  elif redirect_var == 'e33':
    alert_message_dict = {
      'message':"Currently only 'Podcasts' are supported.",
      'type':'danger'
    }
  elif redirect_var == 'e34':
    alert_message_dict = {
      'message':"There was an error with the podcast title, please try again.",
      'type':'danger'
    }
  elif redirect_var == 'e35':
    alert_message_dict = {
      'message':"You have reached your daily limit for this poll.",
      'type':'danger'
    }
  elif redirect_var == 'e36':
    alert_message_dict = {
      'message':"Invalid question",
      'type':'danger'
    }
  elif redirect_var == 'e37':
    alert_message_dict = {
      'message':"Invalid answer choice. Please avoid using special characters or making your response too long.",
      'type':'danger'
    }
  elif redirect_var == 'e38':
    alert_message_dict = {
      'message':"Your answer choices are too lengthy.",
      'type':'danger'
    }
  elif redirect_var == 'e39':
    alert_message_dict = {
      'message':"You need more than 1 answer choice",
      'type':'danger'
    }
  elif redirect_var == 'e40':
    alert_message_dict = {
      'message':"You reached your poll submission daily limit for this show.",
      'type':'danger'
    }
  elif redirect_var == 'e41':
    alert_message_dict = {
      'message':"Poll not available or not yet approved.",
      'type':'danger'
    }
  elif redirect_var == 'e43':
    alert_message_dict = {
      'message':"You have not yet created any custom polls.",
      'type':'danger'
    }
  # ------------------------ errors end ------------------------
  # ------------------------ success start ------------------------
  elif redirect_var == 's1':
    alert_message_dict = {
      'message':'Request sent.',
      'type':'success'
    }
  elif redirect_var == 's2':
    alert_message_dict = {
      'message':'Schedule settings successfully updated. They will go into effect on your NEXT team quiz.',
      'type':'success'
    }
  elif redirect_var == 's3':
    alert_message_dict = {
      'message':'Team trivia contest created, submit your activity answers now!',
      'type':'success'
    }
  elif redirect_var == 's4':
    alert_message_dict = {
      'message':'Answers successfully saved. The grading/winner will be announced by email when your quiz closes.',
      'type':'success'
    }
  elif redirect_var == 's5':
    alert_message_dict = {
      'message':'Subscription successfully updated.',
      'type':'success'
    }
  elif redirect_var == 's6':
    alert_message_dict = {
      'message':'Password updated!',
      'type':'success'
    }
  elif redirect_var == 's7':
    alert_message_dict = {
      'message':'Emails sent!',
      'type':'success'
    }
  elif redirect_var == 's8':
    alert_message_dict = {
      'message':'Check your spam/promotions folder and mark HerdReviews as "Not Spam". A verification link has been successfully sent to your email.',
      'type':'success'
    }
  elif redirect_var == 's9':
    alert_message_dict = {
      'message':'Your email has been successfully verified.',
      'type':'success'
    }
  elif redirect_var == 's10':
    alert_message_dict = {
      'message':'Successfully added',
      'type':'success'
    }
  elif redirect_var == 's11':
    alert_message_dict = {
      'message':'Successfully reset default settings',
      'type':'success'
    }
  elif redirect_var == 's12':
    alert_message_dict = {
      'message':'Successfully submitted',
      'type':'success'
    }
  elif redirect_var == 's13':
    alert_message_dict = {
      'message':'Check your spam/promotions folder and mark HerdReviews as "Not Spam". A password reset link has been successfully sent to your email.',
      'type':'success'
    }
  elif redirect_var == 's14':
    alert_message_dict = {
      'message':'Successfully following show. Scroll to see poll status below.',
      'type':'success'
    }
  elif redirect_var == 's15':
    alert_message_dict = {
      'message':'You are already following this show, search below.',
      'type':'success'
    }
  elif redirect_var == 's16':
    alert_message_dict = {
      'message':'Successfully following show, start polling below.',
      'type':'success'
    }
  elif redirect_var == 's17':
    alert_message_dict = {
      'message':'You are up to date with the newest show polls.',
      'type':'success'
    }
  elif redirect_var == 's18':
    alert_message_dict = {
      'message':'You are up to date with the latest user polls.',
      'type':'success'
    }
  elif redirect_var == 's19':
    alert_message_dict = {
      'message':'Poll successfully created! Pending admin final approval.',
      'type':'success'
    }
  # ------------------------ success end ------------------------
  # ------------------------ info end ------------------------
  elif redirect_var == 'i1':
    alert_message_dict = {
      'message':'Schedule settings unchanged.',
      'type':'info'
    }
  elif redirect_var == 'i2':
    alert_message_dict = {
      'message':'User is subscribed.',
      'type':'info'
    }
  elif redirect_var == 'i3':
    alert_message_dict = {
      'message':'Request already sent.',
      'type':'info'
    }
  # ------------------------ info end ------------------------
  # ------------------------ warning end ------------------------
  elif redirect_var == 'w1':
    alert_message_dict = {
      'message':'Deleted!',
      'type':'warning'
    }
  elif redirect_var == 'w2':
    alert_message_dict = {
      'message':'Poll successfully received',
      'type':'warning'
    }
  elif redirect_var == 'w3':
    alert_message_dict = {
      'message':'You must create an account to submit your answer',
      'type':'warning'
    }
  # ------------------------ warning end ------------------------
  # localhost_print_function('=========================================== alert_message_default_function_v2 END ===========================================')
  return alert_message_dict
# ------------------------ individual function end ------------------------