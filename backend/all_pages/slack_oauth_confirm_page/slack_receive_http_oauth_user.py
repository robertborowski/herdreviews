from flask import render_template, Blueprint, redirect, request, session, make_response
from backend.utils.app_setup_before.check_if_url_www import check_if_url_www_function
from backend.utils.app_setup_before.remove_www_from_domain import remove_www_from_domain_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
import os
from slack_sdk import WebClient
from backend.db.connection.redis_connect_to_database import redis_connect_to_database_function
from backend.all_pages.slack_oauth_confirm_page.update_db_new_user_store_obj_redis_cookie import update_db_new_user_store_obj_redis_cookie_function
from backend.all_pages.slack_oauth_confirm_page.user_store_loggedin_data_redis import user_store_loggedin_data_redis_function
from backend.utils.pretty_print.pretty_print import pretty_print_function

slack_receive_http_oauth_user = Blueprint("slack_receive_http_oauth_user", __name__, static_folder="static", template_folder="templates")

@slack_receive_http_oauth_user.before_request
def before_request():
  """Returns: The domain should work with both www and non-www domain. But should always redirect to non-www version"""
  www_start = check_if_url_www_function(request.url)
  if www_start:
    new_url = remove_www_from_domain_function(request.url)
    return redirect(new_url, code=301)

@slack_receive_http_oauth_user.route("/finish_auth", methods=['GET','POST'])
def slack_receive_http_oauth_user_function():
  """Returns: Authenticates user access and stores login info in database"""  
  print('=========================================== /finish_auth Page START ===========================================')
  # Need to create a css unique key so that cache busting can be done
  cache_busting_output = create_uuid_function('css_')

  # -------------------------------------------------------------- Running on localhost
  server_env = os.environ.get('TESTING', 'false')
  # If running on localhost
  if server_env == 'true':
    # Connect to redis database pool (no need to close)
    redis_connection = redis_connect_to_database_function()

    # Get key:value from redis then delete row from redis
    localhost_slack_state_key = 'localhost_slack_state_key'
    slack_state_value_passed_in_url = redis_connection.get(localhost_slack_state_key).decode('utf-8')
    redis_connection.delete(localhost_slack_state_key)

    # Get key:value from redis then delete row from redis
    localhost_redis_browser_cookie_key = 'localhost_redis_browser_cookie_key'
    get_cookie_value_from_browser = redis_connection.get(localhost_redis_browser_cookie_key).decode('utf-8')
    #redis_connection.delete(localhost_redis_browser_cookie_key) --> DONT Delete this here. When on localhost delete this only when the user clicks Log Out.

  # -------------------------------------------------------------- NOT running on localhost
  else:
    slack_state_value_passed_in_url = session['slack_state_uuid_value']
    get_cookie_value_from_browser = request.cookies.get('triviafy_browser_cookie')

  # -------------------------------------------------------------- Slack authentication
  # Set up client
  slack_bot_token = os.environ.get('SLACK_BOT_TOKEN')
  client = WebClient(token=slack_bot_token)
  # My Slack Client ID and Client Secret for authentication
  my_slack_client_id = os.environ.get('SLACK_CLIENT_ID')
  my_slack_client_secret = os.environ.get('SLACK_CLIENT_SECRET')
  # Get info from the received URL from Slack once user accepts
  auth_code_received = request.args['code']
  state_received = request.args['state']

  # Authorize slack app for user
  if state_received == slack_state_value_passed_in_url:
    try:
      authed_response_obj = client.oauth_v2_access(
        client_id = my_slack_client_id,
        client_secret = my_slack_client_secret,
        code = auth_code_received
      )

      # With the response object, update the postgres database for user
      user_nested_dict = update_db_new_user_store_obj_redis_cookie_function(client, authed_response_obj)

      user_store_in_redis_status = user_store_loggedin_data_redis_function(user_nested_dict, get_cookie_value_from_browser)
      print(user_store_in_redis_status)
      
    except:
      print('Error while running "slack_receive_http_oauth_user" script.')

  print('=========================================== /finish_auth Page END ===========================================')
  # Render the login page template, pass in the redis nested dict of all user info
  return render_template('dashboard/dashboard_page.html', css_cache_busting = cache_busting_output)