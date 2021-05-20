# -------------------------------------------------------------- Imports
from flask import render_template, Blueprint, redirect, request
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.cached_login.check_if_user_login_through_cookies import check_if_user_login_through_cookies_function

# -------------------------------------------------------------- App Setup
create_question_attempt_database_insert = Blueprint("create_question_attempt_database_insert", __name__, static_folder="static", template_folder="templates")
@create_question_attempt_database_insert.before_request
def before_request():
  """Returns: The domain should work with both www and non-www domain. But should always redirect to non-www version"""
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=301)

# -------------------------------------------------------------- App
@create_question_attempt_database_insert.route("/create/question/submitted/status", methods=['GET','POST'])
def create_question_attempt_database_insert_function():
  """Returns /create/question/submitted/status page"""
  print('=========================================== /create/question/submitted/status Page START ===========================================')
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')

  try:
    user_nested_dict = check_if_user_login_through_cookies_function()

    # Get user information from the nested dict
    user_company_name = user_nested_dict['user_company_name']
    user_channel_name = user_nested_dict['slack_channel_name']
    user_email = user_nested_dict['user_email']
  except:
    print('=========================================== /create/question/submitted/status Page END ===========================================')
    return redirect('/', code=301)
  
  print('=========================================== /create/question/submitted/status Page END ===========================================')
  return render_template('create_question_page_templates/create_question_submitted_status.html',
                          css_cache_busting = cache_busting_output,
                          user_company_name_to_html = user_company_name,
                          user_channel_name_to_html = user_channel_name,
                          user_email_to_html = user_email)