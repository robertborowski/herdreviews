# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from flask_login import login_required, current_user
from website.backend.candidates.autogeneration import question_choices_function
from website.backend.candidates.datetime_manipulation import days_times_timezone_arr_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
from website.backend.candidates.string_manipulation import all_employee_question_categories_sorted_function
from website.backend.candidates.string_manipulation import capitalize_all_words_function
from website.backend.candidates.dropdowns import get_activity_a_dropdowns_function
from website.backend.candidates.send_emails import send_email_template_function
import os
from website import db
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def activity_settings_prep_function(page_dict, url_activity_code, db_activity_settings_dict, url_activity_type):
  page_dict['url_activity_code'] = url_activity_code
  page_dict['url_activity_type'] = url_activity_type
  # ------------------------ page title start ------------------------
  page_dict['title'] = capitalize_all_words_function(url_activity_code)
  page_dict['title'] = page_dict['title'] + ' Settings'
  # ------------------------ page title end ------------------------
  # ------------------------ get dropdowns start ------------------------
  page_dict['settings_dict'] = db_activity_settings_dict
  page_dict['dropdown_weekdays'], page_dict['dropdown_times'], page_dict['dropdown_timezones'] = days_times_timezone_arr_function()
  page_dict['dropdown_cadence_arr'], page_dict['dropdown_question_num_arr'], page_dict['dropdown_question_type_arr'] = question_choices_function()
  page_dict['dropdowns_dict'] = get_activity_a_dropdowns_function()
  # ------------------------ get dropdowns end ------------------------
  # ------------------------ get all categories start ------------------------
  if url_activity_type != 'activity_type_b':
    query_result_arr_of_dicts = select_general_function('select_all_employees_categories_v1')
    page_dict['all_categories_arr'] = all_employee_question_categories_sorted_function(query_result_arr_of_dicts)
  # ------------------------ get all categories end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def activity_settings_post_function(page_dict, url_activity_code, url_activity_type, db_activity_settings_obj, db_activity_settings_dict, ui_start_day, ui_start_time, ui_end_day, ui_end_time, ui_timezone, ui_cadence, ui_total_questions, ui_question_type, ui_select_all_categories, ui_selected_categories):
  post_result = False
  # ------------------------ check if ui is invalid start ------------------------
  if ui_start_day == None and ui_start_time == None and ui_end_day == None and ui_end_time == None and ui_cadence == None and ui_total_questions == None and ui_question_type == None:
    # ------------------------ defaults start ------------------------
    ui_start_day = 'Monday'
    ui_start_time = '12 PM'
    ui_end_day = 'Thursday'
    ui_end_time = '1 PM'
    ui_cadence = 'Weekly'
    if url_activity_type == 'activity_type_a':
      ui_total_questions = 10
      ui_question_type = 'Mixed'
    # ------------------------ defaults end ------------------------
  if ui_start_day not in page_dict['dropdown_weekdays'] or ui_end_day not in page_dict['dropdown_weekdays'] or ui_start_time not in page_dict['dropdown_times'] or ui_end_time not in page_dict['dropdown_times'] or ui_timezone not in page_dict['dropdown_timezones'] or ui_cadence not in page_dict['dropdown_cadence_arr']:
    return 'dropdown_error', page_dict
  if url_activity_type == 'activity_type_a':
    if int(ui_total_questions) not in page_dict['dropdown_question_num_arr'] or ui_question_type not in page_dict['dropdown_question_type_arr']:
      return 'dropdown_error', page_dict
    if ui_selected_categories != [] and ui_selected_categories != None:
      for i in ui_selected_categories:
        if i not in page_dict['all_categories_arr']:
          return 'category_error', page_dict
  # ------------------------ check if ui is invalid start ------------------------
  # ------------------------ if settings changed start ------------------------
  settings_change_occured = False
  # ------------------------ if 'all_categories' selected start ------------------------
  if url_activity_type == 'activity_type_a':
    if ui_select_all_categories == 'all_categories':
      if db_activity_settings_dict['categories'] == 'all_categories':
        pass
      else:
        settings_change_occured = True
        db_activity_settings_obj.categories = 'all_categories'
    # ------------------------ if 'all_categories' selected end ------------------------
    # ------------------------ if 'all_categories' not selected start ------------------------
    if ui_select_all_categories == None:
      if ui_selected_categories == [] or len(ui_selected_categories) == 0:
        return 'select_error', page_dict
      ui_selected_categories_str = ",".join(ui_selected_categories)
      if ui_selected_categories_str == db_activity_settings_dict['categories']:
        pass
      else:
        settings_change_occured = True
        db_activity_settings_obj.categories = ui_selected_categories_str
        # ------------------------ email self start ------------------------
        try:
          output_to_email = os.environ.get('HR_SUPPORT_EMAIL')
          output_subject = f'HerdReviews - Employees Settings Categories Changed - {current_user.email}'
          output_body = f"<p>Hi there,</p>\
                          <p>{current_user.email} changed their categories to: [{ui_selected_categories_str}]</p>\
                          <p style='margin:0;'>Best,</p>\
                          <p style='margin:0;'>HerdReviews Support Team</p>"
          send_email_template_function(output_to_email, output_subject, output_body)
        except:
          pass
        # ------------------------ email self end ------------------------
    # ------------------------ if 'all_categories' not selected end ------------------------
  if ui_start_day != db_activity_settings_dict['start_day']:
    settings_change_occured = True
    db_activity_settings_obj.start_day = ui_start_day
  if ui_start_time != db_activity_settings_dict['start_time']:
    settings_change_occured = True
    db_activity_settings_obj.start_time = ui_start_time
  if ui_end_day != db_activity_settings_dict['end_day']:
    settings_change_occured = True
    db_activity_settings_obj.end_day = ui_end_day
  if ui_end_time != db_activity_settings_dict['end_time']:
    settings_change_occured = True
    db_activity_settings_obj.end_time = ui_end_time
  if ui_timezone != db_activity_settings_dict['timezone']:
    settings_change_occured = True
    db_activity_settings_obj.timezone = ui_timezone
  if ui_cadence != db_activity_settings_dict['cadence']:
    settings_change_occured = True
    db_activity_settings_obj.cadence = ui_cadence
  if url_activity_type == 'activity_type_a':
    if int(ui_total_questions) != db_activity_settings_dict['total_questions']:
      settings_change_occured = True
      db_activity_settings_obj.total_questions = ui_total_questions
    if ui_question_type != db_activity_settings_dict['question_type']:
      settings_change_occured = True
      db_activity_settings_obj.question_type = ui_question_type
  # ------------------------ if new start/end day/times make sense start ------------------------
  start_day_index = page_dict['dropdown_weekdays'].index(ui_start_day)
  start_time_index = page_dict['dropdown_times'].index(ui_start_time)
  end_day_index = page_dict['dropdown_weekdays'].index(ui_end_day)
  end_time_index = page_dict['dropdown_times'].index(ui_end_time)
  if start_day_index > end_day_index or (start_day_index == end_day_index and start_time_index >= end_time_index):
    return 'overlap_error', page_dict
  # ------------------------ if new start/end day/times make sense end ------------------------
  if settings_change_occured == True:
    db.session.commit()
    return 'success_code', page_dict
  # ------------------------ if no change in settings start ------------------------
  if settings_change_occured == False:
    return 'no_change', page_dict
  # ------------------------ if no change in settings end ------------------------
  return post_result, page_dict
# ------------------------ individual function end ------------------------