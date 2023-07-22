# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.models import UserAttributesObj, PollsAnsweredObj
from website.backend.sql_statements.select import select_general_function
from website.backend.get_create_obj import get_age_demographics_function, get_age_group_function, get_starting_arr_function
import pprint
from website.backend.dates import user_years_old_at_timestamp_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def get_percent_data_function(input_numerator, input_denominator):
  result = 0
  try:
    result = float(float(float(input_numerator)/float(input_denominator)) * float(100))
  except:
    pass
  return int(result)
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def get_chart_data_function(page_dict, total_answered_arr_of_dict, current_user):
  # ------------------------ chart general start ------------------------
  for i_dict in page_dict['poll_statistics_dict']['chart_arr_of_dict']:
    # ------------------------ check if current user provided attribute poll response start ------------------------
    if i_dict['user_provided_attribute_x'] != 'ignore':
      db_poll_answered_obj = PollsAnsweredObj.query.filter_by(fk_user_id=current_user.id,fk_show_id=i_dict['fk_show_id'],fk_poll_id=i_dict['fk_poll_id']).order_by(PollsAnsweredObj.created_timestamp.desc()).first()
      if db_poll_answered_obj == None or db_poll_answered_obj == []:
        i_dict['user_provided_attribute_x'] = None
      else:
        if db_poll_answered_obj.poll_answer_submitted == 'Skip this question':
          i_dict['user_provided_attribute_x'] = None
        else:
          i_dict['user_provided_attribute_x'] = True
    # ------------------------ check if current user provided attribute poll response end ------------------------
    # ------------------------ set count to zero for options start ------------------------
    # answer choices only
    if i_dict['chart_name'] == 'chart_distribution_answer_choice':
      for k,v in page_dict['poll_dict']['answer_choices_dict'].items():
        if v != 'Skip this question':
          page_dict['poll_statistics_dict'][i_dict['vote_count_by_x_dict']][k] = 0
    # generation only
    elif i_dict['chart_name'] == 'chart_distribution_generation':
      year_generation_dict, generation_options_arr = get_age_demographics_function()
      for i in generation_options_arr:
        page_dict['poll_statistics_dict'][i_dict['vote_count_by_x_dict']][i] = 0
    else:
      # all user attribute checks
      for i in i_dict['starting_point_arr']:
        page_dict['poll_statistics_dict'][i_dict['vote_count_by_x_dict']][i] = 0
    # ------------------------ set count to zero for options end ------------------------
    # ------------------------ loop for count start ------------------------
    # answer choices only
    if i_dict['chart_name'] == 'chart_distribution_answer_choice':
      for i_poll_answered_dict in total_answered_arr_of_dict:
        i_poll_answer_submitted = i_poll_answered_dict['poll_answer_submitted']
        for k,v in page_dict['poll_dict']['answer_choices_dict'].items():
          if i_poll_answer_submitted == v:
            try:
              page_dict['poll_statistics_dict'][i_dict['vote_count_by_x_dict']][k] += 1
            except:
              pass
    # generation only
    elif i_dict['chart_name'] == 'chart_distribution_generation':
      for i_user in page_dict['poll_statistics_dict']['all_user_ids_participated']:
        try:
          db_user_obj = UserAttributesObj.query.filter_by(fk_user_id=i_user,attribute_code='attribute_birthday').first()
          user_generation = year_generation_dict[str(db_user_obj.attribute_year)]
          page_dict['poll_statistics_dict'][i_dict['vote_count_by_x_dict']][user_generation] += 1
        except:
          pass
    # age group only
    elif i_dict['chart_name'] == 'chart_distribution_age_group':
      for i_poll_answered_dict in total_answered_arr_of_dict:
        i_poll_answer_submitted_timestamp = i_poll_answered_dict['created_timestamp']
        db_user_obj = UserAttributesObj.query.filter_by(fk_user_id=i_poll_answered_dict['fk_user_id'],attribute_code='attribute_birthday').first()
        age_at_submission = user_years_old_at_timestamp_function(i_poll_answer_submitted_timestamp, int(db_user_obj.attribute_year), int(db_user_obj.attribute_month), int(db_user_obj.attribute_day))
        if age_at_submission <= 29:
          page_dict['poll_statistics_dict'][i_dict['vote_count_by_x_dict']]["18-20's"] += 1
        elif age_at_submission >= 30 and age_at_submission <= 39:
          page_dict['poll_statistics_dict'][i_dict['vote_count_by_x_dict']]["30's"] += 1
        elif age_at_submission >= 40 and age_at_submission <= 49:
          page_dict['poll_statistics_dict'][i_dict['vote_count_by_x_dict']]["40's"] += 1
        elif age_at_submission >= 50 and age_at_submission <= 59:
          page_dict['poll_statistics_dict'][i_dict['vote_count_by_x_dict']]["50's"] += 1
        elif age_at_submission >= 60:
          page_dict['poll_statistics_dict'][i_dict['vote_count_by_x_dict']]["60's +"] += 1
    else:
      # all user attribute checks
      total_answered_arr_of_dict = select_general_function('select_query_general_6', i_dict['fk_poll_id'], page_dict['url_poll_id'])
      for i_poll_answered_dict in total_answered_arr_of_dict:
        i_poll_answer_submitted = i_poll_answered_dict['poll_answer_submitted']
        page_dict['poll_statistics_dict'][i_dict['vote_count_by_x_dict']][i_poll_answer_submitted] += 1
    # ------------------------ loop for count end ------------------------
    # ------------------------ loop for percent start ------------------------
    for k, v in page_dict['poll_statistics_dict'][i_dict['vote_count_by_x_dict']].items():
      result = get_percent_data_function(v, len(total_answered_arr_of_dict))
      page_dict['poll_statistics_dict'][i_dict['vote_percent_by_x_dict']][k] = result
    # ------------------------ loop for percent end ------------------------
    # ------------------------ chart variables start ------------------------
    for k,v in page_dict['poll_statistics_dict'][i_dict['vote_percent_by_x_dict']].items():
      if i_dict['chart_name'] == 'chart_distribution_generation' and k == 'Silent':
        continue
      label = k
      if len(label) > 15:
        label = label[0:15]+'...'
      page_dict['poll_statistics_dict'][i_dict['chart_name']]['labels'].append(label)
      page_dict['poll_statistics_dict'][i_dict['chart_name']]['values'].append(v)
    # ------------------------ chart variables end ------------------------
  # ------------------------ chart general end ------------------------
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------

