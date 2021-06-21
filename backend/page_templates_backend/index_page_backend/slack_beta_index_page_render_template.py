# -------------------------------------------------------------- Imports
import os
from flask import render_template, Blueprint, redirect, request, session, make_response
from backend.utils.page_www_to_non_www.check_if_url_www import check_if_url_www_function
from backend.utils.page_www_to_non_www.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
import datetime
from backend.utils.cached_login.cached_login_info import cached_login_info_function

# -------------------------------------------------------------- App Setup
slack_beta_index_page_render_template = Blueprint("slack_beta_index_page_render_template", __name__, static_folder="static", template_folder="templates")
@slack_beta_index_page_render_template.before_request
def before_request():
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=302)

# -------------------------------------------------------------- App
@slack_beta_index_page_render_template.route("/slack_beta", methods=['GET','POST'])
def slack_beta_index_page_render_template_function():
  print('=========================================== slack_beta_index_page_render_template_function START ===========================================')
  
  # ------------------------ CSS support START ------------------------
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')
  # ------------------------ CSS support END ------------------------


  # ------------------------ Check Broswer For Existing Cookie Then Redirect START ------------------------
  # Get cookie from browser if exists
  get_cookie_value_from_browser = request.cookies.get('triviafy_browser_cookie')

  # ------------------------ LocalHost Error Stop START ------------------------
  # -------------------------------------------------------------- Running on localhost
  server_env = os.environ.get('TESTING', 'false')
  # If running on localhost
  if server_env == 'true':
    # Connect to redis database pool (no need to close)
    redis_connection = redis_connect_to_database_function()

    # ------------------------ Set the Slack State Key START ------------------------
    # Make redis key:value pair and push to db (Slack State)
    localhost_slack_state_key = 'localhost_slack_state_key'
    localhost_slack_state_uuid_value = create_uuid_function('slv_')
    
    redis_connection.set(localhost_slack_state_key, localhost_slack_state_uuid_value.encode('utf-8'))
    # ------------------------ Set the Slack State Key END ------------------------

    # ------------------------ Set Redis For Cookie START ------------------------
    if get_cookie_value_from_browser == '' or get_cookie_value_from_browser == None:
      try:
        get_cookie_value_from_browser = redis_connection.get('localhost_redis_browser_cookie_key').decode('utf-8')
      except:
        get_cookie_value_from_browser = None
    # ------------------------ Set Redis For Cookie END ------------------------
  # ------------------------ LocalHost Error Stop END ------------------------

  
  # If cookie exists then check if info is cached in redis db
  if get_cookie_value_from_browser != '' and get_cookie_value_from_browser != None:
    redis_user_nested_dict = cached_login_info_function(get_cookie_value_from_browser)
    if redis_user_nested_dict == 'No obj stored in redis for this browser cookie.' or redis_user_nested_dict == '' or redis_user_nested_dict == None:
      print('No obj stored in redis for this browser cookie.')
    else:
      print('User sign in saved on cookie, redirecting user to loggedin dashboard!')
      print('=========================================== slack_beta_index_page_render_template_function END ===========================================')
      return redirect("/dashboard", code=302)
  # ------------------------ Check Broswer For Existing Cookie Then Redirect END ------------------------


  # ------------------------ If Browswer Cookie Does Not Exist START ------------------------
  # If cookie does not exist then set the cookie
  if get_cookie_value_from_browser == '' or get_cookie_value_from_browser == None:
    # Set cookie key:value pair for browser
    set_browser_cookie_key = 'triviafy_browser_cookie'
    set_browser_cookie_value = create_uuid_function('browsercke_')

  # -------------------------------------------------------------- Running on localhost
  server_env = os.environ.get('TESTING', 'false')
  # If running on localhost
  if server_env == 'true':
    # Connect to redis database pool (no need to close)
    redis_connection = redis_connect_to_database_function()
    
    # Make redis key:value pair and push to db (Browser Cookie). Need this becasue cookie does not save from page to page on localhost
    localhost_redis_browser_cookie_key = 'localhost_redis_browser_cookie_key'
    if get_cookie_value_from_browser == '' or get_cookie_value_from_browser == None:
      redis_connection.set(localhost_redis_browser_cookie_key, set_browser_cookie_value.encode('utf-8'))
    else:
      redis_connection.set(localhost_redis_browser_cookie_key, get_cookie_value_from_browser.encode('utf-8'))

    if get_cookie_value_from_browser == '' or get_cookie_value_from_browser == None:
      browser_response = make_response(render_template('index_page_templates/index_slack_beta.html', css_cache_busting = cache_busting_output, slack_state_uuid_html = localhost_slack_state_uuid_value))
      browser_response.set_cookie(set_browser_cookie_key, set_browser_cookie_value, expires=datetime.datetime.now() + datetime.timedelta(days=30))
      print('=========================================== slack_beta_index_page_render_template_function END ===========================================')
      return browser_response
    else:
      print('=========================================== slack_beta_index_page_render_template_function END ===========================================')
      return render_template('index_page_templates/index_slack_beta.html', css_cache_busting = cache_busting_output, slack_state_uuid_html = localhost_slack_state_uuid_value)

  # -------------------------------------------------------------- NOT running on localhost
  else:
    # Set the session variables in user's browser so that you can check it once user authorizes slack
    session['slack_state_uuid_key'] = create_uuid_function('slk_')
    session['slack_state_uuid_value'] = create_uuid_function('slv_')

    if get_cookie_value_from_browser == '' or get_cookie_value_from_browser == None:
      browser_response = make_response(render_template('index_page_templates/index_slack_beta.html', css_cache_busting = cache_busting_output, slack_state_uuid_html = session['slack_state_uuid_value']))
      browser_response.set_cookie(set_browser_cookie_key, set_browser_cookie_value, expires=datetime.datetime.now() + datetime.timedelta(days=30))
      print('=========================================== slack_beta_index_page_render_template_function END ===========================================')
      return browser_response
    else:
      print('=========================================== slack_beta_index_page_render_template_function END ===========================================')
      return render_template('index_page_templates/index_slack_beta.html', css_cache_busting = cache_busting_output, slack_state_uuid_html = session['slack_state_uuid_value'])