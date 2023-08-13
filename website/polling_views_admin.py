# ------------------------ info about this file start ------------------------
# -routes = pages. Examples: [landing, about, faq, pricing] pages = routes
# -in this file we store the standard routes for our website
# -Note: any pages related to authentication will not be in this file, they will be routed in the auth.py file.
# -@login_required   # this decorator says that url cannot be accessed unless the user is logged in. 
# -@login_required: <-- This decorator will bring a user to __init__ code: [login_manager.login_view = 'auth.candidates_login_page_function'] if they hit a page that requires login and they are not logged in.
# -use code: <methods=['GET', 'POST']> when you want the user to interact with the page through forms/checkbox/textbox/radio/etc.
# ------------------------ info about this file end ------------------------

# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_connect_to_database_function
from website import db
from website.backend.candidates.user_inputs import alert_message_default_function_v2
import os
from website.backend.selenium_script import reddit_scrape_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
polling_views_admin = Blueprint('polling_views_admin', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_admin.route('/admin', methods=['GET', 'POST'])
@polling_views_admin.route('/admin/', methods=['GET', 'POST'])
@polling_views_admin.route('/admin/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def polling_dashboard_function(url_redirect_code=None):
  # ------------------------ check admin status start ------------------------
  if current_user.email != os.environ.get('RUN_TEST_EMAIL'):
    return redirect(url_for('polling_views_interior.polling_dashboard_function'))
  # ------------------------ check admin status end ------------------------
  # ------------------------ page dict start ------------------------
  if url_redirect_code == None:
    try:
      url_redirect_code = request.args.get('url_redirect_code')
    except:
      pass
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ submission start ------------------------
  if request.method == 'POST':
    # ------------------------ get ui start ------------------------
    ui_reddit_button = request.form.get('ui_reddit_button')
    # ------------------------ get ui end ------------------------
    if ui_reddit_button == 'on':
      reddit_scrape_run = reddit_scrape_function()
  # ------------------------ submission end ------------------------    
  localhost_print_function(' ------------- 100-admin start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-admin end ------------- ')
  return render_template('polling/admin_templates/dashboard/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------
