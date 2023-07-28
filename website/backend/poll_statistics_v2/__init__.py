# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.models import UserAttributesObj, PollsAnsweredObj, PollsStandInObj
from website import db
from website.backend.sql_statements.select import select_general_function
from website.backend.get_create_obj import get_age_demographics_function, get_age_group_function, get_starting_arr_function
import pprint
from website.backend.dates import user_years_old_at_timestamp_function
import random
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
import json
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def total_upvote_downvote_function(page_dict, k):
  # ------------------------ set variables start ------------------------
  page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict'] = {}
  page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict']['count_dict'] = {}
  page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict']['count_dict']['upvotes'] = 0
  page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict']['count_dict']['downvotes'] = 0
  page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict']['count_dict']['no_votes'] = 0
  page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict']['percent_dict'] = {}
  page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict']['percent_dict']['upvotes'] = 0
  page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict']['percent_dict']['downvotes'] = 0
  page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict']['percent_dict']['no_votes'] = 0
  # ------------------------ set variables end ------------------------
  # ------------------------ get upvote downvote counts start ------------------------
  for i_dict in page_dict['poll_statistics_v2_dict'][k]['all_response_objs']:
    if i_dict['poll_vote_updown_question'] == True:
      page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict']['count_dict']['upvotes'] += 1
    elif i_dict['poll_vote_updown_question'] == False:
      page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict']['count_dict']['downvotes'] += 1
    else:
      page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict']['count_dict']['no_votes'] += 1
  # ------------------------ get upvote downvote counts end ------------------------
  # ------------------------ get upvote downvote percents start ------------------------
  for k2,v2 in page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict']['count_dict'].items():
    if k2 == 'upvotes':
      page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict']['percent_dict']['upvotes'] = str(float(float(v2) / float(len(page_dict['poll_statistics_v2_dict'][k]['all_response_objs']))) * float(100))+'%'
    if k2 == 'downvotes':
      page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict']['percent_dict']['downvotes'] = str(float(float(v2) / float(len(page_dict['poll_statistics_v2_dict'][k]['all_response_objs']))) * float(100))+'%'
    if k2 == 'no_votes':
      page_dict['poll_statistics_v2_dict'][k]['upvote_downvote_dict']['percent_dict']['no_votes'] = str(float(float(v2) / float(len(page_dict['poll_statistics_v2_dict'][k]['all_response_objs']))) * float(100))+'%'
  # ------------------------ get upvote downvote percents end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_count_and_percent_stats_function(page_dict, k, choices_arr, objs_arr_of_dicts, total_denominator):
  # ------------------------ loop through submitted answers to get answer choice distribution start ------------------------
  # set count and percent to 0
  page_dict['poll_statistics_v2_dict'][k][k+'_votes_dict'] = {}
  page_dict['poll_statistics_v2_dict'][k][k+'_votes_dict']['count_dict'] = {}
  page_dict['poll_statistics_v2_dict'][k][k+'_votes_dict']['percent_dict'] = {}
  for i in choices_arr:
    page_dict['poll_statistics_v2_dict'][k][k+'_votes_dict']['count_dict'][i] = 0
    page_dict['poll_statistics_v2_dict'][k][k+'_votes_dict']['percent_dict'][i] = 0
  # loop + update count
  for i_dict in objs_arr_of_dicts:
    try:
      page_dict['poll_statistics_v2_dict'][k][k+'_votes_dict']['count_dict'][i_dict['poll_answer_submitted']] += 1
    except:
      pass
  # loop + update percents
  for k,v in page_dict['poll_statistics_v2_dict'][k][k+'_votes_dict']['count_dict'].items():
    try:
      page_dict['poll_statistics_v2_dict'][k][k+'_votes_dict']['percent_dict'][k] = str(float(float(v) / float(total_denominator)) * float(100))+'%'
    except:
      pass
  # ------------------------ loop through submitted answers to get answer choice distribution end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_poll_statistics_v2_function(current_user, page_dict):
  # ------------------------ set variables start ------------------------
  page_dict['poll_statistics_v2_dict'] = {}
  page_dict['poll_statistics_v2_dict']['define_dict'] = {
    # k: v, | 'name': 'poll_id',
    'feedback': page_dict['url_poll_id'],
    'gender': 'poll_user_attribute_gender'
  }
  page_dict['poll_statistics_v2_dict']['user_ids_only'] = []
  page_dict['poll_statistics_v2_dict']['user_ids_str_only'] = ''
  # ------------------------ set variables end ------------------------
  for k,v in page_dict['poll_statistics_v2_dict']['define_dict'].items():
    page_dict['poll_statistics_v2_dict'][k] = {}
    if k == 'feedback':
      page_dict['poll_statistics_v2_dict'][k]['all_response_objs'] = select_general_function('select_query_general_4', v)
      page_dict = total_upvote_downvote_function(page_dict, k)
      # ------------------------ get total people that answered poll user ids only start ------------------------
      for i_dict in page_dict['poll_statistics_v2_dict'][k]['all_response_objs']:
        page_dict['poll_statistics_v2_dict']['user_ids_only'].append(i_dict['fk_user_id'])
      page_dict['poll_statistics_v2_dict']['user_ids_str_only'] = "','".join(page_dict['poll_statistics_v2_dict']['user_ids_only'])
      # ------------------------ get total people that answered poll user ids only end ------------------------
    if k != 'feedback':
      page_dict['poll_statistics_v2_dict'][k]['all_response_objs'] = select_general_function('select_query_general_4_2', v, page_dict['poll_statistics_v2_dict']['user_ids_str_only'])
      page_dict = total_upvote_downvote_function(page_dict, k)
    # ------------------------ set starting arrays start ------------------------
    page_dict['poll_statistics_v2_dict'][k]['choices_arr'] = get_starting_arr_function(v)
    # ------------------------ set starting arrays end ------------------------
    # ------------------------ get counts and percentages start ------------------------
    page_dict = get_count_and_percent_stats_function(page_dict, k, page_dict['poll_statistics_v2_dict'][k]['choices_arr'], page_dict['poll_statistics_v2_dict'][k]['all_response_objs'], len(page_dict['poll_statistics_v2_dict'][k]['all_response_objs']))
    # ------------------------ get counts and percentages end ------------------------
  localhost_print_function(' ------------- 50 ------------- ')
  localhost_print_function(pprint.pformat(page_dict, indent=2))
  localhost_print_function(' ------------- 50 ------------- ')
  return page_dict
# ------------------------ individual function end ------------------------