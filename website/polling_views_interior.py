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
from website.backend.candidates.browser import browser_response_set_cookie_function_v6
from website.models import UserObj, EmailSentObj, UserAttributesObj, ShowsFollowingObj, ShowsObj, PollsObj, PollsAnsweredObj, ShowsQueueObj, RedditPostsRequestedObj
from website.backend.onboarding import onboarding_checks_v2_function
from website.backend.login_checks import product_login_checks_function
from website.backend.candidates.string_manipulation import breakup_email_function
import os
import json
from website.backend.candidates.send_emails import send_email_template_function
from website.backend.candidates.lists import get_month_days_years_function, get_marketing_list_v2_function
from website.backend.dates import get_years_from_date_function, return_ints_from_str_function
from website.backend.get_create_obj import get_all_shows_following_function, get_all_platforms_function, get_platform_based_on_name_function, get_show_based_on_name_function, get_show_based_on_id_and_platform_id_function, check_if_currently_following_show_function, get_show_based_on_id_function, get_poll_based_on_id_function, get_show_percent_of_all_polls_answered_function, get_all_polls_based_on_show_id_function, check_at_least_one_poll_answer_submitted_function, get_total_polls_created_today_by_user_for_one_show_function, get_age_demographics_function
from website.backend.spotify import spotify_search_show_function
from website.backend.user_inputs import sanitize_letters_numbers_spaces_specials_only_function, sanitize_text_v1_function, sanitize_text_v2_function
from website.backend.dict_manipulation import arr_of_dict_all_columns_single_item_function, prep_poll_dict_function
from website.backend.show_utils import shows_following_arr_of_dict_function, follow_user_polls_show_function, follow_show_function
from website.backend.sql_statements.select import select_general_function
from website.backend.poll_statistics_v2 import get_poll_statistics_v2_function, get_create_show_chart_colors_function
from website.backend.reddit_statistics import get_reddit_statistics_function
from datetime import datetime
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
polling_views_interior = Blueprint('polling_views_interior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/dashboard', methods=['GET', 'POST'])
@polling_views_interior.route('/dashboard/', methods=['GET', 'POST'])
@polling_views_interior.route('/dashboard/<url_show_id>', methods=['GET', 'POST'])
@polling_views_interior.route('/dashboard/<url_show_id>/', methods=['GET', 'POST'])
@polling_views_interior.route('/dashboard/<url_show_id>/<url_redirect_code>', methods=['GET', 'POST'])
@polling_views_interior.route('/dashboard/<url_show_id>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def polling_dashboard_function(url_redirect_code=None, url_show_id=None):
  # ------------------------ product login check start ------------------------
  is_match = product_login_checks_function(current_user,'polling')
  if is_match == False:
    logout_user()
    localhost_print_function('user logged out and redirecting to login product - polling')
    return redirect(url_for('polling_auth.polling_login_function'))
  # ------------------------ product login check end ------------------------
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
  # ------------------------ onboarding checks start ------------------------
  onbaording_status = onboarding_checks_v2_function(current_user)
  if onbaording_status == 'verify':
    page_dict['verified_email_status'] = False
  if onbaording_status == 'attribute_marketing':
    return redirect(url_for('polling_views_interior.polling_feedback_function', url_feedback_code=onbaording_status))
  # ------------------------ onboarding checks end ------------------------
  # ------------------------ navbar variable start ------------------------
  page_dict['current_user_email'] = current_user.email
  # ------------------------ navbar variable end ------------------------
  # ------------------------ get all shows following sorted start ------------------------
  page_dict['shows_following_arr_of_dict'] = get_all_shows_following_function(current_user)
  page_dict = shows_following_arr_of_dict_function(page_dict)
  # ------------------------ get all shows following sorted end ------------------------
  # ------------------------ dashboard default start ------------------------
  # ------------------------ variables start ------------------------
  page_dict['url_show_id'] = url_show_id
  # ------------------------ variables end ------------------------
  if url_show_id == None:
    # ------------------------ ensure user is part of the user polls show start ------------------------
    if page_dict['shows_following_arr_of_dict'] != None:
      update_made = follow_user_polls_show_function(current_user)
      if update_made == True:
        return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # ------------------------ ensure user is part of the user polls show end ------------------------
    # ------------------------ pull + calculate status bar percent complete start ------------------------
    try:
      show_counter = 0
      for i_dict in page_dict['shows_following_arr_of_dict']:
        i_dict['percent_total_polls_complete'], i_dict['user_completed_all_polls'] = get_show_percent_of_all_polls_answered_function(current_user.id, i_dict['id'])
        show_counter += 1
        i_dict['show_count'] = show_counter
    except:
      pass
    # ------------------------ pull + calculate status bar percent complete end ------------------------
  # ------------------------ dashboard default end ------------------------
  # ------------------------ dashboard show polls start ------------------------
  if url_show_id != None:
    # ------------------------ ensure show id exists start ------------------------
    db_show_obj = get_show_based_on_id_function(url_show_id)
    if db_show_obj == None:
      return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e6'))
    page_dict['db_show_dict'] = arr_of_dict_all_columns_single_item_function(db_show_obj)
    title_limit = 15
    if len(page_dict['db_show_dict']['name']) > title_limit:
      page_dict['db_show_dict']['name_title'] = page_dict['db_show_dict']['name'][0:title_limit] + '...'
    else:
      page_dict['db_show_dict']['name_title'] = page_dict['db_show_dict']['name']
    # ------------------------ ensure show id exists end ------------------------
    # ------------------------ ensure user is following the show start ------------------------
    new_following_updated = follow_show_function(current_user, url_show_id)
    if new_following_updated == True:
      return redirect(url_for('polling_views_interior.polling_dashboard_function', url_show_id=url_show_id))
    # ------------------------ ensure user is following the show end ------------------------
    # ------------------------ pull all polls for show id start ------------------------
    page_dict['all_polls_for_show_arr_of_dict'] = []
    db_objs = get_all_polls_based_on_show_id_function(page_dict['url_show_id'])
    for i_obj in db_objs:
      i_dict = arr_of_dict_all_columns_single_item_function(i_obj)
      page_dict['all_polls_for_show_arr_of_dict'].append(i_dict)
    # ------------------------ pull all polls for show id end ------------------------
    # ------------------------ pull answered status for all polls start ------------------------
    for i_dict in page_dict['all_polls_for_show_arr_of_dict']:
      i_dict['user_answered_poll_at_least_once'] = check_at_least_one_poll_answer_submitted_function(current_user, i_dict['id'])
    # ------------------------ pull answered status for all polls end ------------------------
  # ------------------------ dashboard show polls end ------------------------
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'polling/interior/dashboard/index.html'
  # ------------------------ for setting cookie end ------------------------
  localhost_print_function(' ------------- 100-dashboard start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-dashboard end ------------- ')
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user=current_user, page_dict_to_html=page_dict)
  else:
    browser_response = browser_response_set_cookie_function_v6(current_user, template_location_url, page_dict)
    return browser_response
  # ------------------------ auto set cookie end ------------------------
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/verify/success/<url_verification_code>')
@polling_views_interior.route('/verify/success/<url_verification_code>/<url_redirect_code>')
@polling_views_interior.route('/verify/success/<url_verification_code>/<url_redirect_code>/')
# @login_required
def verification_code_clicked_function(url_redirect_code=None, url_verification_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ verification start ------------------------
  if url_verification_code == None:
    return redirect(url_for('polling_views_interior.polling_dashboard_function'))
  redis_uuid_value = ''
  try:
    redis_uuid_value = redis_connection.get(url_verification_code).decode('utf-8')
  except:
    return redirect(url_for('polling_views_interior.verify_email_function', url_redirect_code='e28'))
  db_user_obj = UserObj.query.filter_by(id=redis_uuid_value).first()
  db_user_obj.verified_email = True
  db.session.commit()
  redis_connection.delete(url_verification_code)
  # ------------------------ verification end ------------------------
  return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='s9'))
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/verify', methods=['GET', 'POST'])
@polling_views_interior.route('/verify/<url_redirect_code>', methods=['GET', 'POST'])
@polling_views_interior.route('/verify/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def verify_email_function(url_redirect_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ redirect check start ------------------------
  if current_user.verified_email == True:
    return redirect(url_for('polling_views_interior.polling_dashboard_function'))
  # ------------------------ redirect check end ------------------------
  page_dict['user_email'] = current_user.email
  page_dict['feedback_step'] = '0'
  output_subject = f'Verify Polling Email: {current_user.email}'
  # ------------------------ check if verify email already sent start ------------------------
  db_email_obj = EmailSentObj.query.filter_by(to_email=current_user.email,subject=output_subject).first()
  # ------------------------ check if verify email already sent end ------------------------
  if db_email_obj == None or db_email_obj == []:
    # ------------------------ verification code store in redis start ------------------------
    verification_code = create_uuid_function('verify_')
    redis_connection.set(verification_code, current_user.id.encode('utf-8'))
    # ------------------------ verification code store in redis end ------------------------
    # ------------------------ auto send first email to user start ------------------------
    guessed_name = breakup_email_function(current_user.email)
    try:
      output_to_email = current_user.email
      output_body = ''
      # ------------------------ get environment start ------------------------
      server_env = os.environ.get('TESTING', 'false')
      # ------------------------ get environment end ------------------------
      # ------------------------ localhost start ------------------------
      if server_env == 'true':
        output_body = f"<p>Hi {guessed_name},</p>\
                        <p>Please click the link below to verify your email address.</p>\
                        <p>Verify email link: http://127.0.0.1:80/verify/success/{verification_code}</p>\
                        <p style='margin:0;'>Best,</p>\
                        <p style='margin:0;'>HerdReviews Support Team</p>"
      # ------------------------ localhost end ------------------------
      # ------------------------ production start ------------------------
      else:
        output_body = f"<p>Hi {guessed_name},</p>\
                        <p>Please click the link below to verify your email address.</p>\
                        <p>Verify email link: https://herdreviews.com/verify/success/{verification_code}</p>\
                        <p style='margin:0;'>Best,</p>\
                        <p style='margin:0;'>HerdReviews Support Team</p>"
      # ------------------------ production end ------------------------
      send_email_template_function(output_to_email, output_subject, output_body)
    except:
      pass
    # ------------------------ auto send first email to user end ------------------------
    # ------------------------ insert email to db start ------------------------
    try:
      new_row_email = EmailSentObj(
        id = create_uuid_function('email_'),
        created_timestamp = create_timestamp_function(),
        from_user_id_fk = current_user.id,
        to_email = output_to_email,
        subject = output_subject,
        body = output_body
      )
      db.session.add(new_row_email)
      db.session.commit()
    except:
      pass
    # ------------------------ insert email to db end ------------------------
  # ------------------------ resend email start ------------------------
  if request.method == 'POST':
    # ------------------------ redirect check start ------------------------
    if current_user.verified_email == True:
      return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # ------------------------ redirect check end ------------------------
    # ------------------------ delete all existing redis keys for this uuid start ------------------------
    redis_keys = redis_connection.keys()
    for i_key in redis_keys:    
      if 'verify' in str(i_key):
        redis_value = redis_connection.get(i_key).decode('utf-8')
        if redis_value == current_user.id:
          redis_connection.delete(i_key)
    # ------------------------ delete all existing redis keys for this uuid end ------------------------
    # ------------------------ create new verification key start ------------------------
    new_verification_code = create_uuid_function('verify_')
    redis_connection.set(new_verification_code, current_user.id.encode('utf-8'))
    # ------------------------ create new verification key end ------------------------
    # ------------------------ send email start ------------------------
    guessed_name = breakup_email_function(current_user.email)
    try:
      output_to_email = current_user.email
      output_body = ''
      # ------------------------ get environment start ------------------------
      server_env = os.environ.get('TESTING', 'false')
      # ------------------------ get environment end ------------------------
      # ------------------------ localhost start ------------------------
      if server_env == 'true':
        output_body = f"<p>Hi {guessed_name},</p>\
                      <p>Please click the link below to verify your email address.</p>\
                      <p>Verify email link: http://127.0.0.1:80/verify/success/{new_verification_code}</p>\
                      <p style='margin:0;'>Best,</p>\
                      <p style='margin:0;'>HerdReviews Support Team</p>"
      # ------------------------ localhost end ------------------------
      # ------------------------ production start ------------------------
      else:
        output_body = f"<p>Hi {guessed_name},</p>\
                        <p>Please click the link below to verify your email address.</p>\
                        <p>Verify email link: https://herdreviews.com/verify/success/{new_verification_code}</p>\
                        <p style='margin:0;'>Best,</p>\
                        <p style='margin:0;'>HerdReviews Support Team</p>"
      # ------------------------ production end ------------------------
      send_email_template_function(output_to_email, output_subject, output_body)
      # ------------------------ insert email to db start ------------------------
      try:
        new_row_email = EmailSentObj(
          id = create_uuid_function('email_'),
          created_timestamp = create_timestamp_function(),
          from_user_id_fk = current_user.id,
          to_email = output_to_email,
          subject = output_subject,
          body = output_body
        )
        db.session.add(new_row_email)
        db.session.commit()
      except:
        pass
      # ------------------------ insert email to db end ------------------------
    except:
      pass
    # ------------------------ send email end ------------------------
    return redirect(url_for('polling_views_interior.verify_email_function', url_redirect_code='s8'))
  # ------------------------ resend email end ------------------------
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'polling/interior/verify_email/index.html'
  # ------------------------ for setting cookie end ------------------------
  # ------------------------ auto set cookie start ------------------------
  get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
  if get_cookie_value_from_browser != None:
    redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
    return render_template(template_location_url, user=current_user, page_dict_to_html=page_dict)
  else:
    browser_response = browser_response_set_cookie_function_v6(current_user, template_location_url, page_dict)
    return browser_response
  # ------------------------ auto set cookie end ------------------------
  # return render_template('polling/interior/verify_email/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/feedback/<url_feedback_code>', methods=['GET', 'POST'])
@polling_views_interior.route('/feedback/<url_feedback_code>/', methods=['GET', 'POST'])
@polling_views_interior.route('/feedback/<url_feedback_code>/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def polling_feedback_function(url_redirect_code=None, url_feedback_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ double check redirect start ------------------------
  if url_feedback_code != 'attribute_marketing' and url_feedback_code != 'attribute_birthday':
    return redirect(url_for('polling_views_interior.polling_dashboard_function'))
  db_user_attribute_obj = UserAttributesObj.query.filter_by(attribute_code=url_feedback_code,fk_user_id=current_user.id).first()
  if db_user_attribute_obj != None:
    return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='s20'))
  # ------------------------ double check redirect end ------------------------
  # ------------------------ set loading bar variables start ------------------------
  if url_feedback_code == 'attribute_tos':
    page_dict['feedback_step'] = '1'
    page_dict['feedback_request'] = url_feedback_code
  if url_feedback_code == 'attribute_birthday':
    page_dict['feedback_step'] = '2'
    page_dict['feedback_request'] = url_feedback_code
  if url_feedback_code == 'attribute_marketing':
    page_dict['feedback_step'] = '3'
    page_dict['feedback_request'] = url_feedback_code
  # ------------------------ set loading bar variables end ------------------------
  # ------------------------ more specific variables init start ------------------------
  months_arr = []
  days_arr = []
  years_arr = []
  month_day_dict = {}
  marketing_list = None
  marketing_list_index = None
  # ------------------------ more specific variables init end ------------------------
  # ------------------------ more specific variables for birthday start ------------------------
  if url_feedback_code == 'attribute_birthday':
    # ------------------------ get month days dict start ------------------------
    months_arr, days_arr, years_arr, month_day_dict = get_month_days_years_function()
    page_dict['months_arr'] = months_arr
    page_dict['days_arr'] = days_arr
    page_dict['years_arr'] = years_arr
    # ------------------------ get month days dict end ------------------------
  # ------------------------ more specific variables for birthday end ------------------------
  # ------------------------ more specific variables for marketing start ------------------------
  if url_feedback_code == 'attribute_marketing':
    # ------------------------ get current activities start ------------------------
    marketing_list, marketing_list_index = get_marketing_list_v2_function()
    page_dict['marketing_list'] = marketing_list
    page_dict['marketing_list_index'] = marketing_list_index
    # ------------------------ get current activities end ------------------------
  # ------------------------ more specific variables for marketing end ------------------------
  # ------------------------ submission start ------------------------
  if request.method == 'POST':
    # ------------------------ double check redirect start ------------------------
    if url_feedback_code == 'attribute_tos':
      onbaording_status = onboarding_checks_v2_function(current_user)
      if onbaording_status != url_feedback_code:
        return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # ------------------------ double check redirect end ------------------------
    # ------------------------ double check redirect start ------------------------
    db_user_attribute_obj = UserAttributesObj.query.filter_by(attribute_code=url_feedback_code,fk_user_id=current_user.id).first()
    if db_user_attribute_obj != None:
      return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # ------------------------ double check redirect end ------------------------
    # ------------------------ post feedback tos start ------------------------
    if url_feedback_code == 'attribute_tos':
      # ------------------------ insert to db start ------------------------
      new_row = UserAttributesObj(
        id=create_uuid_function('attribute_'),
        created_timestamp=create_timestamp_function(),
        fk_user_id=current_user.id,
        product='polling',
        attribute_code=url_feedback_code,
        attribute_response = 'Complete'
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ insert to db end ------------------------
      return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # ------------------------ post feedback tos end ------------------------
    # ------------------------ post feedback birthday start ------------------------
    if url_feedback_code == 'attribute_birthday':
      # ------------------------ get user inputs start ------------------------
      ui_birthday = request.form.get('ui_birthday')
      # ------------------------ get user inputs end ------------------------
      # ------------------------ sanatize inputs start ------------------------
      ui_year, ui_month, ui_day = return_ints_from_str_function(ui_birthday)
      if ui_year == False or ui_month == False or ui_day == False:
        return redirect(url_for('polling_views_interior.polling_feedback_function', url_redirect_code='e6'))
      # ------------------------ sanatize inputs end ------------------------
      # ------------------------ sanatize inputs start ------------------------
      try:
        # birth month
        if int(ui_month) not in months_arr:
          return redirect(url_for('polling_views_interior.polling_feedback_function', url_redirect_code='e20', url_feedback_code=url_feedback_code))
      except:
        pass
      try:
        # birth day
        allowed_days_arr = month_day_dict[str(ui_month)]
        if int(ui_day) not in allowed_days_arr:
          return redirect(url_for('polling_views_interior.polling_feedback_function', url_redirect_code='e21', url_feedback_code=url_feedback_code))
      except:
        pass
      try:
        # birth year
        if int(ui_year) not in years_arr:
          return redirect(url_for('polling_views_interior.polling_feedback_function', url_redirect_code='e26', url_feedback_code=url_feedback_code))
      except:
        pass
      # ------------------------ sanatize inputs end ------------------------
      # ------------------------ age check start ------------------------
      current_age = get_years_from_date_function(ui_year, ui_month, ui_day)
      # if float(current_age) < float(18.0):
      #   return redirect(url_for('polling_views_interior.polling_feedback_function', url_redirect_code='e30', url_feedback_code=url_feedback_code))
      # ------------------------ age check end ------------------------
      # ------------------------ insert to db start ------------------------
      new_row = UserAttributesObj(
        id=create_uuid_function('attribute_'),
        created_timestamp=create_timestamp_function(),
        fk_user_id=current_user.id,
        product='polling',
        attribute_code=url_feedback_code,
        attribute_year=ui_year,
        attribute_month=ui_month,
        attribute_day=ui_day
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ insert to db end ------------------------
      # ------------------------ insert to db poll start ------------------------
      year_generation_dict, generation_options_arr = get_age_demographics_function()
      users_generation = year_generation_dict[str(ui_year)]
      new_row = PollsAnsweredObj(
        id=create_uuid_function('vote_'),
        created_timestamp=create_timestamp_function(),
        fk_show_id='show_user_attributes',
        fk_poll_id='poll_user_attribute_generation',
        fk_user_id=current_user.id,
        poll_answer_submitted=users_generation,
        written_answer_submitted=None,
        status_answer_anonymous=False,
        poll_vote_updown_question=True,
        poll_vote_updown_feedback=True
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ insert to db poll end ------------------------
      return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # ------------------------ post feedback birthday end ------------------------
    # ------------------------ post feedback marketing start ------------------------
    if url_feedback_code == 'attribute_marketing':
      ui_answer = request.form.get('ui_general_selection_radio')
      # ------------------------ invalid start ------------------------
      if ui_answer not in marketing_list:
        return redirect(url_for('polling_views_interior.polling_feedback_function', url_feedback_code=url_feedback_code, url_redirect_code='e6'))
      # ------------------------ invalid end ------------------------
      # ------------------------ insert to db start ------------------------
      new_row = UserAttributesObj(
        id=create_uuid_function('attribute_'),
        created_timestamp=create_timestamp_function(),
        fk_user_id=current_user.id,
        product='polling',
        attribute_code=url_feedback_code,
        attribute_response=ui_answer
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ insert to db end ------------------------
      return redirect(url_for('polling_views_interior.polling_dashboard_function'))
    # ------------------------ post feedback marketing end ------------------------
  # ------------------------ submission end ------------------------
  # ------------------------ set cookie on first feedback step start ------------------------
  if url_feedback_code == 'attribute_tos':
    # ------------------------ for setting cookie start ------------------------
    template_location_url = 'polling/interior/feedback/index.html'
    # ------------------------ for setting cookie end ------------------------
    # ------------------------ auto set cookie start ------------------------
    get_cookie_value_from_browser = redis_check_if_cookie_exists_function()
    if get_cookie_value_from_browser != None:
      redis_connection.set(get_cookie_value_from_browser, current_user.id.encode('utf-8'))
      return render_template(template_location_url, user=current_user, page_dict_to_html=page_dict)
    else:
      browser_response = browser_response_set_cookie_function_v6(current_user, template_location_url, page_dict)
      return browser_response
    # ------------------------ auto set cookie end ------------------------
  # ------------------------ set cookie on first feedback step end ------------------------
  else:
    return render_template('polling/interior/feedback/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/loading/<url_platform_reference_id>')
@login_required
def polling_loading_function(url_platform_reference_id=None):
  # ------------------------ check url start ------------------------
  if url_platform_reference_id == None:
    return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e6'))
  # ------------------------ check url end ------------------------
  # ------------------------ check if exists start ------------------------
  db_show_check_obj = ShowsObj.query.filter_by(platform_reference_id=url_platform_reference_id).first()
  if db_show_check_obj != None:
    db_show_following_obj = ShowsFollowingObj.query.filter_by(fk_show_id=db_show_check_obj.id,fk_user_id=current_user.id).first()
    if db_show_following_obj == None:
      # ------------------------ insert to db start ------------------------
      new_row = ShowsFollowingObj(
        id=create_uuid_function('following_'),
        created_timestamp=create_timestamp_function(),
        fk_platform_id = db_show_check_obj.fk_platform_id,
        fk_show_id = db_show_check_obj.id,
        fk_user_id = current_user.id
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ insert to db end ------------------------
      return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=db_show_check_obj.id, url_redirect_code='s16'))
  # ------------------------ check if exists end ------------------------
  return render_template('polling/interior/loading_screen/index.html')
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/show/add', methods=['GET', 'POST'])
@polling_views_interior.route('/show/add/', methods=['GET', 'POST'])
@polling_views_interior.route('/show/add/<url_step_code>', methods=['GET', 'POST'])
@polling_views_interior.route('/show/add/<url_step_code>/', methods=['GET', 'POST'])
@polling_views_interior.route('/show/add/<url_step_code>/<url_platform_id>', methods=['GET', 'POST'])
@polling_views_interior.route('/show/add/<url_step_code>/<url_platform_id>/', methods=['GET', 'POST'])
@polling_views_interior.route('/show/add/<url_step_code>/<url_platform_id>/<url_redis_key>', methods=['GET', 'POST'])
@polling_views_interior.route('/show/add/<url_step_code>/<url_platform_id>/<url_redis_key>/', methods=['GET', 'POST'])
@polling_views_interior.route('/show/add/<url_step_code>/<url_platform_id>/<url_redis_key>/<url_redirect_code>', methods=['GET', 'POST'])
@polling_views_interior.route('/show/add/<url_step_code>/<url_platform_id>/<url_redis_key>/<url_redirect_code>/', methods=['GET', 'POST'])
# @login_required
def polling_add_show_function(url_redirect_code=None, url_step_code='1', url_platform_id=None, url_redis_key=None):
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
  # ------------------------ get search value from landing url start ------------------------
  pulled_search_value = None
  try:
    pulled_search_value = request.args.get('searchvalue')
  except:
    pass
  page_dict['url_searched_value'] = pulled_search_value
  # ------------------------ get search value from landing url end ------------------------
  # ------------------------ remove from redis check start ------------------------
  try:
    wip_key = request.args.get('wip_key')
    if wip_key != None and wip_key != '':
      redis_connection.delete(wip_key)
  except:
    pass
  # ------------------------ remove from redis check end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['shows_arr_of_dicts'] = []
  page_dict['url_step_code'] = url_step_code
  page_dict['url_platform_id'] = url_platform_id
  page_dict['url_redis_key'] = url_redis_key
  page_dict['url_next_step_code'] = str(int(url_step_code) + 1)
  page_dict['url_previous_step_code'] = str(int(url_step_code) - 1)
  page_dict['platforms_arr'] = []
  page_dict['url_step_title'] = ''
  page_dict['url_back_str'] = ''
  page_dict['shows_following_arr_of_dict'] = None
  page_dict['spotify_pulled_arr_of_dict'] = None
  spotify_pulled_arr_of_dict = []
  # ------------------------ set variables end ------------------------
  page_dict['current_user_is_anonymous'] = False
  if current_user.is_anonymous == True:
    page_dict['current_user_is_anonymous'] = True
  # ------------------------ redirect steps check start ------------------------
  if url_step_code == '1':
    return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code='2',url_platform_id='podcast', searchvalue=pulled_search_value))
  if url_step_code == '2' and (url_platform_id == None or url_redis_key != None):
    return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=page_dict['url_previous_step_code'], url_redirect_code='e6', searchvalue=pulled_search_value))
  if url_step_code == '3' and (url_platform_id == None or url_redis_key == None):
    return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=page_dict['url_previous_step_code'], url_platform_id=url_platform_id, url_redirect_code='e6', searchvalue=pulled_search_value))
  # ------------------------ redirect steps check end ------------------------
  # ------------------------ set back button string start ------------------------
  if url_step_code == '2':
    page_dict['url_back_str'] = f"/dashboard"
  elif url_step_code == '3':
    page_dict['url_back_str'] = f"/show/add/{page_dict['url_previous_step_code']}/{url_platform_id}?wip_key={url_redis_key}"
  # ------------------------ set back button string end ------------------------
  # ------------------------ get all sources following start ------------------------
  if current_user.is_anonymous == True:
    pass
  else:
    page_dict['shows_following_arr_of_dict'] = get_all_shows_following_function(current_user)
  # ------------------------ get all sources following end ------------------------
  # ------------------------ set title start ------------------------
  page_dict['url_step_subtitle'] = "Audience Polling Platform"
  if page_dict['url_step_code'] == '1':
    page_dict['url_step_title'] = 'Platform selection'
  if page_dict['url_step_code'] == '2':
    page_dict['url_step_title'] = 'Search podcast'
  if page_dict['url_step_code'] == '3':
    page_dict['url_step_title'] = 'Confirm show'
  # ------------------------ set title end ------------------------
  # ------------------------ get platforms start ------------------------
  if page_dict['url_step_code'] == '1':
    all_platforms_obj = get_all_platforms_function()
    for i_obj in all_platforms_obj:
      page_dict['platforms_arr'].append(i_obj.name)
  # ------------------------ get platforms end ------------------------
  # ------------------------ pull from redis if exists start ------------------------
  if page_dict['url_step_code'] == '3':
    try:
      redis_pulled_value = redis_connection.get(url_redis_key).decode('utf-8')
      spotify_pulled_arr_of_dict = json.loads(redis_pulled_value)
      page_dict['spotify_pulled_arr_of_dict'] = spotify_pulled_arr_of_dict
    except:
      pass
  # ------------------------ pull from redis if exists end ------------------------
  # ------------------------ get all podcasts start ------------------------
  if url_step_code == '2':
    show_arr_of_dict = select_general_function('select_query_general_8')
    for i in show_arr_of_dict:
      page_dict['shows_arr_of_dicts'].append(i)
  # ------------------------ get all podcasts end ------------------------
  if request.method == 'POST' or (current_user.is_anonymous == True and page_dict['url_searched_value'] != None):
    if page_dict['url_step_code'] == '1':
      # ------------------------ get user inputs start ------------------------
      ui_platform_selection = request.form.get('ui_general_selection_radio')
      # ------------------------ get user inputs end ------------------------
      # ------------------------ sanitize ui start ------------------------
      if ui_platform_selection not in page_dict['platforms_arr']:
        return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=url_step_code, url_redirect_code='e6'))
      if ui_platform_selection != 'Podcast':
        return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=url_step_code, url_redirect_code='e33'))
      # ------------------------ sanitize ui end ------------------------
      # ------------------------ get id based on user inputs start ------------------------
      db_obj = get_platform_based_on_name_function(ui_platform_selection)
      return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=page_dict['url_next_step_code'], url_platform_id=db_obj.id))
      # ------------------------ get id based on user inputs end ------------------------
    if page_dict['url_step_code'] == '2':
      # ------------------------ get user inputs start ------------------------
      ui_search_show_name = None
      if current_user.is_anonymous == True:
        ui_search_show_name = page_dict['url_searched_value']
        if ui_search_show_name == None or ui_search_show_name == '':
          ui_search_show_name = request.form.get('ui_search_show_name')
      else:
        ui_search_show_name = request.form.get('ui_search_show_name')
      # ------------------------ get user inputs end ------------------------
      # ------------------------ sanitize ui start ------------------------
      ui_search_show_name_check = sanitize_letters_numbers_spaces_specials_only_function(ui_search_show_name)
      if ui_search_show_name_check == False:
        return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=url_step_code, url_platform_id=url_platform_id, url_redirect_code='e6'))
      # ------------------------ sanitize ui end ------------------------
      # ------------------------ search spotify start ------------------------
      spotify_pulled_arr_of_dict = spotify_search_show_function(ui_search_show_name)
      if spotify_pulled_arr_of_dict == None:
        return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=url_step_code, url_platform_id=url_platform_id, url_redirect_code='e32'))
      # ------------------------ search spotify end ------------------------
      # ------------------------ add spotify result to redis start ------------------------
      url_redis_key = create_uuid_function('spotify_temp_')
      redis_connection.set(url_redis_key, json.dumps(spotify_pulled_arr_of_dict).encode('utf-8'))
      # ------------------------ add spotify result to redis end ------------------------
      return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=page_dict['url_next_step_code'], url_platform_id=url_platform_id, url_redis_key=url_redis_key))
    if page_dict['url_step_code'] == '3':
      # ------------------------ remove from redis start ------------------------
      try:
        redis_connection.delete(url_redis_key)
      except:
        pass
      # ------------------------ remove from redis end ------------------------
      # ------------------------ user inputs start ------------------------
      ui_show_selected_index_value = request.form.get('flexRadioAllShowSelection')
      # ------------------------ user inputs end ------------------------
      # ------------------------ catch error start ------------------------
      try:
        if ui_show_selected_index_value == None or int(ui_show_selected_index_value) < 0 or int(ui_show_selected_index_value) > 4:
          return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=url_step_code, url_platform_id=url_platform_id, url_redirect_code='e6'))
      except:
        return redirect(url_for('polling_views_interior.polling_add_show_function', url_step_code=url_step_code, url_platform_id=url_platform_id, url_redirect_code='e6'))
      # ------------------------ catch error end ------------------------
      # ------------------------ check if show already in db start ------------------------
      show_already_exists_check = get_show_based_on_name_function(url_platform_id, page_dict['spotify_pulled_arr_of_dict'][int(ui_show_selected_index_value)]['name'])
      if show_already_exists_check != None:
        return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=show_already_exists_check.id))
      # ------------------------ check if show already in db end ------------------------
      if show_already_exists_check == None:
        # ------------------------ check if already in queue start ------------------------
        db_queue_obj = ShowsQueueObj.query.filter_by(name=page_dict['spotify_pulled_arr_of_dict'][int(ui_show_selected_index_value)]['name']).first()
        # ------------------------ check if already in queue end ------------------------
        if db_queue_obj == None:
          # ------------------------ add to live job queue start ------------------------
          new_row = ShowsQueueObj(
            id=create_uuid_function('queue_'),
            created_timestamp=create_timestamp_function(),
            fk_platform_id = url_platform_id,
            platform_reference_id = page_dict['spotify_pulled_arr_of_dict'][int(ui_show_selected_index_value)]['id'],
            name=page_dict['spotify_pulled_arr_of_dict'][int(ui_show_selected_index_value)]['name'],
            description=page_dict['spotify_pulled_arr_of_dict'][int(ui_show_selected_index_value)]['description'],
            img_large=page_dict['spotify_pulled_arr_of_dict'][int(ui_show_selected_index_value)]['img_large'],
            img_medium=page_dict['spotify_pulled_arr_of_dict'][int(ui_show_selected_index_value)]['img_medium'],
            img_small=page_dict['spotify_pulled_arr_of_dict'][int(ui_show_selected_index_value)]['img_small'],
            show_url=page_dict['spotify_pulled_arr_of_dict'][int(ui_show_selected_index_value)]['show_url'],
            fk_show_id=create_uuid_function('show_')
          )
          db.session.add(new_row)
          db.session.commit()
          # ------------------------ add to live job queue end ------------------------
          # ------------------------ email self start ------------------------
          if current_user.is_anonymous == True or current_user.email != os.environ.get('RUN_TEST_EMAIL'):
            try:
              output_to_email = os.environ.get('HR_SUPPORT_EMAIL')
              output_subject = f"New show added to queue: '{page_dict['spotify_pulled_arr_of_dict'][int(ui_show_selected_index_value)]['name']}'"
              output_body = f"<p>New show added to queue: '{page_dict['spotify_pulled_arr_of_dict'][int(ui_show_selected_index_value)]['name']}'</p>"
              send_email_template_function(output_to_email, output_subject, output_body)
            except:
              pass
          # ------------------------ email self end ------------------------
        return redirect(url_for('polling_views_interior.polling_loading_function', url_platform_reference_id=page_dict['spotify_pulled_arr_of_dict'][int(ui_show_selected_index_value)]['id']))
  localhost_print_function(' ------------- 100-show selection start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-show selection end ------------- ')
  return render_template('polling/interior/show_select/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/show/follow/<url_platform_id>/<url_show_id>', methods=['GET', 'POST'])
