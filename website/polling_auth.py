# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -note: any pages related to authentication will be in this auth.py file
# -@login_required   # this decorator says that url cannot be accessed unless the user is logged in. 
# -@login_required: <-- This decorator will bring a user to __init__ code: [login_manager.login_view = 'auth.candidates_login_page_function'] if they hit a page that requires login and they are not logged in.
# -use code: <methods=['GET', 'POST']> when you want the user to interact with the page through forms/checkbox/textbox/radio/etc.
# ------------------------ info about this file end ------------------------

# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from website.backend.candidates.user_inputs import sanitize_email_function, sanitize_password_function
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_connect_to_database_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from website.backend.candidates.send_emails import send_email_template_function
import os
from website.backend.candidates.user_inputs import alert_message_default_function_v2
from .models import UserObj
from website.backend.sql_statements.select import select_general_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
polling_auth = Blueprint('polling_auth', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@polling_auth.route('/signup', methods=['GET', 'POST'])
@polling_auth.route('/signup/', methods=['GET', 'POST'])
@polling_auth.route('/signup/<url_redirect_code>', methods=['GET', 'POST'])
def polling_signup_function(url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ get all podcasts start ------------------------
  page_dict['shows_arr_of_dicts'] = []
  show_arr_of_dict = select_general_function('select_query_general_8')
  for i in show_arr_of_dict:
    page_dict['shows_arr_of_dicts'].append(i)
  # ------------------------ get all podcasts end ------------------------
  if request.method == 'POST':
    # ------------------------ post method hit #2 - full sign up start ------------------------
    ui_email = request.form.get('uiEmail')
    ui_password = request.form.get('uiPassword')
    # ------------------------ sanitize/check user inputs start ------------------------
    # ------------------------ sanitize/check user input email start ------------------------
    ui_email_cleaned = sanitize_email_function(ui_email, 'false')
    if ui_email_cleaned == False:
      return redirect(url_for('polling_auth.polling_signup_function', url_redirect_code='e1'))
    # ------------------------ sanitize/check user input email end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_cleaned = sanitize_password_function(ui_password)
    if ui_password_cleaned == False:
      return redirect(url_for('polling_auth.polling_signup_function', url_redirect_code='e2'))
    # ------------------------ sanitize/check user input password end ------------------------
    # ------------------------ sanitize/check user inputs end ------------------------
    # ------------------------ check if user email already exists in db start ------------------------
    user_exists = UserObj.query.filter_by(email=ui_email,signup_product='polling').first()
    if user_exists != None and user_exists != []:
      return redirect(url_for('polling_auth.polling_signup_function', url_redirect_code='e3'))
    # ------------------------ check if user email already exists in db start ------------------------
    else:
      # ------------------------ create new user in db start ------------------------
      new_row = UserObj(
        id=create_uuid_function('user_'),
        created_timestamp=create_timestamp_function(),
        email=ui_email.lower(),
        password=generate_password_hash(ui_password, method="sha256"),
        verified_email = False,
        signup_product = 'polling'
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ create new user in db end ------------------------
      # ------------------------ keep user logged in start ------------------------
      login_user(new_row, remember=True)
      # ------------------------ keep user logged in end ------------------------
      # ------------------------ email self start ------------------------
      try:
        output_to_email = os.environ.get('TRIVIAFY_NOTIFICATIONS_EMAIL')
        output_subject = f'Polling - Signup - {ui_email}'
        output_body = f"Hi there,\n\nNew user signed up: {ui_email} \n\nBest,\nTriviafy"
        send_email_template_function(output_to_email, output_subject, output_body)
      except:
        pass
      # ------------------------ email self end ------------------------
      return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # ------------------------ post method hit #2 - full sign up end ------------------------
  return render_template('polling/exterior/signup/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_auth.route('/login', methods=['GET', 'POST'])
@polling_auth.route('/login/', methods=['GET', 'POST'])
@polling_auth.route('/login/<url_redirect_code>', methods=['GET', 'POST'])
def polling_login_function(url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ auto sign in with cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    try:
      user_id_from_redis = redis_connection.get(get_cookie_value_from_browser).decode('utf-8')
      if user_id_from_redis != None:
        user = UserObj.query.filter_by(id=user_id_from_redis,signup_product='polling').first()
        # ------------------------ force logout same email logged into different product start ------------------------
        if user == None:
          try:
            redis_connection.delete(get_cookie_value_from_browser)
            localhost_print_function(f'delete redis key for user logged into different Triviafy product. Deleted: {get_cookie_value_from_browser}')
            logout_user()
            localhost_print_function('redirect to login page - polling')
            return redirect(url_for('polling_auth.polling_login_function'))
          except:
            pass
        # ------------------------ force logout same email logged into different product end ------------------------
        # ------------------------ keep user logged in start ------------------------
        if user != None:
          try:
            login_user(user, remember=True)
          except:
            pass
        # ------------------------ keep user logged in end ------------------------
        localhost_print_function('redirect to dashboard page - polling')
        return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    except:
      pass
  # ------------------------ auto sign in with cookie end ------------------------
  # ------------------------ get all podcasts start ------------------------
  page_dict['shows_arr_of_dicts'] = []
  show_arr_of_dict = select_general_function('select_query_general_8')
  for i in show_arr_of_dict:
    page_dict['shows_arr_of_dicts'].append(i)
  # ------------------------ get all podcasts end ------------------------
  if request.method == 'POST':
    # ------------------------ post method hit #1 - regular login start ------------------------
    # ------------------------ post request sent start ------------------------
    ui_email = request.form.get('uiEmail')
    ui_password = request.form.get('uiPassword')
    # ------------------------ post request sent end ------------------------
    # ------------------------ sanitize/check user input email start ------------------------
    ui_email_cleaned = sanitize_email_function(ui_email)
    if ui_email_cleaned == False:
      return redirect(url_for('polling_auth.polling_login_function', url_redirect_code='e1'))
    # ------------------------ sanitize/check user input email end ------------------------
    # ------------------------ sanitize/check user input password start ------------------------
    ui_password_cleaned = sanitize_password_function(ui_password)
    if ui_password_cleaned == False:
      return redirect(url_for('polling_auth.polling_login_function', url_redirect_code='e2'))
    # ------------------------ sanitize/check user input password end ------------------------
    user = UserObj.query.filter_by(email=ui_email,signup_product='polling').first()
    if user:
      if check_password_hash(user.password, ui_password):
        # ------------------------ keep user logged in start ------------------------
        login_user(user, remember=True)
        # ------------------------ keep user logged in end ------------------------
        return redirect(url_for('polling_views_interior.polling_dashboard_function'))
      else:
        return redirect(url_for('polling_auth.polling_login_function', url_redirect_code='e4'))
    else:
      return redirect(url_for('polling_auth.polling_login_function', url_redirect_code='e4'))
    # ------------------------ post method hit #1 - regular login end ------------------------
  return render_template('polling/exterior/login/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_auth.route('/logout')
@polling_auth.route('/logout/')
@login_required
def polling_logout_function():
  logout_user()
  # ------------------------ auto sign in with cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  # ------------------------ auto sign in with cookie end ------------------------
  if get_cookie_value_from_browser != None:
    try:
      redis_connection.delete(get_cookie_value_from_browser)
    except:
      pass
  # ------------------------ auto sign in with cookie end ------------------------
  return redirect(url_for('polling_auth.polling_login_function'))
# ------------------------ individual route end ------------------------