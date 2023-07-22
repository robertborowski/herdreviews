# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website import db
from flask_login import current_user
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def select_general_function(tag_query_to_use, additional_input=None, additional_input2=None, additional_input3=None, additional_input4=None):
  try:
    current_user_id_defined_var = current_user.id
  except:
    current_user_id_defined_var = None
  # ------------------------ select queries start ------------------------
  select_queries_dict = {
    'select_specific_assessment_questions_v2': {
      'raw_query': f"SELECT \
                      id, categories, question, title, aws_image_url, answer, option_a, option_b, option_c, option_d \
                    FROM \
                      activity_a_created_questions_obj \
                    WHERE \
                      id IN ({additional_input}) \
                    ORDER BY \
                      created_timestamp;",
      'input_args': {}
    },
    'select_specific_assessment_questions_v3': {
      'raw_query': f"SELECT \
                      id, categories, question, title, aws_image_url, answer, option_a, option_b, option_c, option_d, option_e \
                    FROM \
                      activity_a_created_questions_obj \
                    WHERE \
                      id = {additional_input};",
      'input_args': {}
    },
    'select_all_capacity_options': {
      'raw_query': 'SELECT id FROM candidates_capacity_options_obj',
      'input_args': {}
    },
    'select_all_capacity_options_employees': {
      'raw_query': 'SELECT id FROM stripe_payment_options_obj',
      'input_args': {}
    },
    'select_if_desired_languages_captured': {
      'raw_query': 'SELECT desired_languages FROM candidates_desired_languages_obj WHERE user_id_fk = :val ORDER BY created_timestamp DESC',
      'input_args': {'val': current_user_id_defined_var}
    },
    'select_all_candidate_categories_chosen_v2': {
      'raw_query': "SELECT DISTINCT q.categories FROM activity_a_created_questions_obj AS q WHERE q.status=TRUE AND q.product='candidates' ORDER BY q.categories;",
      'input_args': {}
    },
    'select_all_employees_categories_v1': {
      'raw_query': "SELECT DISTINCT q.categories FROM activity_a_created_questions_obj AS q WHERE q.status=TRUE AND q.product NOT LIKE 'candidates' AND q.categories IS NOT NULL ORDER BY q.categories;",
      'input_args': {}
    },
    'select_all_questions_for_x_categories_v2': {
      'raw_query': f"SELECT \
                      id, categories, question, title, aws_image_url, answer, option_a, option_b, option_c, option_d, option_e \
                    FROM \
                      activity_a_created_questions_obj \
                    WHERE \
                      status = TRUE AND product='candidates' \
                      AND ({additional_input}) \
                    ORDER BY \
                      RANDOM();",
      'input_args': {}
    },
    'select_all_questions_for_x_categories_v3': {
      'raw_query': f"SELECT \
                      id \
                    FROM \
                      activity_a_created_questions_obj \
                    WHERE \
                      status = TRUE AND product='candidates' \
                      AND ({additional_input}) \
                    ORDER BY \
                      RANDOM() \
                    LIMIT 10;",
      'input_args': {}
    },
    'select_all_questions_for_x_categories_v4': {
      'raw_query': f"SELECT \
                      id \
                    FROM \
                      activity_a_created_questions_obj \
                    WHERE \
                      status = TRUE AND product LIKE '%{additional_input4}%' \
                      AND ({additional_input}) \
                      AND id NOT IN (SELECT fk_question_id FROM activity_a_group_questions_used_obj WHERE fk_group_id='{additional_input3}') \
                    ORDER BY \
                      RANDOM() \
                    LIMIT {additional_input2};",
      'input_args': {}
    },
    'select_all_questions_for_x_categories_v5': {
      'raw_query': f"SELECT \
                      id \
                    FROM \
                      activity_a_created_questions_obj \
                    WHERE \
                      status = TRUE AND product='trivia' \
                      AND id NOT IN (SELECT fk_question_id FROM activity_a_group_questions_used_obj WHERE fk_group_id='{additional_input2}') {additional_input3} \
                    ORDER BY \
                      RANDOM() \
                    LIMIT {additional_input};",
      'input_args': {}
    },
    'select_all_questions_for_x_categories_v6': {
      'raw_query': f"SELECT \
                      id \
                    FROM \
                      activity_a_created_questions_obj \
                    WHERE \
                      status = TRUE AND product LIKE '%{additional_input4}%' \
                      AND ({additional_input}) \
                      AND id NOT IN (SELECT fk_question_id FROM activity_a_group_questions_used_obj WHERE product='{additional_input4}' AND fk_group_id='{additional_input3}') \
                    ORDER BY \
                      RANDOM() \
                    LIMIT {additional_input2};",
      'input_args': {}
    },
    'select_all_questions_for_x_categories_v7': {
      'raw_query': f"SELECT \
                      id \
                    FROM \
                      activity_a_created_questions_obj \
                    WHERE \
                      status = TRUE AND product LIKE '%{additional_input4}%' \
                      AND id NOT IN (SELECT fk_question_id FROM activity_a_group_questions_used_obj WHERE product='{additional_input4}' AND fk_group_id='{additional_input2}') {additional_input3} \
                    ORDER BY \
                      RANDOM() \
                    LIMIT {additional_input};",
      'input_args': {}
    },
    'select_v6': {
      'raw_query': f"SELECT \
                      id \
                    FROM \
                      activity_a_created_questions_obj \
                    WHERE \
                      status = TRUE AND product LIKE '%{additional_input3}%' \
                      AND id NOT IN (SELECT fk_question_id FROM activity_a_group_questions_used_obj WHERE fk_group_id='{additional_input2}') \
                    ORDER BY \
                      RANDOM() \
                    LIMIT {additional_input};",
      'input_args': {}
    },
    'select_v7': {
      'raw_query': f"SELECT \
                      id \
                    FROM \
                      activity_b_created_questions_obj \
                    WHERE \
                      status = TRUE AND product LIKE '%{additional_input}%' \
                      AND id NOT IN (SELECT fk_question_id FROM activity_b_group_questions_used_obj WHERE fk_group_id='{additional_input2}') \
                    ORDER BY \
                      RANDOM() \
                    LIMIT 1;",
      'input_args': {}
    },
    'select_one_question_for_x_categories_v1': {
      'raw_query': f"SELECT \
                      id \
                    FROM \
                      activity_a_created_questions_obj \
                    WHERE \
                      status = TRUE AND product='candidates' \
                      AND ({additional_input}) \
                      AND id NOT IN ({additional_input2})\
                    ORDER BY \
                      RANDOM() \
                    LIMIT 1;",
      'input_args': {}
    },
    'select_question_id_actually_exists_v2': {
      'raw_query': "SELECT id FROM activity_a_created_questions_obj WHERE id=:val;",
      'input_args': {'val': additional_input}
    },
    'select_sample_trivia': {
      'raw_query': f"SELECT \
                      * \
                    FROM \
                      activity_a_created_questions_obj \
                    WHERE \
                      status=TRUE \
                      AND product='trivia' \
                    ORDER BY \
                      created_timestamp DESC \
                    LIMIT 5;",
      'input_args': {}
    },
    'select_sample_trivia2': {
      'raw_query': f"SELECT \
                      * \
                    FROM \
                      activity_a_created_questions_obj \
                    WHERE \
                      status=TRUE \
                      AND product='trivia' \
                      AND id IN ('questionid_50536b69-dca5-4576-9963-955d47b57d55','questionid_c1410845-325f-4fa9-bb0c-32643e89c7a6','questionid_c28d1b3a-db3d-4f13-ac01-d5a8537b92c2','questionid_305b16ca-5ca3-4b94-8fef-b83d824bd429','questionid_cf424ccc-0363-4575-ad38-3760c13727da');",
      'input_args': {}
    },
    'select_sample_picture_quiz': {
      'raw_query': f"SELECT \
                      * \
                    FROM \
                      activity_a_created_questions_obj \
                    WHERE \
                      status = TRUE \
                      AND product LIKE '%picture_quiz%' \
                    ORDER BY \
                      created_timestamp DESC \
                    LIMIT 5;",
      'input_args': {}
    },
    'select_sample_icebreakers': {
      'raw_query': f"SELECT \
                      * \
                    FROM \
                      activity_b_created_questions_obj \
                    WHERE \
                      status = TRUE \
                      AND product LIKE '%icebreakers%' \
                    ORDER BY \
                      RANDOM() \
                    LIMIT 1;",
      'input_args': {}
    },
    'select_celebrations_v1': {
      'raw_query': f"SELECT \
                      * \
                    FROM \
                      user_celebrate_obj \
                    WHERE \
                      fk_user_id IN ({additional_input}) \
                      AND celebrate_month = {additional_input2} \
                      AND celebrate_day = {additional_input3} \
                    ORDER BY \
                      fk_user_id;",
      'input_args': {}
    },
    'select_upcoming_celebrations_v2': {
      'raw_query': f"SELECT \
                      * \
                    FROM \
                      user_celebrate_obj \
                    WHERE \
                      fk_user_id IN ({additional_input}) \
                    ORDER BY \
                      fk_user_id;",
      'input_args': {}
    }
  }
  # ------------------------ select queries end ------------------------
  # ------------------------ general query start ------------------------
  # result_obj = db.session.execute('SELECT * FROM user_obj WHERE email = :val', {'val': 'a@a.com'})
  result_obj = db.session.execute(select_queries_dict[tag_query_to_use]['raw_query'], select_queries_dict[tag_query_to_use]['input_args'])
  # ------------------------ general query end ------------------------
  # ------------------------ default result start ------------------------
  result_arr_of_dicts = []
  # ------------------------ default result end ------------------------
  # ------------------------ existing result start ------------------------
  for i_row in result_obj:
    # result_dict = dict(i_row.items()) # convert to dict keyed by column names
    result_dict = dict(i_row) # convert to dict keyed by column names
    result_arr_of_dicts.append(result_dict)
  # ------------------------ existing result end ------------------------
  return result_arr_of_dicts
# ------------------------ individual function end ------------------------