@polling_views_interior.route('/show/follow/<url_platform_id>/<url_show_id>/', methods=['GET', 'POST'])
@login_required
def polling_follow_show_function(url_platform_id=None, url_show_id=None):
  # ------------------------ check inputs start ------------------------
  if url_platform_id == None or url_show_id == None:
    return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e6'))
  # ------------------------ check inputs end ------------------------
  # ------------------------ sanitize inputs start ------------------------
  db_obj = get_show_based_on_id_and_platform_id_function(url_show_id, url_platform_id)
  if db_obj == None:
    return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e6'))
  # ------------------------ sanitize inputs end ------------------------
  # ------------------------ check if already following start ------------------------
  db_obj = check_if_currently_following_show_function(current_user, url_show_id, url_platform_id)
  if db_obj != None:
    return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_redirect_code='s16'))
  # ------------------------ check if already following end ------------------------
  # ------------------------ redirect to dashboard start ------------------------
  return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_redirect_code='s16'))
  # ------------------------ redirect to dashboard end ------------------------
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/show/<url_show_id>', methods=['GET', 'POST'])
@polling_views_interior.route('/show/<url_show_id>/', methods=['GET', 'POST'])
@polling_views_interior.route('/show/<url_show_id>/<url_poll_id>', methods=['GET', 'POST'])
@polling_views_interior.route('/show/<url_show_id>/<url_poll_id>/', methods=['GET', 'POST'])
@polling_views_interior.route('/show/<url_show_id>/<url_poll_id>/<url_redirect_code>', methods=['GET', 'POST'])
@polling_views_interior.route('/show/<url_show_id>/<url_poll_id>/<url_redirect_code>/', methods=['GET', 'POST'])
# @login_required
def polling_show_function(url_redirect_code=None, url_show_id=None, url_poll_id=None):
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
  # ------------------------ try for url value start ------------------------
  url_anonymous_code = None
  try:
    url_anonymous_code = request.args.get('url_anonymous_code')
  except:
    pass
  # ------------------------ try for url value end ------------------------
  if current_user.is_anonymous == True and url_show_id == 'show_user_attributes':
    return redirect(url_for('polling_auth.polling_signup_function'))
  # ------------------------ if somebody tries to change their generation start ------------------------
  if url_show_id == 'show_user_attributes' and url_poll_id=='poll_user_attribute_generation':
    return redirect(url_for('polling_views_interior.polling_feedback_function', url_feedback_code='attribute_birthday'))
  # ------------------------ if somebody tries to change their generation end ------------------------
  # ------------------------ pull show info start ------------------------
  # Get show based on id from shows table
  db_show_obj = get_show_based_on_id_function(url_show_id)
  # ------------------------ check if show exists in db start ------------------------
  if db_show_obj == None:
    return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e6'))
  # ------------------------ check if show exists in db end ------------------------
  page_dict['db_show_dict'] = arr_of_dict_all_columns_single_item_function(db_show_obj)
  title_limit = 15
  if len(page_dict['db_show_dict']['name']) > title_limit:
    page_dict['db_show_dict']['name_title'] = page_dict['db_show_dict']['name'][0:title_limit] + '...'
  else:
    page_dict['db_show_dict']['name_title'] = page_dict['db_show_dict']['name']
  # ------------------------ ref name start ------------------------
  reference_name = page_dict['db_show_dict']['name'].replace("'","")
  reference_name = reference_name.replace(' ','')
  reference_name = reference_name.replace('-','')
  reference_name = reference_name.replace('!','')
  reference_name = reference_name.replace('?','')
  reference_name = reference_name.replace('.','')
  reference_name = reference_name.replace(',','')
  if len(reference_name) > 10:
    reference_name = reference_name[:10]
  page_dict['db_show_dict']['reference_name'] = reference_name
  # ------------------------ ref name end ------------------------
  # ------------------------ pull show info end ------------------------
  # ------------------------ variables start ------------------------
  page_dict['url_show_id'] = url_show_id
  page_dict['url_poll_id'] = url_poll_id
  page_dict['url_poll_id_random_next'] = None
  page_dict['poll_answered'] = False
  page_dict['poll_answered_dict'] = None
  page_dict['current_user_email'] = None
  page_dict['percent_total_polls_complete'] = int(0)
  page_dict['user_completed_all_polls'] = False
  page_dict['current_user_is_anonymous'] = False
  if current_user.is_anonymous == True:
    page_dict['current_user_is_anonymous'] = True
  else:
    page_dict['current_user_email'] = current_user.email
  # ------------------------ variables end ------------------------
  # ------------------------ pull show + poll combination start ------------------------
  poll_arr_of_dict = []
  # ------------------------ if poll id provided start ------------------------
  if url_poll_id != None:
    # ------------------------ check if poll exists in db start ------------------------
    db_poll_obj = get_poll_based_on_id_function(url_poll_id)
    if db_poll_obj == None:
      return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e6'))
    # ------------------------ check if poll exists in db end ------------------------
    if current_user.is_anonymous == True:
      # pull specific, unanswered or answered
      poll_arr_of_dict = select_general_function('select_query_general_2_anonymous', url_show_id, url_poll_id)
      # ------------------------ get next random question start ------------------------
      poll_arr_of_dict_next_random = select_general_function('select_query_general_1_anonymous_random', url_show_id, url_poll_id)
      if poll_arr_of_dict_next_random == None or poll_arr_of_dict_next_random == []:
        page_dict['url_poll_id_random_next'] = poll_arr_of_dict[0]['id']
      else:
        page_dict['url_poll_id_random_next'] = poll_arr_of_dict_next_random[0]['id']
      # ------------------------ get next random question end ------------------------
    else:
      user_to_lookup = current_user.id
      # ------------------------ admin check start ------------------------
      if current_user.email == os.environ.get('RUN_TEST_EMAIL'):
        user_to_lookup = 'ADMIN'
      # ------------------------ admin check end ------------------------
      # pull specific, unanswered or answered
      poll_arr_of_dict = select_general_function('select_query_general_2', url_show_id, url_poll_id, user_to_lookup)
  # ------------------------ if poll id provided end ------------------------
  # ------------------------ if poll id not provided start ------------------------
  else:
    if current_user.is_anonymous == True:
      # pull latest, unanswered - primary
      poll_arr_of_dict = select_general_function('select_query_general_3_anonymous', url_show_id)
      if poll_arr_of_dict == None or poll_arr_of_dict == []:
        # pull latest, unanswered - not primary
        poll_arr_of_dict = select_general_function('select_query_general_1_anonymous', url_show_id)
    else:
      # pull latest, unanswered - primary
      poll_arr_of_dict = select_general_function('select_query_general_1_primary', url_show_id, current_user.id)
      if poll_arr_of_dict == None or poll_arr_of_dict == []:
        # pull latest, unanswered - not primary
        poll_arr_of_dict = select_general_function('select_query_general_1', url_show_id, current_user.id)
    # all polls answered
    if poll_arr_of_dict == None or poll_arr_of_dict == []:
      if url_show_id == 'show_user_attributes':
        return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='s18'))
      else:
        return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='s17'))
  # ------------------------ if poll id not provided end ------------------------
  # ------------------------ poll dict prep start ------------------------
  try:
    page_dict['poll_dict'] = prep_poll_dict_function(poll_arr_of_dict[0])
  except:
    return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e41'))
  if url_poll_id == None or url_poll_id != page_dict['poll_dict']['id']:
    return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=page_dict['poll_dict']['id'], url_redirect_code=url_redirect_code))
  # ------------------------ poll dict prep end ------------------------
  # ------------------------ pull show + poll combination end ------------------------
  # ------------------------ pull + calculate status bar percent complete start ------------------------
  if current_user.is_anonymous == True:
    page_dict['percent_total_polls_complete'] = int(99)
  else:
    page_dict['percent_total_polls_complete'], page_dict['user_completed_all_polls'] = get_show_percent_of_all_polls_answered_function(current_user.id, url_show_id)
  # ------------------------ pull + calculate status bar percent complete end ------------------------
  # ------------------------ pull latest answer if exists start ------------------------
  try:
    if current_user.is_anonymous == True:
      if url_anonymous_code == 'submitted':
        page_dict['poll_answered'] = True
      pass
    else:
      db_latest_poll_obj = PollsAnsweredObj.query.filter_by(fk_show_id=url_show_id,fk_poll_id=url_poll_id,fk_user_id=current_user.id).order_by(PollsAnsweredObj.created_timestamp.desc()).first()
      page_dict['poll_answered_dict'] = arr_of_dict_all_columns_single_item_function(db_latest_poll_obj)
      page_dict['poll_answered'] = True
  except:
    pass
  # ------------------------ pull latest answer if exists end ------------------------
  # ------------------------ get poll statistics start ------------------------
  if page_dict['poll_answered'] == True:
    page_dict['show_colors_dict'] = get_create_show_chart_colors_function(page_dict)
    page_dict = get_poll_statistics_v2_function(page_dict, current_user)
  # ------------------------ get poll statistics end ------------------------
  # ------------------------ get reddit statistics start ------------------------
  if page_dict['poll_answered'] == True:
    page_dict = get_reddit_statistics_function(page_dict, current_user)
  # ------------------------ get reddit statistics end ------------------------
  if request.method == 'POST':
    if current_user.is_anonymous == True:
      return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=page_dict['poll_dict']['id'], url_redirect_code='e44', url_anonymous_code='submitted'))
    else:
      # ------------------------ check how many posts this person did today on this question start ------------------------
      total_poll_submissions_today = 0
      try:
        db_poll_answered_obj = PollsAnsweredObj.query.filter_by(fk_poll_id=url_poll_id,fk_user_id=current_user.id).order_by(PollsAnsweredObj.created_timestamp.desc()).all()
        if db_poll_answered_obj != None and db_poll_answered_obj != []:
          for i_obj in db_poll_answered_obj:
            submission_created_timestamp = i_obj.created_timestamp
            submission_date = submission_created_timestamp.date()
            today_date = datetime.now().date()
            if submission_date == today_date:
              total_poll_submissions_today += 1
          if total_poll_submissions_today >= 10:
            return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=url_poll_id, url_redirect_code='e35'))
      except:
        pass
      # ------------------------ check how many posts this person did today on this question end ------------------------
      # ------------------------ get ui start ------------------------
      ui_answer_selected = request.form.get('ui_selection_radio')
      ui_anonymous_check = request.form.get('ui_anonymous_check')
      ui_vote_question = request.form.get('ui_vote_question')
      ui_vote_feedback = request.form.get('ui_vote_feedback')
      ui_written_feedback = request.form.get('ui_written_feedback')
      # ------------------------ get ui end ------------------------
      # ------------------------ sanatize ui start ------------------------
      if ui_answer_selected not in page_dict['poll_dict']['answer_choices']:
        return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=page_dict['poll_dict']['id'], url_redirect_code='e6'))
      if ui_anonymous_check != None and ui_anonymous_check != 'ui_checked':
        return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=page_dict['poll_dict']['id'], url_redirect_code='e6'))
      if ui_vote_question != None and ui_vote_question != 'up' and ui_vote_question != 'down':
        return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=page_dict['poll_dict']['id'], url_redirect_code='e6'))
      if ui_vote_feedback != None and ui_vote_feedback != 'up' and ui_vote_feedback != 'down':
        return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=page_dict['poll_dict']['id'], url_redirect_code='e6'))
      ui_written_feedback = sanitize_text_v1_function(ui_written_feedback, 150, False)
      if ui_written_feedback == False:
        return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=page_dict['poll_dict']['id'], url_redirect_code='e6'))
      # ------------------------ sanatize ui end ------------------------
      # ------------------------ variables before insert start ------------------------
      if ui_vote_question == 'up' or ui_vote_question == None:
        ui_vote_question = True
      if ui_vote_question == 'down':
        ui_vote_question = False
      if ui_vote_feedback == 'up' or ui_vote_feedback == None:
        ui_vote_feedback = True
      if ui_vote_feedback == 'down':
        ui_vote_feedback = False
      if ui_anonymous_check == 'ui_checked':
        ui_anonymous_check = True
      # ------------------------ variables before insert end ------------------------
      # ------------------------ insert to db start ------------------------
      new_row = PollsAnsweredObj(
        id=create_uuid_function('vote_'),
        created_timestamp=create_timestamp_function(),
        fk_show_id=url_show_id,
        fk_poll_id=url_poll_id,
        fk_user_id=current_user.id,
        poll_answer_submitted=ui_answer_selected,
        written_answer_submitted=ui_written_feedback,
        status_answer_anonymous=ui_anonymous_check,
        poll_vote_updown_question=ui_vote_question,
        poll_vote_updown_feedback=ui_vote_feedback
      )
      db.session.add(new_row)
      db.session.commit()
      # ------------------------ insert to db end ------------------------
      # ------------------------ make sure user is following the show if submitted answer start ------------------------
      db_following_obj = ShowsFollowingObj.query.filter_by(fk_show_id=url_show_id,fk_user_id=current_user.id).first()
      if db_following_obj == None or db_following_obj == []:
        # ------------------------ insert to db start ------------------------
        new_row = ShowsFollowingObj(
          id=create_uuid_function('following_'),
          created_timestamp=create_timestamp_function(),
          fk_platform_id='podcast',
          fk_show_id=url_show_id,
          fk_user_id=current_user.id
        )
        db.session.add(new_row)
        db.session.commit()
        # ------------------------ insert to db end ------------------------
      # ------------------------ make sure user is following the show if submitted answer end ------------------------
      if current_user.email != os.environ.get('RUN_TEST_EMAIL'):
        # ------------------------ email self start ------------------------
        try:
          output_to_email = os.environ.get('HR_SUPPORT_EMAIL')
          output_subject = f"Poll answered for '{page_dict['db_show_dict']['name']}' by '{current_user.email}'"
          output_body = f"<p>{current_user.email} answered a poll for '{page_dict['db_show_dict']['name']}'</p>\
                          <p>Question: '{page_dict['poll_dict']['question']}'</p>\
                          <p>Voted: {ui_answer_selected}</p>\
                          <p>Written: '{ui_written_feedback}'</p>"
          send_email_template_function(output_to_email, output_subject, output_body)
        except:
          pass
        # ------------------------ email self end ------------------------
      return redirect(url_for('polling_views_interior.polling_show_function', url_show_id=url_show_id, url_poll_id=page_dict['poll_dict']['id']))
  localhost_print_function(' ------------- 100-show poll start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-show poll end ------------- ')
  return render_template('polling/interior/poll/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/create/<url_show_id>', methods=['GET', 'POST'])
