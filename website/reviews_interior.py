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
from website import db
from website.models import UserObj, EmailSentObj, UserAttributesObj, ShowsFollowingObj, ShowsObj, PollsObj, PollsAnsweredObj, ShowsQueueObj, RedditPostsRequestedObj
from website.backend.candidates.redis import redis_check_if_cookie_exists_function, redis_connect_to_database_function
from website.backend.candidates.user_inputs import alert_message_default_function_v2
from website.backend.candidates.browser import browser_response_set_cookie_function_v6
from website.backend.onboarding import onboarding_checks_v2_function
# ------------------------ imports end ------------------------

# ------------------------ function start ------------------------
reviews_interior = Blueprint('reviews_interior', __name__)
# ------------------------ function end ------------------------
# ------------------------ connect to redis start ------------------------
redis_connection = redis_connect_to_database_function()
# ------------------------ connect to redis end ------------------------

# ------------------------ individual route start ------------------------
@reviews_interior.route('/dashboard', methods=['GET', 'POST'])
@reviews_interior.route('/dashboard/', methods=['GET', 'POST'])
@reviews_interior.route('/dashboard/<url_redirect_code>', methods=['GET', 'POST'])
@reviews_interior.route('/dashboard/<url_redirect_code>/', methods=['GET', 'POST'])
@login_required
def dashboard_function(url_redirect_code=None):
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
    return redirect(url_for('reviews_interior.feedback_function', url_feedback_code=onbaording_status))
  # ------------------------ onboarding checks end ------------------------
  # ------------------------ navbar variable start ------------------------
  page_dict['current_user_email'] = current_user.email
  # ------------------------ navbar variable end ------------------------
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'reviews_templates/interior/dashboard/index.html'
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
@reviews_interior.route('/feedback/<url_feedback_code>', methods=['GET', 'POST'])
@reviews_interior.route('/feedback/<url_feedback_code>/', methods=['GET', 'POST'])
@reviews_interior.route('/feedback/<url_feedback_code>/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def feedback_function(url_redirect_code=None, url_feedback_code=None):
  # ------------------------ page dict start ------------------------
  alert_message_dict = alert_message_default_function_v2(url_redirect_code)
  page_dict = {}
  page_dict['alert_message_dict'] = alert_message_dict
  # ------------------------ page dict end ------------------------
  # ------------------------ double check redirect start ------------------------
  if url_feedback_code != 'attribute_marketing' and url_feedback_code != 'attribute_birthday':
    return redirect(url_for('reviews_interior.dashboard_function'))
  db_user_attribute_obj = UserAttributesObj.query.filter_by(attribute_code=url_feedback_code,fk_user_id=current_user.id).first()
  if db_user_attribute_obj != None:
    return redirect(url_for('reviews_interior.dashboard_function', url_redirect_code='s20'))
  # ------------------------ double check redirect end ------------------------
  # ------------------------ set loading bar variables start ------------------------
  if url_feedback_code == 'attribute_birthday':
    page_dict['feedback_request'] = url_feedback_code
  if url_feedback_code == 'attribute_marketing':
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
        return redirect(url_for('reviews_interior.dashboard_function'))
    # ------------------------ double check redirect end ------------------------
    # ------------------------ double check redirect start ------------------------
    db_user_attribute_obj = UserAttributesObj.query.filter_by(attribute_code=url_feedback_code,fk_user_id=current_user.id).first()
    if db_user_attribute_obj != None:
      return redirect(url_for('reviews_interior.dashboard_function'))
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
      return redirect(url_for('reviews_interior.dashboard_function'))
    # ------------------------ post feedback tos end ------------------------
    # ------------------------ post feedback birthday start ------------------------
    if url_feedback_code == 'attribute_birthday':
      # ------------------------ get user inputs start ------------------------
      ui_birthday = request.form.get('ui_birthday')
      # ------------------------ get user inputs end ------------------------
      # ------------------------ sanatize inputs start ------------------------
      ui_year, ui_month, ui_day = return_ints_from_str_function(ui_birthday)
      if ui_year == False or ui_month == False or ui_day == False:
        return redirect(url_for('reviews_interior.feedback_function', url_redirect_code='e6'))
      # ------------------------ sanatize inputs end ------------------------
      # ------------------------ sanatize inputs start ------------------------
      try:
        # birth month
        if int(ui_month) not in months_arr:
          return redirect(url_for('reviews_interior.feedback_function', url_redirect_code='e20', url_feedback_code=url_feedback_code))
      except:
        pass
      try:
        # birth day
        allowed_days_arr = month_day_dict[str(ui_month)]
        if int(ui_day) not in allowed_days_arr:
          return redirect(url_for('reviews_interior.feedback_function', url_redirect_code='e21', url_feedback_code=url_feedback_code))
      except:
        pass
      try:
        # birth year
        if int(ui_year) not in years_arr:
          return redirect(url_for('reviews_interior.feedback_function', url_redirect_code='e26', url_feedback_code=url_feedback_code))
      except:
        pass
      # ------------------------ sanatize inputs end ------------------------
      # ------------------------ age check start ------------------------
      current_age = get_years_from_date_function(ui_year, ui_month, ui_day)
      # if float(current_age) < float(18.0):
      #   return redirect(url_for('reviews_interior.feedback_function', url_redirect_code='e30', url_feedback_code=url_feedback_code))
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
      return redirect(url_for('reviews_interior.dashboard_function'))
    # ------------------------ post feedback birthday end ------------------------
    # ------------------------ post feedback marketing start ------------------------
    if url_feedback_code == 'attribute_marketing':
      ui_answer = request.form.get('ui_general_selection_radio')
      # ------------------------ invalid start ------------------------
      if ui_answer not in marketing_list:
        return redirect(url_for('reviews_interior.feedback_function', url_feedback_code=url_feedback_code, url_redirect_code='e6'))
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
      return redirect(url_for('reviews_interior.dashboard_function'))
    # ------------------------ post feedback marketing end ------------------------ 
    # ------------------------ post feedback twitter start ------------------------
    if url_feedback_code == 'x_twitter_handle':
      ui_twitter_username = request.form.get('ui_twitter_username')
      # ------------------------ x sanitize start ------------------------
      ui_twitter_username_check = sanitize_x_handle_function(ui_twitter_username)
      if ui_twitter_username_check == False:
        return redirect(url_for('reviews_interior.feedback_function', url_redirect_code='e6', url_feedback_code=url_feedback_code))
      # ------------------------ x sanitize end ------------------------
      # ------------------------ insert to db start ------------------------
      new_row = UserAttributesObj(
        id=create_uuid_function('attribute_'),
        created_timestamp=create_timestamp_function(),
        fk_user_id=current_user.id,
        product='polling',
        attribute_code=url_feedback_code,
        attribute_response=ui_twitter_username
      )
      db.session.add(new_row)
      db.session.commit()
      # # ------------------------ insert to db end ------------------------
      return redirect(url_for('reviews_interior.dashboard_function'))
    # ------------------------ post feedback twitter end ------------------------
  # ------------------------ submission end ------------------------
  # ------------------------ set cookie on first feedback step start ------------------------
  if url_feedback_code == 'attribute_tos':
    # ------------------------ for setting cookie start ------------------------
    template_location_url = 'reviews_templates/interior/feedback/index.html'
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
    return render_template('reviews_templates/interior/feedback/index.html', page_dict_to_html=page_dict)
# ------------------------ individual route end ------------------------

# ------------------------ individual route start ------------------------
@reviews_interior.route('/account', methods=['GET', 'POST'])
@reviews_interior.route('/account/', methods=['GET', 'POST'])
@reviews_interior.route('/account/<url_redirect_code>', methods=['GET', 'POST'])
@login_required
def account_function(url_redirect_code=None):
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
    return redirect(url_for('reviews_interior.feedback_function', url_feedback_code=onbaording_status))
  # ------------------------ onboarding checks end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['current_user_email'] = current_user.email
  # ------------------------ set variables end ------------------------
  # ------------------------ for setting cookie start ------------------------
  template_location_url = 'reviews_templates/interior/account/index.html'
  # ------------------------ for setting cookie end ------------------------
  localhost_print_function(' ------------- 100-profile start ------------- ')
  page_dict = dict(sorted(page_dict.items(),key=lambda x:x[0]))
  for k,v in page_dict.items():
    localhost_print_function(f"k: {k} | v: {v}")
    pass
  localhost_print_function(' ------------- 100-profile end ------------- ')
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