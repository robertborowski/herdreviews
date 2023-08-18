# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.backend.sql_statements.select import select_general_function
from website.backend.get_create_obj import get_starting_arr_function, get_alphabet_arr_function, default_chart_colors_function, get_percent_mins_dict_function, rgb_to_hex_function
import pprint
from website.models import PollsObj, PollsStandInObj, ShowsAttributesObj, PollsAnsweredObj
from website import db
import random
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
import json
from website.backend.dict_manipulation import get_answers_shortened_v2_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def create_fake_redistribution_function(page_dict, current_choices_arr, vote_distribution_dict, limits_dict):
  # ------------------------ set variables start ------------------------
  ignore_redistribution_arr = []
  ignore_redistribution_dict = {}
  remainder_value_per_choice = float(0)
  total_value_to_redistribute = float(0)
  # ------------------------ set variables end ------------------------
  # ------------------------ loop through to force reassign and get total remainder start ------------------------
  for k_answer,v_dict in limits_dict.items():
    try:
      max_value = float(v_dict[page_dict['url_show_id']])
      for i in range(len(current_choices_arr)):
        if current_choices_arr[i] == k_answer:
          ignore_redistribution_arr.append(current_choices_arr[i])
          ignore_redistribution_dict[current_choices_arr[i]] = max_value
          if float(vote_distribution_dict[current_choices_arr[i]]) <= max_value:
            pass
          else:
            remainder_value = float(float(vote_distribution_dict[current_choices_arr[i]]) - float(max_value))
            total_value_to_redistribute += remainder_value
    except Exception as e:
      pass
  # ------------------------ loop through to force reassign and get total remainder end ------------------------
  # ------------------------ reassign variables start ------------------------
  remainder_total_options = len(current_choices_arr) - len(ignore_redistribution_arr)
  remainder_value_per_choice = float(float(total_value_to_redistribute) / float(remainder_total_options))
  # ------------------------ reassign variables end ------------------------
  # ------------------------ apply remainders to non forced variables start ------------------------
  for k,v in vote_distribution_dict.items():
    if k in ignore_redistribution_arr:
      try:
        vote_distribution_dict[k] = ignore_redistribution_dict[k]
      except:
        pass
    else:
      try:
        vote_distribution_dict[k] = round(float(float(v) + float(remainder_value_per_choice)),4)
      except:
        pass
  # ------------------------ apply remainders to non forced variables end ------------------------
  return vote_distribution_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def create_fake_count_stats_function(page_dict, stat_name, col_name, exception_v1_trues_falses_nones=False):
  min_votes_limit = page_dict['poll_statistics_v2_dict']['min_votes_limit']
  # ------------------------ get from db start ------------------------
  vote_distribution_dict = {}
  search_key = stat_name + '~' + col_name + '~' + 'percent_dict'
  db_standin_obj = PollsStandInObj.query.filter_by(fk_show_id=page_dict['url_show_id'],fk_poll_id=page_dict['url_poll_id'],standin_key=search_key).order_by(PollsStandInObj.created_timestamp.desc()).first()
  # ------------------------ get from db end ------------------------
  # ------------------------ not yet created start ------------------------
  if db_standin_obj == None or db_standin_obj == []:
    # ------------------------ first pre insert matchup/assign random start ------------------------
    current_choices_arr = page_dict['poll_statistics_v2_dict'][stat_name]['choices_arr']
    # ------------------------ exception 1 start ------------------------
    if exception_v1_trues_falses_nones == True:
      current_choices_arr = ['falses','nones','trues']
    # ------------------------ exception 1 end ------------------------
    # ------------------------ randomize array start ------------------------
    percentages_arr = [0] * len(current_choices_arr)
    remaining_percentage = float(100.0)
    for i in range(len(current_choices_arr) - 1):
      max_percent = float(min(40.0, remaining_percentage - (len(current_choices_arr) - i - 1)))
      percentages_arr[i] = float(random.uniform(0, max_percent))
      remaining_percentage = float(remaining_percentage - percentages_arr[i])
    percentages_arr[-1] = float(remaining_percentage)
    random.shuffle(percentages_arr)
    # ------------------------ randomize array end ------------------------  
    # ------------------------ format fake array to decimal/percents start ------------------------
    for i in range(len(current_choices_arr)):
      vote_distribution_dict[current_choices_arr[i]] = round(float(float(percentages_arr[i])/float(100)),4)
    # ------------------------ format fake array to decimal/percents end ------------------------
    # ------------------------ first pre insert matchup/assign random end ------------------------
    # ------------------------ redistribute percentages - general start ------------------------
    limits_dict = get_percent_mins_dict_function(page_dict['url_show_id'])
    vote_distribution_dict = create_fake_redistribution_function(page_dict, current_choices_arr, vote_distribution_dict, limits_dict)
    # ------------------------ redistribute percentages - general end ------------------------
    # ------------------------ insert to db start ------------------------
    try:
      new_row = PollsStandInObj(
        id = create_uuid_function('standin_'),
        created_timestamp = create_timestamp_function(),
        fk_show_id = page_dict['url_show_id'],
        fk_poll_id = page_dict['url_poll_id'],
        standin_key = search_key,
        standin_values = json.dumps(vote_distribution_dict)
      )
      db.session.add(new_row)
      db.session.commit()
    except Exception as e:
      pass
    # ------------------------ insert to db end ------------------------
  # ------------------------ not yet created end ------------------------
  # ------------------------ yes created start ------------------------
  else:
    vote_distribution_dict = json.loads(db_standin_obj.standin_values)
    pass
  # ------------------------ yes created end ------------------------
  # ------------------------ assign/map the percentages to the counts start ------------------------
  for k, v in page_dict['poll_statistics_v2_dict'][stat_name][col_name+'_dict']['count_dict'].items():
    page_dict['poll_statistics_v2_dict'][stat_name][col_name+'_dict']['count_dict'][k] = int(float(vote_distribution_dict[k]) * float(min_votes_limit))
  # ------------------------ assign/map the percentages to the counts end ------------------------
  # ------------------------ update dict variables start ------------------------
  page_dict['poll_statistics_v2_dict'][stat_name]['all_response_objs_len'] += min_votes_limit
  # ------------------------ update dict variables end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_count_and_percent_stats_function(page_dict, stat_name, choices_arr, col_name, exception_v1_trues_falses_nones=False, passed_current_user_obj=None):
  objs_arr_of_dicts = page_dict['poll_statistics_v2_dict'][stat_name]['all_response_objs']
  total_participation = int(page_dict['poll_statistics_v2_dict'][stat_name]['all_response_objs_len'])
  # ------------------------ set count to 0 for all options start ------------------------
  page_dict['poll_statistics_v2_dict'][stat_name][col_name+'_dict'] = {}
  page_dict['poll_statistics_v2_dict'][stat_name][col_name+'_dict']['count_dict'] = {}
  page_dict['poll_statistics_v2_dict'][stat_name][col_name+'_dict']['percent_dict'] = {}
  for i in choices_arr:
    page_dict['poll_statistics_v2_dict'][stat_name][col_name+'_dict']['count_dict'][i] = 0
    page_dict['poll_statistics_v2_dict'][stat_name][col_name+'_dict']['percent_dict'][i] = 0
  # ------------------------ set count to 0 for all options end ------------------------
  # ------------------------ get real count start ------------------------
  for i_dict in objs_arr_of_dicts:
    try:
      page_dict['poll_statistics_v2_dict'][stat_name][col_name+'_dict']['count_dict'][i_dict[col_name]] += 1
    except:
      pass
  # ------------------------ get real count end ------------------------
  # ------------------------ get fake count if needed start ------------------------
  min_votes_limit = 0
  if passed_current_user_obj.is_anonymous == True:
    min_votes_limit = 106
  page_dict['poll_statistics_v2_dict']['min_votes_limit'] = min_votes_limit
  if total_participation < min_votes_limit:
    page_dict = create_fake_count_stats_function(page_dict, stat_name, col_name, exception_v1_trues_falses_nones)
  # ------------------------ get fake count if needed end ------------------------
  # ------------------------ get percents start ------------------------
  for k,v in page_dict['poll_statistics_v2_dict'][stat_name][col_name+'_dict']['count_dict'].items():
    try:
      if total_participation < min_votes_limit:
        page_dict['poll_statistics_v2_dict'][stat_name][col_name+'_dict']['percent_dict'][k] = str(round(float(float(v) / float(min_votes_limit)) * float(100),2))+'%'
      else:
        page_dict['poll_statistics_v2_dict'][stat_name][col_name+'_dict']['percent_dict'][k] = str(round(float(float(v) / float(total_participation)) * float(100),2))+'%'
    except:
      pass
  # ------------------------ get percents end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_create_show_chart_colors_function(page_dict):
  end_dict =  {}
  fk_show_id = page_dict['url_show_id']
  db_show_attributes_obj_primary = ShowsAttributesObj.query.filter_by(fk_show_id=fk_show_id,attribute_key='show_color_primary').order_by(ShowsAttributesObj.created_timestamp.desc()).first()
  db_show_attributes_obj_secondary = ShowsAttributesObj.query.filter_by(fk_show_id=fk_show_id,attribute_key='show_color_secondary').order_by(ShowsAttributesObj.created_timestamp.desc()).first()
  # ------------------------ if missing start ------------------------
  if db_show_attributes_obj_primary == None or db_show_attributes_obj_primary == [] or db_show_attributes_obj_secondary == None or db_show_attributes_obj_secondary == []:
    # ------------------------ get random color set from list start ------------------------
    colors_arr = default_chart_colors_function()
    # ------------------------ get random color set from list end ------------------------
    # ------------------------ insert to db start ------------------------
    try:
      new_row = ShowsAttributesObj(
        id = create_uuid_function('s-att_'),
        created_timestamp = create_timestamp_function(),
        fk_show_id = fk_show_id,
        attribute_key = 'show_color_primary',
        attribute_value = colors_arr[0],
        attribute_note = colors_arr[2]
      )
      db.session.add(new_row)
      db.session.commit()
    except Exception as e:
      pass
    # ------------------------ insert to db end ------------------------
    # ------------------------ insert to db start ------------------------
    try:
      new_row = ShowsAttributesObj(
        id = create_uuid_function('s-att_'),
        created_timestamp = create_timestamp_function(),
        fk_show_id = fk_show_id,
        attribute_key = 'show_color_secondary',
        attribute_value = colors_arr[1],
        attribute_note = colors_arr[3]
      )
      db.session.add(new_row)
      db.session.commit()
    except Exception as e:
      pass
    # ------------------------ insert to db end ------------------------
    db_show_attributes_obj_primary = ShowsAttributesObj.query.filter_by(fk_show_id=fk_show_id,attribute_key='show_color_primary').order_by(ShowsAttributesObj.created_timestamp.desc()).first()
    db_show_attributes_obj_secondary = ShowsAttributesObj.query.filter_by(fk_show_id=fk_show_id,attribute_key='show_color_secondary').order_by(ShowsAttributesObj.created_timestamp.desc()).first()
  # ------------------------ if missing end ------------------------
  else:
    pass
  end_dict['show_color_primary'] = db_show_attributes_obj_primary.attribute_value
  end_dict['show_color_secondary'] = db_show_attributes_obj_secondary.attribute_value
  # ------------------------ convert rgb to hex start ------------------------
  end_dict['show_color_primary_to_hex'] = rgb_to_hex_function(end_dict['show_color_primary'])
  # ------------------------ convert rgb to hex end ------------------------
  # ------------------------ defaults start ------------------------
  db_words_faded_obj = ShowsAttributesObj.query.filter_by(fk_show_id='admin_default',attribute_key='text_faded').order_by(ShowsAttributesObj.created_timestamp.desc()).first()
  db_words_correct_obj = ShowsAttributesObj.query.filter_by(fk_show_id='admin_default',attribute_key='text_correct').order_by(ShowsAttributesObj.created_timestamp.desc()).first()
  end_dict['text_faded'] = db_words_faded_obj.attribute_value
  end_dict['text_correct'] = db_words_correct_obj.attribute_value
  # ------------------------ defaults end ------------------------
  return end_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_chart_title_function(stat_name, show_name_title, title_type):
  chart_title = ''
  if title_type == 'normal':
    chart_title = stat_name
    chart_title = chart_title.replace('_', ' ')
    chart_title = chart_title.title()
    chart_title = chart_title + ' | ' + show_name_title + ' listeners'
  if title_type == 'short':
    chart_title = stat_name
    chart_title = chart_title.replace('_', ' ')
    chart_title = chart_title.title()
  return chart_title
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_chart_info_function(page_dict, stat_name, passed_current_user_obj):
  # ------------------------ set variables start ------------------------
  page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict'] = {}
  db_answered_obj = {}
  # ------------------------ check if answered feedback start ------------------------
  if stat_name == 'feedback':
    if passed_current_user_obj.is_anonymous == True:
      db_answered_obj = None
    else:
      db_answered_obj = PollsAnsweredObj.query.filter_by(fk_show_id=page_dict['url_show_id'],fk_poll_id=page_dict['url_poll_id'],fk_user_id=passed_current_user_obj.id).order_by(PollsAnsweredObj.created_timestamp.desc()).first()
  # ------------------------ check if answered feedback end ------------------------
  # ------------------------ check if answered attritbutes start ------------------------
  else:
    if passed_current_user_obj.is_anonymous == True:
      db_answered_obj = None
    else:
      db_answered_obj = PollsAnsweredObj.query.filter_by(fk_show_id='show_user_attributes',fk_poll_id='poll_user_attribute_'+stat_name,fk_user_id=passed_current_user_obj.id).order_by(PollsAnsweredObj.created_timestamp.desc()).first()
  if db_answered_obj == None or db_answered_obj == []:
    if passed_current_user_obj.is_anonymous == True:
      pass
    else:
      page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['status'] = 'invisible'
      page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['id'] = 'id-none-001'
      return page_dict
  # ------------------------ check if answered attritbutes end ------------------------
  page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['status'] = 'visible'
  page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['id'] = 'id-chart_' + stat_name
  page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['title'] = get_chart_title_function(stat_name, page_dict['db_show_dict']['name_title'], 'normal')
  page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['title_short'] = get_chart_title_function(stat_name, page_dict['db_show_dict']['name_title'], 'short')
  page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['js_dict'] = {}
  page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['js_dict']['labels_arr'] = []
  page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['js_dict']['values_arr'] = []
  page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['js_dict']['chart_colors_arr'] = []
  page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['js_dict']['text_colors_arr'] = []
  # ------------------------ set variables end ------------------------
  # ------------------------ start ------------------------
  js_dict = {}
  for k,v in page_dict['poll_statistics_v2_dict'][stat_name]['choices_dict'].items():
    label_string = k + ' | ' + page_dict['poll_statistics_v2_dict'][stat_name]['poll_answer_submitted_dict']['percent_dict'][v] + ' | ' + str(page_dict['poll_statistics_v2_dict'][stat_name]['poll_answer_submitted_dict']['count_dict'][v]) + ' |'
    page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['js_dict']['labels_arr'].append(label_string)
    page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['js_dict']['values_arr'].append(page_dict['poll_statistics_v2_dict'][stat_name]['poll_answer_submitted_dict']['count_dict'][v])
  # ------------------------ end ------------------------
  # ------------------------ assign chart colors based on max start ------------------------
  max_value = max(page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['js_dict']['values_arr'])
  for i in range(len(page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['js_dict']['values_arr'])):
    if int(page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['js_dict']['values_arr'][i]) == int(max_value):
      page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['js_dict']['chart_colors_arr'].append(page_dict['show_colors_dict']['show_color_primary'])
      page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['js_dict']['text_colors_arr'].append(page_dict['show_colors_dict']['text_correct'])
    else:
      page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['js_dict']['chart_colors_arr'].append(page_dict['show_colors_dict']['show_color_secondary'])
      page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['js_dict']['text_colors_arr'].append(page_dict['show_colors_dict']['text_faded'])
  # ------------------------ assign chart colors based on max end ------------------------
  # ------------------------ chart height for js start ------------------------
  page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['change_chart_size_to'] = 75 * len(page_dict['poll_statistics_v2_dict'][stat_name]['chart_dict']['js_dict']['labels_arr'])
  # ------------------------ chart height for js end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_poll_statistics_v2_function(page_dict, passed_current_user_obj):
  # ------------------------ set variables start ------------------------
  page_dict['poll_statistics_v2_dict'] = {}
  page_dict['poll_statistics_v2_dict']['define_dict'] = {
    # k: v, | 'gender': 'poll_user_attribute_gender'
    'feedback': page_dict['url_poll_id'],
  }
  page_dict['poll_statistics_v2_dict']['user_ids_only'] = []
  page_dict['poll_statistics_v2_dict']['user_ids_str_only'] = ''
  # ------------------------ set variables end ------------------------
  # ------------------------ get all variable names start ------------------------
  db_polls_objs = PollsObj.query.filter_by(fk_show_id='show_user_attributes',status_approved=True,status_removed=False).order_by(PollsObj.id.asc()).all()
  for i_obj in db_polls_objs:
    id = i_obj.id
    name = id.replace('poll_user_attribute_','')
    page_dict['poll_statistics_v2_dict']['define_dict'][name] = id
  # ------------------------ get all variable names end ------------------------
  # ------------------------ define dict arr start ------------------------
  page_dict['poll_statistics_v2_dict']['define_dict_arr'] = []
  for k,v in page_dict['poll_statistics_v2_dict']['define_dict'].items():
    page_dict['poll_statistics_v2_dict']['define_dict_arr'].append(k)
  # ------------------------ define dict arr end ------------------------
  # ------------------------ get user responses start ------------------------
  for k,v in page_dict['poll_statistics_v2_dict']['define_dict'].items():
    page_dict['poll_statistics_v2_dict'][k] = {}
    if k == 'feedback':
      page_dict['poll_statistics_v2_dict'][k]['all_response_objs'] = select_general_function('select_query_general_4', v)
      # ------------------------ get user ids only start ------------------------
      for i_dict in page_dict['poll_statistics_v2_dict'][k]['all_response_objs']:
        page_dict['poll_statistics_v2_dict']['user_ids_only'].append(i_dict['fk_user_id'])
      page_dict['poll_statistics_v2_dict']['user_ids_str_only'] = "','".join(page_dict['poll_statistics_v2_dict']['user_ids_only'])
      # ------------------------ get user ids only end ------------------------
    if k != 'feedback':
      page_dict['poll_statistics_v2_dict'][k]['all_response_objs'] = select_general_function('select_query_general_4_2', v, page_dict['poll_statistics_v2_dict']['user_ids_str_only'])
    # ------------------------ get user responses end ------------------------
    # ------------------------ total user responses start ------------------------
    page_dict['poll_statistics_v2_dict'][k]['all_response_objs_len'] = len(page_dict['poll_statistics_v2_dict'][k]['all_response_objs'])
    # ------------------------ total user responses end ------------------------
    # ------------------------ set starting arrays start ------------------------
    page_dict['poll_statistics_v2_dict'][k]['choices_arr'] = get_starting_arr_function(v)
    page_dict['poll_statistics_v2_dict'][k]['choices_dict'] = get_answers_shortened_v2_function(page_dict['poll_statistics_v2_dict'][k]['choices_arr'])
    # ------------------------ set starting arrays end ------------------------
    # ------------------------ get counts and percentages for poll start ------------------------
    # answer submitted column
    page_dict = get_count_and_percent_stats_function(page_dict, k, page_dict['poll_statistics_v2_dict'][k]['choices_arr'], 'poll_answer_submitted', False, passed_current_user_obj)
    # trues falses nones columns exception_v1
    col_names_arr = ['poll_vote_updown_feedback', 'poll_vote_updown_question', 'status_answer_anonymous']
    temp_starting_arr = ['trues','falses','nones']
    for i in col_names_arr:
      page_dict = get_count_and_percent_stats_function(page_dict, k, temp_starting_arr, i, True, passed_current_user_obj)
    # ------------------------ get counts and percentages for poll end ------------------------
    # ------------------------ presentation names start ------------------------
    proper_case = k.replace('_',' ')
    proper_case = proper_case[0].upper() + proper_case[1:]
    page_dict['poll_statistics_v2_dict'][k]['name_proper_case'] = proper_case
    # ------------------------ presentation names end ------------------------
    # ------------------------ chart information start ------------------------
    page_dict = get_chart_info_function(page_dict, k, passed_current_user_obj)
    # ------------------------ chart information end ------------------------
  # localhost_print_function(' ------------- 50 ------------- ')
  # localhost_print_function(pprint.pformat(page_dict, indent=2))
  # localhost_print_function(' ------------- 50 ------------- ')
  return page_dict
# ------------------------ individual function end ------------------------