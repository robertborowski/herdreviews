# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from backend.utils.cached_login.check_if_user_login_through_cookies import check_if_user_login_through_cookies_function
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.insert_queries.insert_triviafy_quiz_feedback_responses_table import insert_triviafy_quiz_feedback_responses_table_function
from backend.utils.sanitize_user_inputs.sanitize_feedback_user import sanitize_feedback_user_function
from backend.utils.free_trial_period_utils.check_if_free_trial_period_is_expired_days_left import check_if_free_trial_period_is_expired_days_left_function

# -------------------------------------------------------------- App Setup
quiz_feedback_processing = Blueprint("quiz_feedback_processing", __name__, static_folder="static", template_folder="templates")
@quiz_feedback_processing.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@quiz_feedback_processing.route("/quiz/team/feedback/processing", methods=['GET','POST'])
def quiz_feedback_processing_function():
  print('=========================================== /quiz/team/feedback/processing Page START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  try:
    # ------------------------ Page Load User Pre Checks START ------------------------
    # Check if user logged in through cookies
    user_nested_dict = check_if_user_login_through_cookies_function()

    # Check if user free trial is expired
    user_nested_dict = check_if_free_trial_period_is_expired_days_left_function(user_nested_dict)
    if user_nested_dict == None or user_nested_dict == True:
      return redirect('/subscription', code=302)

    days_left = str(user_nested_dict['trial_period_days_left_int']) + " days left."
    if user_nested_dict['trial_period_days_left_int'] == 1:
      days_left = str(user_nested_dict['trial_period_days_left_int']) + " day left."

    free_trial_ends_info = "Free Trial Ends: " + user_nested_dict['free_trial_end_date'] + ", " + days_left
    # ------------------------ Page Load User Pre Checks END ------------------------
    
    
    user_uuid = user_nested_dict['user_uuid']


    # ------------------------ Get Form User Input START ------------------------
    # NOTE: Need to sanitize this before production
    user_input_feedback_form = sanitize_feedback_user_function(request.form.get('user_input_quiz_feedback'))
    # ------------------------ Get Form User Input END ------------------------


    # ------------------------ Create Variables for DB START ------------------------
    user_feedback_uuid = create_uuid_function('feedbckid_')
    user_feedback_timestamp = create_timestamp_function()
    # ------------------------ Create Variables for DB END ------------------------


    # ------------------------ Upload Feedback to DB START ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()
    
    # Insert feedback to DB
    output_message = insert_triviafy_quiz_feedback_responses_table_function(postgres_connection, postgres_cursor, user_feedback_uuid, user_feedback_timestamp, user_uuid, user_input_feedback_form)
    print(output_message)
    
    # Close postgres db connection
    postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
    # ------------------------ Upload Feedback to DB END ------------------------

    
  except:
    print('page load except error hit')
    print('=========================================== /quiz/team/feedback/processing Page END ===========================================')
    return redirect('/logout', code=302)
    # return redirect('/', code=302)

  
  print('=========================================== /quiz/team/feedback/processing Page END ===========================================')
  return redirect('/quiz/team/feedback/submit', code=302)