@polling_views_interior.route('/create/<url_show_id>/', methods=['GET', 'POST'])
@polling_views_interior.route('/create/<url_show_id>/<url_redirect_code>', methods=['GET', 'POST'])
@polling_views_interior.route('/create/<url_show_id>/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def polling_create_poll_function(url_redirect_code=None, url_show_id=None):
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
  # ------------------------ navbar variable start ------------------------
  page_dict['current_user_email'] = current_user.email
  # ------------------------ navbar variable end ------------------------
  # ------------------------ if no show id start ------------------------
  if url_show_id == None:
    return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e6'))
  # ------------------------ if no show id end ------------------------
  # ------------------------ ensure show id exists start ------------------------
  db_show_obj = get_show_based_on_id_function(url_show_id)
  if db_show_obj == None:
    return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e6'))
  page_dict['db_show_dict'] = arr_of_dict_all_columns_single_item_function(db_show_obj)
  title_limit = 15
  if len(page_dict['db_show_dict']['name']) > title_limit:
    page_dict['db_show_dict']['name_title'] = page_dict['db_show_dict']['name'][0:title_limit] + '...'
  else:
    page_dict['db_show_dict']['name_title'] = page_dict['db_show_dict']['name']
  # ------------------------ ensure show id exists end ------------------------
  # ------------------------ ensure user is following the show start ------------------------
  new_following_updated = follow_show_function(current_user, url_show_id)
  if new_following_updated == True:
    return redirect(url_for('polling_views_interior.polling_create_poll_function', url_show_id=url_show_id))
  # ------------------------ ensure user is following the show end ------------------------
  # ------------------------ provide array of answer choice amount allowed start ------------------------
  page_dict['allowed_answers_arr'] = [i for i in range(1, 10+1)]
  # ------------------------ provide array of answer choice amount allowed end ------------------------
  # ------------------------ submission start ------------------------
  if request.method == 'POST':
    # ------------------------ get ui start ------------------------
    ui_question = request.form.get('ui_question')
    ui_answer_choices_arr = request.form.getlist('ui_answer_choices')
    max_character_count = 1000
    character_count_n1 = 480
    # ------------------------ get ui end ------------------------
    # ------------------------ sanatize ui start ------------------------
    # sanitize question
    ui_question = sanitize_text_v2_function(ui_question, character_count_n1, True)
    if ui_question == False:
      return redirect(url_for('polling_views_interior.polling_create_poll_function', url_redirect_code='e36', url_show_id=url_show_id))
    # sanitize answer choices
    ui_answer_choices_arr_cleaned = []
    for i in ui_answer_choices_arr:
      if i == '':
        continue
      i = sanitize_text_v2_function(i, character_count_n1, False)
      if i == False:
        return redirect(url_for('polling_views_interior.polling_create_poll_function', url_redirect_code='e37', url_show_id=url_show_id))
      ui_answer_choices_arr_cleaned.append(i)
    if len(ui_answer_choices_arr_cleaned) < 2:
      return redirect(url_for('polling_views_interior.polling_create_poll_function', url_redirect_code='e39', url_show_id=url_show_id))
    ui_answer_choices_str = "~".join(ui_answer_choices_arr_cleaned)
    if len(ui_answer_choices_str) > max_character_count:
      return redirect(url_for('polling_views_interior.polling_create_poll_function', url_redirect_code='e38', url_show_id=url_show_id))
    # ------------------------ sanatize ui end ------------------------
    # ------------------------ check if user submitted max amount for today for this show start ------------------------
    total_polls_created_today_by_user_for_show = get_total_polls_created_today_by_user_for_one_show_function(current_user.id,url_show_id)
    if int(total_polls_created_today_by_user_for_show) > 10:
      return redirect(url_for('polling_views_interior.polling_create_poll_function', url_redirect_code='e40', url_show_id=url_show_id))
    # ------------------------ check if user submitted max amount for today for this show end ------------------------
    # ------------------------ insert to db start ------------------------
    new_poll_id=create_uuid_function('poll_')
    # ------------------------ admin logic start ------------------------
    poll_user_to_insert = current_user.id
    if current_user.email == os.environ.get('RUN_TEST_EMAIL'):
      poll_user_to_insert = 'ADMIN'
    # ------------------------ admin logic end ------------------------
    new_row = PollsObj(
      id=new_poll_id,
      created_timestamp=create_timestamp_function(),
      type='show',
      fk_show_id=url_show_id,
      question=ui_question,
      answer_choices=ui_answer_choices_str,
      written_response_allowed=True,
      status_approved=False,
      status_removed=False,
      fk_user_id=poll_user_to_insert
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ insert to db end ------------------------
    # ------------------------ redirect to poll start ------------------------
    return redirect(url_for('polling_views_interior.polling_show_function', url_redirect_code='s19', url_show_id=url_show_id, url_poll_id=new_poll_id))
    # ------------------------ redirect to poll end ------------------------
  # ------------------------ submission end ------------------------
  localhost_print_function(' ------------- 100-create poll start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-create poll end ------------- ')
  return render_template('polling/interior/poll/create/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/create/all', methods=['GET', 'POST'])
@polling_views_interior.route('/create/all/', methods=['GET', 'POST'])
@polling_views_interior.route('/create/all/<url_redirect_code>', methods=['GET', 'POST'])
@polling_views_interior.route('/create/all/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def polling_view_all_created_polls_function(url_redirect_code=None):
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
  # ------------------------ navbar variable start ------------------------
  page_dict['current_user_email'] = current_user.email
  # ------------------------ navbar variable end ------------------------
  # ------------------------ pull all created polls start ------------------------
  page_dict['created_polls_arr_of_dict'] = select_general_function('select_query_general_5', current_user.id)
  if page_dict['created_polls_arr_of_dict'] == None or page_dict['created_polls_arr_of_dict'] == []:
    return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e43'))
  # ------------------------ pull all created polls end ------------------------
  localhost_print_function(' ------------- 100-created polls start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-created polls end ------------- ')
  return render_template('polling/interior/poll/create/view_all_created/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@polling_views_interior.route('/request/reddit/<url_show_id>/<url_poll_id>', methods=['GET', 'POST'])
@polling_views_interior.route('/request/reddit/<url_show_id>/<url_poll_id>/', methods=['GET', 'POST'])
@login_required
def request_reddit_post_function(url_show_id=None, url_poll_id=None):
  if url_show_id == None or url_poll_id == None:
    return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e6'))
  db_show_obj = ShowsObj.query.filter_by(id=url_show_id).first()
  db_poll_obj = PollsObj.query.filter_by(id=url_poll_id).first()
  if db_show_obj == None or db_show_obj == [] or db_poll_obj == None or db_poll_obj == []:
    return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='e6'))
  else:
    # ------------------------ check if user already requested start ------------------------
    db_requested_obj = RedditPostsRequestedObj.query.filter_by(fk_user_id=current_user.id,fk_show_id=url_show_id,fk_poll_id=url_poll_id).first()
    if db_requested_obj != None and db_requested_obj != []:
      return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='s22'))
    # ------------------------ check if user already requested end ------------------------
    # ------------------------ insert email to db start ------------------------
    try:
      new_row_email = RedditPostsRequestedObj(
        id = create_uuid_function('request_'),
        created_timestamp = create_timestamp_function(),
        fk_show_id = url_show_id,
        fk_poll_id = url_poll_id,
        fk_user_id = current_user.id
      )
      db.session.add(new_row_email)
      db.session.commit()
    except:
      pass
    # ------------------------ insert email to db end ------------------------
  return redirect(url_for('polling_views_interior.polling_dashboard_function', url_redirect_code='s22'))
# ------------------------ individual route end ------------------------