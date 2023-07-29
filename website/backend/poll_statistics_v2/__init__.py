# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.backend.sql_statements.select import select_general_function
from website.backend.get_create_obj import get_starting_arr_function
import pprint
from website.models import PollsObj
from website import db
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def arr_to_shortened_dict_function(page_dict, stat_name):
  # ------------------------ set starting arrays start ------------------------
  choices_arr = page_dict['poll_statistics_v2_dict'][stat_name]['choices_arr']
  page_dict['poll_statistics_v2_dict'][stat_name]['choices_dict'] = {}
  for i in choices_arr:
    i_short = i
    if len(i_short) > 10:
      i_short = i_short[:10] + '...'
    page_dict['poll_statistics_v2_dict'][stat_name]['choices_dict'][i_short] = i
  # ------------------------ set starting arrays end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def create_fake_count_stats_function(page_dict, stat_name, choices_arr, col_name):
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_count_and_percent_stats_function(page_dict, stat_name, choices_arr, col_name):
  objs_arr_of_dicts = page_dict['poll_statistics_v2_dict'][stat_name]['all_response_objs']
  total_denominator = len(objs_arr_of_dicts)
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
  # min_votes_limit = 100
  # page_dict['poll_statistics_v2_dict']['min_votes_limit'] = min_votes_limit
  # if total_denominator < min_votes_limit:
  #   page_dict = create_fake_count_stats_function(page_dict, stat_name, choices_arr, col_name)
  # ------------------------ get fake count if needed end ------------------------
  # ------------------------ get percents start ------------------------
  for k,v in page_dict['poll_statistics_v2_dict'][stat_name][col_name+'_dict']['count_dict'].items():
    try:
      page_dict['poll_statistics_v2_dict'][stat_name][col_name+'_dict']['percent_dict'][k] = str(float(float(v) / float(total_denominator)) * float(100))+'%'
    except:
      pass
  # ------------------------ get percents end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_poll_statistics_v2_function(page_dict):
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
  db_polls_objs = PollsObj.query.filter_by(fk_show_id='show_user_attributes').order_by(PollsObj.created_timestamp.asc()).all()
  for i_obj in db_polls_objs:
    id = i_obj.id
    name = id.replace('poll_user_attribute_','')
    page_dict['poll_statistics_v2_dict']['define_dict'][name] = id
  # ------------------------ get all variable names end ------------------------
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
    page_dict = arr_to_shortened_dict_function(page_dict, k)
    # ------------------------ set starting arrays end ------------------------
    # ------------------------ get counts and percentages for poll start ------------------------
    # answer submitted column
    page_dict = get_count_and_percent_stats_function(page_dict, k, page_dict['poll_statistics_v2_dict'][k]['choices_arr'], 'poll_answer_submitted')
    # trues falses nones columns
    col_names_arr = ['poll_vote_updown_question', 'poll_vote_updown_feedback', 'status_answer_anonymous']
    temp_starting_arr = ['trues','falses','nones']
    for i in col_names_arr:
      page_dict = get_count_and_percent_stats_function(page_dict, k, temp_starting_arr, i)
    # ------------------------ get counts and percentages for poll end ------------------------
  localhost_print_function(' ------------- 50 ------------- ')
  localhost_print_function(pprint.pformat(page_dict, indent=2))
  localhost_print_function(' ------------- 50 ------------- ')
  return page_dict
# ------------------------ individual function end ------------------------