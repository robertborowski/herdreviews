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
from website.models import RedditPostsObj, PollsObj, RedditMappingObj, HostMarketingObj
from website.backend.reddit_api import reddit_api_posts_and_comments_function, reddit_api_send_messages_function
from website.backend.candidates.user_inputs import sanitize_email_function
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
def admin_function(url_redirect_code=None):
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
    ui_reddit_input = request.form.get('ui_reddit_input')
    ui_poll_input = request.form.get('ui_poll_input')
    ui_reddit_api_button_posts_and_comments = request.form.get('ui_reddit_api_button_posts_and_comments')
    ui_reddit_api_button_send_messages = request.form.get('ui_reddit_api_button_send_messages')
    # ------------------------ get ui end ------------------------
    # ------------------------ reddit poll mapping start ------------------------
    if ui_reddit_input != None and ui_poll_input != None:
      obj_reddit = RedditPostsObj.query.filter_by(id=ui_reddit_input).first()
      obj_poll = PollsObj.query.filter_by(id=ui_poll_input).first()
      if obj_reddit != None and obj_reddit != [] and obj_poll != None and obj_poll != []:
        # ------------------------ check if already mapped start ------------------------
        obj_map = RedditMappingObj.query.filter_by(fk_poll_id=ui_poll_input,fk_reddit_post_id=ui_reddit_input).first()
        if obj_map != None and ui_reddit_input != []:
          return redirect(url_for('polling_views_admin.admin_function', url_redirect_code='e45'))
        # ------------------------ check if already mapped end ------------------------
        else:
          # ------------------------ insert to db start ------------------------
          new_row = RedditMappingObj(
            id=create_uuid_function('map_'),
            created_timestamp=create_timestamp_function(),
            fk_poll_id=ui_poll_input,
            fk_reddit_post_id=ui_reddit_input
          )
          db.session.add(new_row)
          db.session.commit()
          # ------------------------ insert to db end ------------------------
          return redirect(url_for('polling_views_admin.admin_function', url_redirect_code='s21'))
    # ------------------------ reddit poll mapping end ------------------------
    # ------------------------ reddit posts and comments start ------------------------
    if ui_reddit_api_button_posts_and_comments == 'on':
      reddit_api_run = reddit_api_posts_and_comments_function()
      return redirect(url_for('polling_views_admin.admin_function', url_redirect_code='s21'))
    # ------------------------ reddit posts and comments end ------------------------
    # # ------------------------ reddit send messages start ------------------------
    # if ui_reddit_api_button_send_messages == 'on':
    #   reddit_api_run = reddit_api_send_messages_function()
    #   return redirect(url_for('polling_views_admin.admin_function', url_redirect_code='s21'))
    # # ------------------------ reddit send messages end ------------------------
  # ------------------------ submission end ------------------------    
  localhost_print_function(' ------------- 100-admin start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-admin end ------------- ')
  return render_template('polling/admin_templates/dashboard/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_admin.route('/admin/hosts', methods=['GET', 'POST'])
@polling_views_admin.route('/admin/hosts/', methods=['GET', 'POST'])
@polling_views_admin.route('/admin/hosts/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def admin_hosts_function(url_redirect_code=None):
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
    # ------------------------ send emails function start ------------------------
    try:
      ui_send_emails = request.form.get('ui_send_emails')
      if ui_send_emails == 'on':
        pass
    except:
      pass
    # ------------------------ send emails function end ------------------------
    # ------------------------ add host email start ------------------------
    try:
      # ------------------------ get ui start ------------------------
      ui_host_podcast_name = request.form.get('ui_host_podcast_name')
      ui_host_podcast_email = request.form.get('ui_host_podcast_email')
      ui_host_podcast_greeting = request.form.get('ui_host_podcast_greeting')
      # ------------------------ get ui end ------------------------
      # ------------------------ sanitize inputs start ------------------------
      sanitize_email_function_check = sanitize_email_function(ui_host_podcast_email)
      if sanitize_email_function_check == False:
        return redirect(url_for('polling_views_admin.admin_hosts_function', url_redirect_code='e6'))
      # ------------------------ sanitize inputs end ------------------------
      # ------------------------ check if exists start ------------------------
      db_obj = HostMarketingObj.query.filter_by(host_email=ui_host_podcast_email).first()
      if db_obj == None or db_obj == []:
        # ------------------------ add to db start ------------------------
        try:
          new_row = HostMarketingObj(
            id = create_uuid_function('host_'),
            created_timestamp = create_timestamp_function(),
            podcast_name = ui_host_podcast_name,
            host_email = ui_host_podcast_email,
            greeting_name = ui_host_podcast_greeting,
            unsubscribed = False
          )
          db.session.add(new_row)
          db.session.commit()
          return redirect(url_for('polling_views_admin.admin_hosts_function', url_redirect_code='s10'))
        except:
          pass
        # ------------------------ add to db end ------------------------
      # ------------------------ check if exists end ------------------------
    except:
      pass
    # ------------------------ add host email end ------------------------
  localhost_print_function(' ------------- 100-admin start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-admin end ------------- ')
  return render_template('polling/admin_templates/hosts/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------