# ------------------------ individual function start ------------------------
def get_poll_statistics_function(current_user, page_dict):
  # ------------------------ pull variables start ------------------------
  poll_id = page_dict['url_poll_id']
  show_id = page_dict['url_show_id']
  # ------------------------ pull variables end ------------------------
  # ------------------------ set variables start ------------------------
  page_dict['poll_statistics_dict'] = {}
  # total answered
  page_dict['poll_statistics_dict']['total_latest_poll_answers'] = 0
  # users participated
  page_dict['poll_statistics_dict']['all_user_ids_participated'] = []
  charts_arr = ['answer_choice','generation','age_group','gender','annual_income','relationship_status','education','employment','collar','ethnicity','politics','own_vs_rent','industry']
  for i in charts_arr:
    if i!='answer_choice' and i!='generation' and i!='age_group':
      page_dict['poll_statistics_dict']['user_provided_attribute_'+i] = None
    page_dict['poll_statistics_dict']['vote_count_dict_'+i] = {}
    page_dict['poll_statistics_dict']['vote_percent_dict_'+i] = {}
    page_dict['poll_statistics_dict']['chart_distribution_'+i] = {}
    page_dict['poll_statistics_dict']['chart_distribution_'+i]['labels'] = []
    page_dict['poll_statistics_dict']['chart_distribution_'+i]['values'] = []
  # ------------------------ set variables page_dict end ------------------------
  # ------------------------ set variables for charts start ------------------------
  chart_arr_of_dict = [
    {
      'unique_id':'id-chart_distribution_answer_choice',
      'js_variables_arr':['chart_distribution_title_answer_choice','chart_distribution_labels_answer_choice','chart_distribution_values_answer_choice'],
      'chart_attribute':'Answer choices',
      'chart_name':'chart_distribution_answer_choice',
      'chart_title':page_dict['db_show_dict']['name_title']+' | Answer (%) | HerdReviews.com',
      'fk_show_id':show_id,
      'fk_poll_id':poll_id,
      'user_provided_attribute_x':'ignore',
      'starting_point_arr':None,
      'vote_count_by_x_dict':'vote_count_dict_answer_choice',
      'vote_percent_by_x_dict':'vote_percent_dict_answer_choice'
    },
    {
      'unique_id':'id-chart_distribution_generation',
      'js_variables_arr':['chart_distribution_title_generation','chart_distribution_labels_generation','chart_distribution_values_generation'],
      'chart_attribute':'Generation',
      'chart_name':'chart_distribution_generation',
      'chart_title':page_dict['db_show_dict']['name_title']+' | Generation (%) | HerdReviews.com',
      'fk_show_id':show_id,
      'fk_poll_id':poll_id,
      'user_provided_attribute_x':'ignore',
      'starting_point_arr':None,
      'vote_count_by_x_dict':'vote_count_dict_generation',
      'vote_percent_by_x_dict':'vote_percent_dict_generation'
    },
    {
      'unique_id':'id-chart_distribution_age_group',
      'js_variables_arr':['chart_distribution_title_age_group','chart_distribution_labels_age_group','chart_distribution_values_age_group'],
      'chart_attribute':'Age group',
      'chart_name':'chart_distribution_age_group',
      'chart_title':page_dict['db_show_dict']['name_title']+' | Age group (%) | HerdReviews.com',
      'fk_show_id':show_id,
      'fk_poll_id':poll_id,
      'user_provided_attribute_x':'ignore',
      'starting_point_arr':get_age_group_function(),
      'vote_count_by_x_dict':'vote_count_dict_age_group',
      'vote_percent_by_x_dict':'vote_percent_dict_age_group'
    },
    {
      'unique_id':'id-chart_distribution_gender',
      'js_variables_arr':['chart_distribution_title_gender','chart_distribution_labels_gender','chart_distribution_values_gender'],
      'chart_attribute':'Gender',
      'chart_name':'chart_distribution_gender',
      'chart_title':page_dict['db_show_dict']['name_title']+' | Gender (%) | HerdReviews.com',
      'fk_show_id':'show_user_attributes',
      'fk_poll_id':'poll_user_attribute_gender',
      'user_provided_attribute_x':None,
      'starting_point_arr':get_starting_arr_function('poll_user_attribute_gender'),
      'vote_count_by_x_dict':'vote_count_dict_gender',
      'vote_percent_by_x_dict':'vote_percent_dict_gender'
    },
    {
      'unique_id':'id-chart_distribution_annual_income',
      'js_variables_arr':['chart_distribution_title_annual_income','chart_distribution_labels_annual_income','chart_distribution_values_annual_income'],
      'chart_attribute':'Annual income',
      'chart_name':'chart_distribution_annual_income',
      'chart_title':page_dict['db_show_dict']['name_title']+' | Annual income (%) | HerdReviews.com',
      'fk_show_id':'show_user_attributes',
      'fk_poll_id':'poll_user_attribute_annual_income',
      'user_provided_attribute_x':None,
      'starting_point_arr':get_starting_arr_function('poll_user_attribute_annual_income'),
      'vote_count_by_x_dict':'vote_count_dict_annual_income',
      'vote_percent_by_x_dict':'vote_percent_dict_annual_income'
    },
    {
      'unique_id':'id-chart_distribution_relationship_status',
      'js_variables_arr':['chart_distribution_title_relationship_status','chart_distribution_labels_relationship_status','chart_distribution_values_relationship_status'],
      'chart_attribute':'Relationship status',
      'chart_name':'chart_distribution_relationship_status',
      'chart_title':page_dict['db_show_dict']['name_title']+' | Relationship status (%) | HerdReviews.com',
      'fk_show_id':'show_user_attributes',
      'fk_poll_id':'poll_user_attribute_relationship_status',
      'user_provided_attribute_x':None,
      'starting_point_arr':get_starting_arr_function('poll_user_attribute_relationship_status'),
      'vote_count_by_x_dict':'vote_count_dict_relationship_status',
      'vote_percent_by_x_dict':'vote_percent_dict_relationship_status'
    },
    {
      'unique_id':'id-chart_distribution_education',
      'js_variables_arr':['chart_distribution_title_education','chart_distribution_labels_education','chart_distribution_values_education'],
      'chart_attribute':'Education',
      'chart_name':'chart_distribution_education',
      'chart_title':page_dict['db_show_dict']['name_title']+' | Education (%) | HerdReviews.com',
      'fk_show_id':'show_user_attributes',
      'fk_poll_id':'poll_user_attribute_education',
      'user_provided_attribute_x':None,
      'starting_point_arr':get_starting_arr_function('poll_user_attribute_education'),
      'vote_count_by_x_dict':'vote_count_dict_education',
      'vote_percent_by_x_dict':'vote_percent_dict_education'
    },
    {
      'unique_id':'id-chart_distribution_employment',
      'js_variables_arr':['chart_distribution_title_employment','chart_distribution_labels_employment','chart_distribution_values_employment'],
      'chart_attribute':'Employment',
      'chart_name':'chart_distribution_employment',
      'chart_title':page_dict['db_show_dict']['name_title']+' | Employment (%) | HerdReviews.com',
      'fk_show_id':'show_user_attributes',
      'fk_poll_id':'poll_user_attribute_employment',
      'user_provided_attribute_x':None,
      'starting_point_arr':get_starting_arr_function('poll_user_attribute_employment'),
      'vote_count_by_x_dict':'vote_count_dict_employment',
      'vote_percent_by_x_dict':'vote_percent_dict_employment'
    },
    {
      'unique_id':'id-chart_distribution_collar',
      'js_variables_arr':['chart_distribution_title_collar','chart_distribution_labels_collar','chart_distribution_values_collar'],
      'chart_attribute':'Job type',
      'chart_name':'chart_distribution_collar',
      'chart_title':page_dict['db_show_dict']['name_title']+' | Job type (%) | HerdReviews.com',
      'fk_show_id':'show_user_attributes',
      'fk_poll_id':'poll_user_attribute_collar',
      'user_provided_attribute_x':None,
      'starting_point_arr':get_starting_arr_function('poll_user_attribute_collar'),
      'vote_count_by_x_dict':'vote_count_dict_collar',
      'vote_percent_by_x_dict':'vote_percent_dict_collar'
    },
    {
      'unique_id':'id-chart_distribution_ethnicity',
      'js_variables_arr':['chart_distribution_title_ethnicity','chart_distribution_labels_ethnicity','chart_distribution_values_ethnicity'],
      'chart_attribute':'Ethnicity',
      'chart_name':'chart_distribution_ethnicity',
      'chart_title':page_dict['db_show_dict']['name_title']+' | Ethnicity (%) | HerdReviews.com',
      'fk_show_id':'show_user_attributes',
      'fk_poll_id':'poll_user_attribute_ethnicity',
      'user_provided_attribute_x':None,
      'starting_point_arr':get_starting_arr_function('poll_user_attribute_ethnicity'),
      'vote_count_by_x_dict':'vote_count_dict_ethnicity',
      'vote_percent_by_x_dict':'vote_percent_dict_ethnicity'
    },
    {
      'unique_id':'id-chart_distribution_politics',
      'js_variables_arr':['chart_distribution_title_politics','chart_distribution_labels_politics','chart_distribution_values_politics'],
      'chart_attribute':'Political affiliation',
      'chart_name':'chart_distribution_politics',
      'chart_title':page_dict['db_show_dict']['name_title']+' | Political affiliation (%) | HerdReviews.com',
      'fk_show_id':'show_user_attributes',
      'fk_poll_id':'poll_user_attribute_politics',
      'user_provided_attribute_x':None,
      'starting_point_arr':get_starting_arr_function('poll_user_attribute_politics'),
      'vote_count_by_x_dict':'vote_count_dict_politics',
      'vote_percent_by_x_dict':'vote_percent_dict_politics'
    },
    {
      'unique_id':'id-chart_distribution_own_vs_rent',
      'js_variables_arr':['chart_distribution_title_own_vs_rent','chart_distribution_labels_own_vs_rent','chart_distribution_values_own_vs_rent'],
      'chart_attribute':'Living space',
      'chart_name':'chart_distribution_own_vs_rent',
      'chart_title':page_dict['db_show_dict']['name_title']+' | Living space (%) | HerdReviews.com',
      'fk_show_id':'show_user_attributes',
      'fk_poll_id':'poll_user_attribute_own_vs_rent',
      'user_provided_attribute_x':None,
      'starting_point_arr':get_starting_arr_function('poll_user_attribute_own_vs_rent'),
      'vote_count_by_x_dict':'vote_count_dict_own_vs_rent',
      'vote_percent_by_x_dict':'vote_percent_dict_own_vs_rent'
    },
    {
      'unique_id':'id-chart_distribution_industry',
      'js_variables_arr':['chart_distribution_title_industry','chart_distribution_labels_industry','chart_distribution_values_industry'],
      'chart_attribute':'Occupation/Industry',
      'chart_name':'chart_distribution_industry',
      'chart_title':page_dict['db_show_dict']['name_title']+' | Occupation/Industry (%) | HerdReviews.com',
      'fk_show_id':'show_user_attributes',
      'fk_poll_id':'poll_user_attribute_industry',
      'user_provided_attribute_x':None,
      'starting_point_arr':get_starting_arr_function('poll_user_attribute_industry'),
      'vote_count_by_x_dict':'vote_count_dict_industry',
      'vote_percent_by_x_dict':'vote_percent_dict_industry'
    }
  ]
  page_dict['poll_statistics_dict']['chart_arr_of_dict'] = chart_arr_of_dict
  # ------------------------ set variables for charts end ------------------------
  # ------------------------ get total answered start ------------------------
  total_answered_arr_of_dict = select_general_function('select_query_general_4', poll_id)
  try:
    page_dict['poll_statistics_dict']['total_latest_poll_answers'] = int(len(total_answered_arr_of_dict))
  except:
    pass
  # ------------------------ get total answered end ------------------------
  # ------------------------ get all user id's that voted start ------------------------
  for i_poll_answered_dict in total_answered_arr_of_dict:
    page_dict['poll_statistics_dict']['all_user_ids_participated'].append(i_poll_answered_dict['fk_user_id'])
  # ------------------------ get all user id's that voted end ------------------------
  # ------------------------ get chart data start ------------------------
  page_dict = get_chart_data_function(page_dict, total_answered_arr_of_dict, current_user)
  # ------------------------ get chart data end ------------------------
  localhost_print_function(' ------------- 50 ------------- ')
  localhost_print_function(pprint.pformat(page_dict, indent=2))
  localhost_print_function(' ------------- 50 ------------- ')
  return page_dict
# ------------------------ individual function end ------------------------