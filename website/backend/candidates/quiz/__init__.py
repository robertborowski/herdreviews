# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import re
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from website.backend.candidates.sql_statements.sql_statements_select import select_general_function
from website.models import ActivityASettingsObj, ActivityATestObj, ActivityAGroupQuestionsUsedObj, ActivityATestGradedObj, UserObj, EmailSentObj, ActivityBTestObj, ActivityBGroupQuestionsUsedObj
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function
from website import db
from website.backend.candidates.datetime_manipulation import get_current_weekday_function, get_current_hour_function, get_upcoming_date_function, build_out_datetime_from_parts_function, get_week_dates_function, get_weekday_dict_function_v2
import os, time
from website.backend.candidates.sql_statements.sql_prep import prepare_where_clause_function
from datetime import date, timedelta, datetime
import difflib
import json
from website.backend.candidates.send_emails import send_email_template_function
from website.backend.candidates.pull_create_logic import pull_create_activity_settings_obj_function, pull_latest_activity_test_obj_function
# ------------------------ imports end ------------------------

# ------------------------ Set Timezone START ------------------------
# Set the timezone of the application when user creates account is will be in US/Easterm time
os.environ['TZ'] = 'US/Eastern'
time.tzset()
# ------------------------ Set Timezone END ------------------------

# ------------------------ individual function start ------------------------
def build_question_type_arr_function(input_type, input_total_questions):
  input_total_questions = int(input_total_questions)
  options_arr = ['Fill in the blank', 'Multiple choice', 'Mixed']
  question_types_arr = []
  # ------------------------ method 1 start ------------------------
  # counter=0
  # while counter < input_total_questions:
  #   counter+=1
  #   if input_type == options_arr[0]:
  #     question_types_arr.append(options_arr[0])
  #   if input_type == options_arr[1]:
  #     question_types_arr.append(options_arr[1])
  #   if input_type == options_arr[2]:
  #     if counter % 2 == 0:
  #       question_types_arr.append(options_arr[1])
  #     else:
  #       question_types_arr.append(options_arr[0])
  # ------------------------ method 1 end ------------------------
  # ------------------------ method 2 start ------------------------
  if input_type == 'Multiple choice':
    if input_total_questions == 10:
      question_types_arr = ['Multiple choice','Multiple choice','Multiple choice','Multiple choice','Multiple choice','Multiple choice','Multiple choice','Multiple choice','Multiple choice','Multiple choice']
    elif input_total_questions == 5:
      question_types_arr = ['Multiple choice','Multiple choice','Multiple choice','Multiple choice','Multiple choice']
  elif input_type == 'Fill in the blank':
    if input_total_questions == 10:
      question_types_arr = ['Fill in the blank','Fill in the blank','Fill in the blank','Fill in the blank','Fill in the blank','Fill in the blank','Fill in the blank','Fill in the blank','Fill in the blank','Fill in the blank']
    elif input_total_questions == 5:
      question_types_arr = ['Fill in the blank','Fill in the blank','Fill in the blank','Fill in the blank','Fill in the blank']
  elif input_type == 'Mixed':
    if input_total_questions == 10:
      question_types_arr = ['Multiple choice','Multiple choice','Multiple choice','Multiple choice','Multiple choice','Multiple choice','Multiple choice','Multiple choice','Fill in the blank','Fill in the blank']
    elif input_total_questions == 5:
      question_types_arr = ['Multiple choice','Multiple choice','Multiple choice','Multiple choice','Fill in the blank']
  # ------------------------ method 2 end ------------------------
  question_types_str = ','.join(question_types_arr)
  return question_types_str
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_next_quiz_open_function(current_user, url_activity_code, url_activity_type):
  # ------------------------ get group settings start ------------------------
  db_group_settings_obj = pull_create_activity_settings_obj_function(current_user, url_activity_code, url_activity_type)
  db_group_settings_dict = arr_of_dict_all_columns_single_item_function(db_group_settings_obj)
  # ------------------------ get group settings end ------------------------
  # ------------------------ get latest test start ------------------------
  db_tests_obj = pull_latest_activity_test_obj_function(current_user, url_activity_code, url_activity_type)
  db_tests_dict = arr_of_dict_all_columns_single_item_function(db_tests_obj)
  # ------------------------ get latest test end ------------------------
  # ------------------------ get next quiz open start ------------------------
  weekday_dict = get_weekday_dict_function_v2()
  latest_test_dates_of_week_end_arr = get_week_dates_function(db_tests_dict['end_timestamp'].date())
  monday_of_lastest_test_end_week = latest_test_dates_of_week_end_arr[0]
  if db_group_settings_dict['cadence'] == 'Weekly':
    should_be_this_weeks_monday = monday_of_lastest_test_end_week + timedelta(days=7)
  elif db_group_settings_dict['cadence'] == 'Biweekly':
    should_be_this_weeks_monday = monday_of_lastest_test_end_week + timedelta(days=14)
  elif db_group_settings_dict['cadence'] == 'Monthly':
    should_be_this_weeks_monday = monday_of_lastest_test_end_week + timedelta(days=28)
  should_be_dates_of_week_arr = get_week_dates_function(should_be_this_weeks_monday)
  next_quiz_open_start_date = should_be_dates_of_week_arr[weekday_dict[db_group_settings_dict['start_day']]]
  final_str = db_group_settings_dict['start_day'] + ' ' + next_quiz_open_start_date.strftime('%m/%d') + ', ' + db_group_settings_dict['start_time'] + ' ' + db_group_settings_dict['timezone']
  # ------------------------ get next quiz open end ------------------------
  return final_str
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def compare_candence_vs_previous_quiz_function(db_group_settings_dict, db_tests_obj):
  # ------------------------ desired start ------------------------
  desired_start_day = db_group_settings_dict['start_day']
  desired_cadence = db_group_settings_dict['cadence']
  # ------------------------ desired end ------------------------
  # ------------------------ all tests type conversion start ------------------------
  tests_arr_of_dicts = []
  for i in db_tests_obj:
    db_tests_dict = arr_of_dict_all_columns_single_item_function(i)
    tests_arr_of_dicts.append(db_tests_dict)
  # ------------------------ all tests type conversion end ------------------------
  # ------------------------ latest test checks start ------------------------
  latest_test_dict = tests_arr_of_dicts[0]
  latest_test_start_date = latest_test_dict['start_timestamp'].date()
  latest_test_end_date = latest_test_dict['end_timestamp'].date()
  latest_test_dates_of_week_start_arr = get_week_dates_function(latest_test_start_date)
  latest_test_dates_of_week_end_arr = get_week_dates_function(latest_test_end_date)
  todays_date = date.today()
  if todays_date in latest_test_dates_of_week_start_arr or todays_date in latest_test_dates_of_week_end_arr:
    return False
  else:
    if desired_cadence == 'Weekly':
      return True
    if desired_cadence == 'Biweekly' or desired_cadence == 'Monthly':
      monday_of_lastest_test_end_week = latest_test_dates_of_week_end_arr[0]    # 'datetime.date' | 2023-02-06
      if desired_cadence == 'Biweekly':
        should_be_this_weeks_monday = monday_of_lastest_test_end_week + timedelta(days=14)  # 'datetime.date' | 2023-02-20
      if desired_cadence == 'Monthly':
        should_be_this_weeks_monday = monday_of_lastest_test_end_week + timedelta(days=28)  # 'datetime.date' | 2023-02-20
      should_be_dates_of_week_arr = get_week_dates_function(should_be_this_weeks_monday)
      if todays_date in should_be_dates_of_week_arr or todays_date >= max(should_be_dates_of_week_arr):
        return True
  # ------------------------ latest test checks end ------------------------
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def compare_candence_vs_previous_quiz_function_v2(current_user, db_tests_obj, activity_name, activity_type):
  # ------------------------ get group activity settings start ------------------------
  db_activity_settings_obj = pull_create_activity_settings_obj_function(current_user, activity_name, activity_type)
  db_activity_settings_dict = arr_of_dict_all_columns_single_item_function(db_activity_settings_obj)
  # ------------------------ get group activity settings end ------------------------
  # ------------------------ desired start ------------------------
  desired_start_day = db_activity_settings_dict['start_day']
  desired_cadence = db_activity_settings_dict['cadence']
  # ------------------------ desired end ------------------------
  # ------------------------ latest test checks start ------------------------
  latest_test_dict = arr_of_dict_all_columns_single_item_function(db_tests_obj)
  latest_test_start_date = latest_test_dict['start_timestamp'].date()
  latest_test_end_date = latest_test_dict['end_timestamp'].date()
  latest_test_dates_of_week_start_arr = get_week_dates_function(latest_test_start_date)
  latest_test_dates_of_week_end_arr = get_week_dates_function(latest_test_end_date)
  todays_date = date.today()
  if todays_date in latest_test_dates_of_week_start_arr or todays_date in latest_test_dates_of_week_end_arr:
    return False
  else:
    if desired_cadence == 'Weekly':
      return True
    if desired_cadence == 'Biweekly' or desired_cadence == 'Monthly':
      monday_of_lastest_test_end_week = latest_test_dates_of_week_end_arr[0]    # 'datetime.date' | 2023-02-06
      if desired_cadence == 'Biweekly':
        should_be_this_weeks_monday = monday_of_lastest_test_end_week + timedelta(days=14)  # 'datetime.date' | 2023-02-20
      if desired_cadence == 'Monthly':
        should_be_this_weeks_monday = monday_of_lastest_test_end_week + timedelta(days=28)  # 'datetime.date' | 2023-02-20
      should_be_dates_of_week_arr = get_week_dates_function(should_be_this_weeks_monday)
      if todays_date in should_be_dates_of_week_arr or todays_date >= max(should_be_dates_of_week_arr):
        return True
  # ------------------------ latest test checks end ------------------------
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def create_quiz_function(group_id, immediate=False):
  # ------------------------ Set Timezone START ------------------------
  # Set the timezone of the application when user creates account is will be in US/Easterm time
  os.environ['TZ'] = 'US/Eastern'
  time.tzset()
  # ------------------------ Set Timezone END ------------------------
  # ------------------------ pull group settings start ------------------------
  db_group_settings_obj = ActivityASettingsObj.query.filter_by(fk_group_id=group_id,product='trivia').order_by(ActivityASettingsObj.created_timestamp.desc()).first()
  db_group_settings_dict = arr_of_dict_all_columns_single_item_function(db_group_settings_obj)
  # ------------------------ pull group settings end ------------------------
  # ------------------------ pull latest tests check start ------------------------
  correct_cadence = False
  db_tests_obj = ActivityATestObj.query.filter_by(fk_group_id=db_group_settings_dict['fk_group_id'],product='trivia').order_by(ActivityATestObj.created_timestamp.desc()).all()
  if db_tests_obj == None or db_tests_obj == []:
    correct_cadence = True
  else:
    # ------------------------ update correct_cadence based on previous two quizzes start ------------------------
    quiz_to_be_made_check = compare_candence_vs_previous_quiz_function(db_group_settings_dict, db_tests_obj)
    if quiz_to_be_made_check == True:
      correct_cadence = True
    # ------------------------ update correct_cadence based on previous two quizzes end ------------------------
  # ------------------------ pull latest tests check end ------------------------
  # ------------------------ create quiz start ------------------------
  if correct_cadence == True:
    # ------------------------ if quiz to be made immediately (first quiz) start ------------------------
    if immediate == True:
      db_group_settings_dict['start_day'] = get_current_weekday_function()
      db_group_settings_dict['start_time'] = get_current_hour_function()  # will return current hour in EST
      # ------------------------ construct start/end timestamps start ------------------------
      start_date_str = get_upcoming_date_function(db_group_settings_dict['start_day'])
      end_date_str = get_upcoming_date_function(db_group_settings_dict['end_day'], start_date_str)
      start_timestamp_created = build_out_datetime_from_parts_function(start_date_str, db_group_settings_dict['start_time'], 'EST')
      end_timestamp_created = build_out_datetime_from_parts_function(end_date_str, db_group_settings_dict['end_time'], db_group_settings_dict['timezone'])    # converted to EST for job runs
      if end_timestamp_created <= start_timestamp_created:
        return 'false_end_time'
      # ------------------------ construct start/end timestamps end ------------------------
      # ------------------------ if quiz to be made immediately (first quiz) end ------------------------
    else:
      # ------------------------ get this weeks dates start ------------------------
      todays_date = date.today()
      latest_test_dates_of_week_arr = get_week_dates_function(todays_date)
      # ------------------------ get this weeks dates end ------------------------
      # ------------------------ assign start ------------------------
      weekday_dict = get_weekday_dict_function_v2()
      start_date_str = latest_test_dates_of_week_arr[weekday_dict[db_group_settings_dict['start_day']]].strftime('%m-%d-%Y')
      end_date_str = latest_test_dates_of_week_arr[weekday_dict[db_group_settings_dict['end_day']]].strftime('%m-%d-%Y')
      # ------------------------ assign end ------------------------
      start_timestamp_created = build_out_datetime_from_parts_function(start_date_str, db_group_settings_dict['start_time'], db_group_settings_dict['timezone'])
      end_timestamp_created = build_out_datetime_from_parts_function(end_date_str, db_group_settings_dict['end_time'], db_group_settings_dict['timezone'])    # converted to EST for job runs
      if end_timestamp_created <= start_timestamp_created:
        return 'false_end_time'
      # ------------------------ catch example: If my test is set to end on Thrusday's but for the newest test I log on Friday, the end would be yesterday start ------------------------
      current_datetime = datetime.now()
      if end_timestamp_created <= current_datetime:
        end_date_str_exception_1 = get_upcoming_date_function(db_group_settings_dict['end_day'], end_date_str)
        end_timestamp_created = build_out_datetime_from_parts_function(end_date_str_exception_1, db_group_settings_dict['end_time'], db_group_settings_dict['timezone'])    # converted to EST for job runs
      # ------------------------ catch example: If my test is set to end on Thrusday's but for the newest test I log on Friday, the end would be yesterday end ------------------------
    # ------------------------ pull question id's start ------------------------
    final_uuids_arr = []
    where_clause_str = None
    where_clause_arr = prepare_where_clause_function(db_group_settings_dict['categories'])
    where_clause_str = where_clause_arr[0]
    query_result_arr_of_dicts = select_general_function('select_all_questions_for_x_categories_v4', where_clause_str, db_group_settings_dict['total_questions'], db_group_settings_dict['fk_group_id'])
    for i in query_result_arr_of_dicts:
      final_uuids_arr.append(i['id'])
    remainder_questions_needed = db_group_settings_dict['total_questions'] - len(query_result_arr_of_dicts)
    if remainder_questions_needed > 0:
      # ------------------------ exclude wip id's start ------------------------
      exclude_where_clause = '/* AND id NOT IN () */'
      wip_question_ids_arr = []
      for i in query_result_arr_of_dicts:
        i_id = "'" + i['id'] + "'"
        wip_question_ids_arr.append(i_id)
      if len(wip_question_ids_arr) == 0:
        pass
      else:
        in_string = ','.join(wip_question_ids_arr)
        exclude_where_clause = 'AND id NOT IN (' + in_string + ')'
      # ------------------------ exclude wip id's end ------------------------
      # ------------------------ second pull if remainder start ------------------------
      query_result_arr_of_dicts_remainder = select_general_function('select_all_questions_for_x_categories_v5', remainder_questions_needed, db_group_settings_dict['fk_group_id'], exclude_where_clause)
      for i in query_result_arr_of_dicts_remainder:
        final_uuids_arr.append(i['id'])
      # ------------------------ second pull if remainder end ------------------------
    final_uuids_str = ','.join(final_uuids_arr)
    # ------------------------ pull question id's end ------------------------
    # ------------------------ question type order start ------------------------
    question_types_str = build_question_type_arr_function(db_group_settings_dict['question_type'], db_group_settings_dict['total_questions'])
    # ------------------------ question type order end ------------------------
    # ------------------------ insert to db start ------------------------
    new_test_id = create_uuid_function('test_')
    try:
      new_row = ActivityATestObj(
        id = new_test_id,
        created_timestamp = create_timestamp_function(),
        fk_group_id = db_group_settings_dict['fk_group_id'],
        timezone = db_group_settings_dict['timezone'],
        start_day = db_group_settings_dict['start_day'],
        start_time = db_group_settings_dict['start_time'],
        start_timestamp = start_timestamp_created,
        end_day = db_group_settings_dict['end_day'],
        end_time = db_group_settings_dict['end_time'],
        end_timestamp = end_timestamp_created,
        cadence = db_group_settings_dict['cadence'],
        total_questions = db_group_settings_dict['total_questions'],
        question_type = db_group_settings_dict['question_type'],
        categories = db_group_settings_dict['categories'],
        question_ids = final_uuids_str,
        question_types_order = question_types_str,
        status = 'Open',
        product = 'trivia'
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      pass
    # ------------------------ insert to db end ------------------------
    # ------------------------ insert to db start ------------------------
    for i in final_uuids_arr:
      try:
        new_row = ActivityAGroupQuestionsUsedObj(
          id = create_uuid_function('used_'),
          created_timestamp = create_timestamp_function(),
          fk_group_id = db_group_settings_dict['fk_group_id'],
          fk_question_id = i,
          fk_test_id = new_test_id,
          product = 'trivia'
        )
        db.session.add(new_row)
        db.session.commit()
      except:
        pass
    # ------------------------ insert to db end ------------------------
  # ------------------------ create quiz end ------------------------
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def create_activity_function(current_user, activity_code, activity_type, immediate=False):
  # ------------------------ Set Timezone START ------------------------
  # Set the timezone of the application when user creates account is will be in US/Easterm time
  os.environ['TZ'] = 'US/Eastern'
  time.tzset()
  # ------------------------ Set Timezone END ------------------------
  # ------------------------ pull group settings start ------------------------
  db_group_settings_obj = pull_create_activity_settings_obj_function(current_user, activity_code, activity_type)
  db_group_settings_dict = arr_of_dict_all_columns_single_item_function(db_group_settings_obj)
  # ------------------------ pull group settings end ------------------------
  # ------------------------ setup timeframe start ------------------------
  # ------------------------ if quiz to be made immediately (first quiz) start ------------------------
  if immediate == True:
    db_group_settings_dict['start_day'] = get_current_weekday_function()
    db_group_settings_dict['start_time'] = get_current_hour_function()  # will return current hour in EST
    # ------------------------ construct start/end timestamps start ------------------------
    start_date_str = get_upcoming_date_function(db_group_settings_dict['start_day'])
    end_date_str = get_upcoming_date_function(db_group_settings_dict['end_day'], start_date_str)
    start_timestamp_created = build_out_datetime_from_parts_function(start_date_str, db_group_settings_dict['start_time'], 'EST')
    end_timestamp_created = build_out_datetime_from_parts_function(end_date_str, db_group_settings_dict['end_time'], db_group_settings_dict['timezone'])    # converted to EST for job runs
    if end_timestamp_created <= start_timestamp_created:
      return 'false_end_time'
    # ------------------------ construct start/end timestamps end ------------------------
    # ------------------------ if quiz to be made immediately (first quiz) end ------------------------
  else:
    # ------------------------ get this weeks dates start ------------------------
    todays_date = date.today()
    latest_test_dates_of_week_arr = get_week_dates_function(todays_date)
    # ------------------------ get this weeks dates end ------------------------
    # ------------------------ assign start ------------------------
    weekday_dict = get_weekday_dict_function_v2()
    start_date_str = latest_test_dates_of_week_arr[weekday_dict[db_group_settings_dict['start_day']]].strftime('%m-%d-%Y')
    end_date_str = latest_test_dates_of_week_arr[weekday_dict[db_group_settings_dict['end_day']]].strftime('%m-%d-%Y')
    # ------------------------ assign end ------------------------
    start_timestamp_created = build_out_datetime_from_parts_function(start_date_str, db_group_settings_dict['start_time'], db_group_settings_dict['timezone'])
    end_timestamp_created = build_out_datetime_from_parts_function(end_date_str, db_group_settings_dict['end_time'], db_group_settings_dict['timezone'])    # converted to EST for job runs
    if end_timestamp_created <= start_timestamp_created:
      return 'false_end_time'
    # ------------------------ catch example: If my test is set to end on Thrusday's but for the newest test I log on Friday, the end would be yesterday start ------------------------
    current_datetime = datetime.now()
    if end_timestamp_created <= current_datetime:
      end_date_str_exception_1 = get_upcoming_date_function(db_group_settings_dict['end_day'], end_date_str)
      end_timestamp_created = build_out_datetime_from_parts_function(end_date_str_exception_1, db_group_settings_dict['end_time'], db_group_settings_dict['timezone'])    # converted to EST for job runs
    # ------------------------ catch example: If my test is set to end on Thrusday's but for the newest test I log on Friday, the end would be yesterday end ------------------------
  # ------------------------ setup timeframe end ------------------------
  # ------------------------ activity_type_a start ------------------------
  if activity_type == 'activity_type_a':
    # ------------------------ pull question id's start ------------------------
    final_uuids_arr = []
    where_clause_str = None
    where_clause_arr = prepare_where_clause_function(db_group_settings_dict['categories'])
    where_clause_str = where_clause_arr[0]
    query_result_arr_of_dicts = select_general_function('select_all_questions_for_x_categories_v6', where_clause_str, db_group_settings_dict['total_questions'], db_group_settings_dict['fk_group_id'], activity_code)
    for i in query_result_arr_of_dicts:
      final_uuids_arr.append(i['id'])
    remainder_questions_needed = db_group_settings_dict['total_questions'] - len(query_result_arr_of_dicts)
    if remainder_questions_needed > 0:
      # ------------------------ exclude wip id's start ------------------------
      exclude_where_clause = '/* AND id NOT IN () */'
      wip_question_ids_arr = []
      for i in query_result_arr_of_dicts:
        i_id = "'" + i['id'] + "'"
        wip_question_ids_arr.append(i_id)
      if len(wip_question_ids_arr) == 0:
        pass
      else:
        in_string = ','.join(wip_question_ids_arr)
        exclude_where_clause = 'AND id NOT IN (' + in_string + ')'
      # ------------------------ exclude wip id's end ------------------------
      # ------------------------ second pull if remainder start ------------------------
      query_result_arr_of_dicts_remainder = select_general_function('select_all_questions_for_x_categories_v7', remainder_questions_needed, db_group_settings_dict['fk_group_id'], exclude_where_clause, activity_code)
      for i in query_result_arr_of_dicts_remainder:
        final_uuids_arr.append(i['id'])
      # ------------------------ second pull if remainder end ------------------------
    final_uuids_str = ','.join(final_uuids_arr)
    # ------------------------ pull question id's end ------------------------
    # ------------------------ question type order start ------------------------
    question_types_str = build_question_type_arr_function(db_group_settings_dict['question_type'], db_group_settings_dict['total_questions'])
    # ------------------------ question type order end ------------------------
    # ------------------------ insert to db start ------------------------
    new_test_id = create_uuid_function('test_')
    try:
      new_row = ActivityATestObj(
        id = new_test_id,
        created_timestamp = create_timestamp_function(),
        fk_group_id = db_group_settings_dict['fk_group_id'],
        timezone = db_group_settings_dict['timezone'],
        start_day = db_group_settings_dict['start_day'],
        start_time = db_group_settings_dict['start_time'],
        start_timestamp = start_timestamp_created,
        end_day = db_group_settings_dict['end_day'],
        end_time = db_group_settings_dict['end_time'],
        end_timestamp = end_timestamp_created,
        cadence = db_group_settings_dict['cadence'],
        total_questions = db_group_settings_dict['total_questions'],
        question_type = db_group_settings_dict['question_type'],
        categories = db_group_settings_dict['categories'],
        question_ids = final_uuids_str,
        question_types_order = question_types_str,
        status = 'Open',
        product = activity_code
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      pass
    # ------------------------ insert to db end ------------------------
    # ------------------------ insert to db start ------------------------
    for i in final_uuids_arr:
      try:
        new_row = ActivityAGroupQuestionsUsedObj(
          id = create_uuid_function('used_'),
          created_timestamp = create_timestamp_function(),
          fk_group_id = db_group_settings_dict['fk_group_id'],
          fk_question_id = i,
          fk_test_id = new_test_id,
          product = activity_code
        )
        db.session.add(new_row)
        db.session.commit()
      except:
        pass
    # ------------------------ insert to db end ------------------------
  # ------------------------ activity_type_a end ------------------------
  # ------------------------ activity_type_b start ------------------------
  elif activity_type == 'activity_type_b':
    # ------------------------ get new question id start ------------------------
    query_result_arr_of_dicts = select_general_function('select_v7', activity_code, db_group_settings_dict['fk_group_id'])
    question_id = query_result_arr_of_dicts[0]['id']
    # ------------------------ get new question id end ------------------------
    # ------------------------ insert to db start ------------------------
    new_test_id = create_uuid_function('test_')
    try:
      new_row = ActivityBTestObj(
        id = new_test_id,
        created_timestamp = create_timestamp_function(),
        fk_group_id = db_group_settings_dict['fk_group_id'],
        timezone = db_group_settings_dict['timezone'],
        start_day = db_group_settings_dict['start_day'],
        start_time = db_group_settings_dict['start_time'],
        start_timestamp = start_timestamp_created,
        end_day = db_group_settings_dict['end_day'],
        end_time = db_group_settings_dict['end_time'],
        end_timestamp = end_timestamp_created,
        cadence = db_group_settings_dict['cadence'],
        fk_question_id = question_id,
        status = 'Open',
        product = activity_code
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      pass
    # ------------------------ insert to db end ------------------------
    # ------------------------ insert to db start ------------------------
    try:
      new_row = ActivityBGroupQuestionsUsedObj(
        id = create_uuid_function('used_'),
        created_timestamp = create_timestamp_function(),
        fk_group_id = db_group_settings_dict['fk_group_id'],
        fk_question_id = question_id,
        fk_test_id = new_test_id,
        product = activity_code
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      pass
    # ------------------------ insert to db end ------------------------
  # ------------------------ activity_type_b end ------------------------
  # ------------------------ create quiz end ------------------------
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def grade_quiz_function(ui_answer, url_test_id, total_questions, url_question_number, db_question_dict, current_user_id, public_group_id, url_activity_code):
  ui_answer_is_correct = False
  ui_answer_fitb_accuracy_score = 0
  # ------------------------ append to dict start ------------------------
  db_question_dict['question_number'] = url_question_number
  db_question_dict['ui_answer'] = ui_answer
  # ------------------------ append to dict end ------------------------
  question_type = db_question_dict['desired_question_type']
  # ------------------------ grade multiple choice start ------------------------
  if question_type == 'Multiple choice':
    acceptable_answer_arr = ['a', 'b', 'c', 'd', 'e']
    correct_answer = db_question_dict['answer']
    # ------------------------ loop answers arr for 1 letter start ------------------------
    if len(correct_answer) > 1:
      if ',' in correct_answer:
        correct_answer_arr = correct_answer.split(',')
        for i in correct_answer_arr:
          i = i.strip()
          if len(i) == 1:
            if i.lower() in acceptable_answer_arr:
              correct_answer = i
              break
    # ------------------------ loop answers arr for 1 letter end ------------------------
    # ------------------------ compare 1 letter start ------------------------
    if len(correct_answer) == 1:
      if correct_answer.lower() in acceptable_answer_arr:
        if correct_answer.lower() == ui_answer.lower():
          ui_answer_is_correct = True
          db_question_dict['ui_answer_fitb_accuracy_score'] = 0
        db_question_dict['ui_answer_fitb_accuracy_score'] = 0
    # ------------------------ compare 1 letter end ------------------------
  # ------------------------ grade multiple choice end ------------------------
  # ------------------------ grade fill in the blank start ------------------------
  if question_type == 'Fill in the blank':
    correct_answer = db_question_dict['answer']
    ui_answer = ui_answer.strip()
    # ------------------------ loop through answers arr start ------------------------
    if ',' in correct_answer:
      correct_answer_arr = correct_answer.split(',')
      for i in correct_answer_arr:
        i = i.strip()
        if len(i) > 1:    # avoid multiple choice answers here
          # ------------------------ test similarity start ------------------------
          answer_match_score = difflib.SequenceMatcher(None, i.lower(), ui_answer.lower()).ratio()*100
          if answer_match_score > 80:
            ui_answer_is_correct = True
            ui_answer_fitb_accuracy_score = answer_match_score
            db_question_dict['ui_answer_fitb_accuracy_score'] = ui_answer_fitb_accuracy_score
            break
          db_question_dict['ui_answer_fitb_accuracy_score'] = 0
          # ------------------------ test similarity end ------------------------
    # ------------------------ loop through answers arr end ------------------------
  # ------------------------ grade fill in the blank end ------------------------
  # ------------------------ append to dict start ------------------------
  db_question_dict['ui_answer_is_correct'] = ui_answer_is_correct
  db_question_arr_of_dict = []
  db_question_arr_of_dict.append(db_question_dict)
  # ------------------------ append to dict end ------------------------
  # ------------------------ pull/create grading obj start ------------------------
  db_test_grading_obj = ActivityATestGradedObj.query.filter_by(fk_test_id=url_test_id, fk_user_id=current_user_id,product=url_activity_code).first()
  if db_test_grading_obj == None or db_test_grading_obj == []:
    # ------------------------ insert to db start ------------------------
    new_test_id = create_uuid_function('testg_')
    try:
      new_row = ActivityATestGradedObj(
        id = new_test_id,
        created_timestamp = create_timestamp_function(),
        fk_group_id = public_group_id,
        fk_user_id = current_user_id,
        fk_test_id = url_test_id,
        total_questions = int(total_questions),
        correct_count = int(0),
        final_score = int(0),
        status = 'wip',
        graded_count = int(0),
        test_obj = json.dumps(db_question_arr_of_dict),
        product = url_activity_code
      )
      db.session.add(new_row)
      db.session.commit()
    except:
      pass
    # ------------------------ insert to db end ------------------------
    db_test_grading_obj = ActivityATestGradedObj.query.filter_by(fk_test_id=url_test_id, fk_user_id=current_user_id,product=url_activity_code).first()
  # ------------------------ pull/create grading obj end ------------------------
  # ------------------------ update master dict start ------------------------
  db_test_grading_dict = arr_of_dict_all_columns_single_item_function(db_test_grading_obj, for_json_dumps=True)
  master_test_tracking_arr_of_dict = json.loads(db_test_grading_dict['test_obj'])
  quesion_id_found = False
  quesion_id_found_index = 0
  for i in range(len(master_test_tracking_arr_of_dict)):
    if master_test_tracking_arr_of_dict[i]['id'] == db_question_dict['id']:
      quesion_id_found = True
      quesion_id_found_index = i
      break
  if quesion_id_found == True:
    master_test_tracking_arr_of_dict[quesion_id_found_index] = db_question_dict
  if quesion_id_found == False:
    master_test_tracking_arr_of_dict.append(db_question_dict)
  # ------------------------ update master dict end ------------------------
  # ------------------------ wip grading entire master dict start ------------------------
  wip_grading_total_correct_count = 0
  for i in master_test_tracking_arr_of_dict:
    if i['ui_answer_is_correct'] == True:
      wip_grading_total_correct_count += 1
  try:
    wip_grading_final_score = float(float(wip_grading_total_correct_count) / float(db_test_grading_dict['total_questions']))
  except:
    wip_grading_final_score = float(0)
  # ------------------------ wip grading entire master dict end ------------------------
  # ------------------------ update db start ------------------------
  db_test_grading_obj.correct_count = wip_grading_total_correct_count
  db_test_grading_obj.final_score = wip_grading_final_score
  db_test_grading_obj.graded_count = len(master_test_tracking_arr_of_dict)
  db_test_grading_obj.test_obj = json.dumps(master_test_tracking_arr_of_dict)
  if int(db_test_grading_obj.graded_count) == int(total_questions):
    db_test_grading_obj.status = 'complete'
    # ------------------------ email self start ------------------------
    try:
      db_user_obj = UserObj.query.filter_by(id=current_user_id).first()
      output_subject = f'Employees Test Graded | {db_user_obj.email} | {url_test_id}'
      db_email_sent_obj = EmailSentObj.query.filter_by(subject=output_subject).first()
      if db_email_sent_obj == None or db_email_sent_obj == []:
        output_to_email = os.environ.get('HR_SUPPORT_EMAIL')
        # ------------------------ get str of all answers start ------------------------
        all_user_answers_arr = []
        for i in range(len(master_test_tracking_arr_of_dict)):
          all_user_answers_arr.append(master_test_tracking_arr_of_dict[i]['ui_answer'])
        all_user_answers_str = ','.join(all_user_answers_arr)
        # ------------------------ get str of all answers end ------------------------
        output_body = f"<p>Hi there,</p>\
                        <p>{db_user_obj.email} completed their team's latest test.</p>\
                        <p>Answers on first submission: [{all_user_answers_str}]</p>\
                        <p>Score on first submission: [{wip_grading_final_score}]</p>\
                        <p style='margin:0;'>Best,</p>\
                        <p style='margin:0;'>HerdReviews Support Team</p>"
        send_email_template_function(output_to_email, output_subject, output_body)
        # ------------------------ insert email to db start ------------------------
        try:
          new_row_email = EmailSentObj(
            id = create_uuid_function('self_'),
            created_timestamp = create_timestamp_function(),
            from_user_id_fk = 'notifications',
            to_email = output_to_email,
            subject = output_subject,
            body = output_body
          )
          db.session.add(new_row_email)
        except:
          pass
        # ------------------------ insert email to db end ------------------------
      else:
        localhost_print_function('email already sent')
        pass
    except:
      pass
    # ------------------------ email self end ------------------------
  db.session.commit()
  # ------------------------ update db end ------------------------
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def pull_question_function(group_id, categories, url_activity_code):
  # ------------------------ pull based on categories start ------------------------
  where_clause_arr = prepare_where_clause_function(categories)
  query_result_arr_of_dicts = select_general_function('select_all_questions_for_x_categories_v4', where_clause_arr[0], 1, group_id, url_activity_code)
  # ------------------------ pull based on categories end ------------------------
  # ------------------------ pull any start ------------------------
  if query_result_arr_of_dicts == []:
    query_result_arr_of_dicts = select_general_function('select_v6', 1, group_id, url_activity_code)
  # ------------------------ pull any end ------------------------
  new_question_id = query_result_arr_of_dicts[0]['id']
  return new_question_id
# ------------------------ individual function end ------------------------