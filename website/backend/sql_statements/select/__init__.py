# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website import db
from flask_login import current_user
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def select_general_function(tag_query_to_use, input1=None, input2=None, input3=None, input4=None):
  # ------------------------ select queries start ------------------------
  select_queries_dict = {
    'select_query_general_1': {
      'raw_query': f"SELECT \
                      * \
                    FROM \
                      polls_obj \
                    WHERE \
                      status_removed=False AND status_approved=True AND \
                      fk_show_id='{input1}' AND \
                      id NOT IN (SELECT DISTINCT fk_poll_id FROM polls_answered_obj WHERE fk_show_id='{input1}' AND fk_user_id='{input2}') \
                    ORDER BY \
                      created_timestamp DESC \
                    LIMIT 1;"
    },
    'select_query_general_1_anonymous': {
      'raw_query': f"SELECT \
                      * \
                    FROM \
                      polls_obj \
                    WHERE \
                      status_removed=False AND status_approved=True AND \
                      fk_show_id='{input1}' \
                    ORDER BY \
                      created_timestamp DESC \
                    LIMIT 1;"
    },
    'select_query_general_1_anonymous_random': {
      'raw_query': f"SELECT \
                      * \
                    FROM \
                      polls_obj \
                    WHERE \
                      status_removed=False AND status_approved=True AND \
                      fk_show_id='{input1}' \
                      AND id!='{input2}' \
                    ORDER BY \
                      RANDOM()LIMIT 1"
    },
    'select_query_general_2': {
      'raw_query': f"SELECT \
                      * \
                    FROM \
                      polls_obj \
                    WHERE \
                      status_removed=False AND (status_approved=True OR fk_user_id='{input3}') AND \
                      fk_show_id='{input1}' AND \
                      id='{input2}';"
    },
    'select_query_general_2_anonymous': {
      'raw_query': f"SELECT \
                      * \
                    FROM \
                      polls_obj \
                    WHERE \
                      status_removed=False AND status_approved=True AND \
                      fk_show_id='{input1}' AND \
                      id='{input2}';"
    },
    'select_query_general_3': {
      'raw_query': f"SELECT \
                      DISTINCT t1.fk_poll_id \
                    FROM \
                      polls_answered_obj AS t1 LEFT JOIN polls_obj AS t2 ON t1.fk_poll_id=t2.id \
                    WHERE \
                      t2.status_approved=True AND t2.status_removed=False AND \
                      t1.fk_show_id='{input1}' AND \
                      t1.fk_user_id='{input2}';"
    },
    'select_query_general_4': {
      'raw_query': f"WITH cte1 AS(SELECT ROW_NUMBER()OVER(PARTITION BY t1.fk_poll_id,t1.fk_user_id ORDER BY t1.created_timestamp DESC)AS row_num,t1.*FROM polls_answered_obj AS t1 LEFT JOIN polls_obj AS t2 ON t1.fk_poll_id=t2.id WHERE t1.fk_poll_id='{input1}' AND t2.status_approved=TRUE AND t2.status_removed=FALSE)SELECT*FROM cte1 WHERE row_num=1;"
    },
    'select_query_general_4_2': {
      'raw_query': f"WITH cte1 AS(SELECT ROW_NUMBER()OVER(PARTITION BY t1.fk_poll_id,t1.fk_user_id ORDER BY t1.created_timestamp DESC)AS row_num,t1.*FROM polls_answered_obj AS t1 LEFT JOIN polls_obj AS t2 ON t1.fk_poll_id=t2.id WHERE t1.fk_poll_id='{input1}' AND t2.status_approved=TRUE AND t2.status_removed=FALSE AND t1.fk_user_id IN('{input2}'))SELECT*FROM cte1 WHERE row_num=1;"
    },
    'select_query_general_5': {
      'raw_query': f"SELECT p.*,s.name,s.platform_image_small,s.platform_image_medium,s.platform_image_large FROM polls_obj AS p LEFT JOIN shows_obj AS s ON p.fk_show_id=s.id WHERE p.fk_user_id='{input1}' ORDER BY p.fk_show_id, p.created_timestamp DESC;"
    },
    'select_query_general_6': {
      'raw_query': f"WITH cte1 AS(SELECT ROW_NUMBER()OVER(PARTITION BY t1.fk_poll_id,t1.fk_user_id ORDER BY t1.created_timestamp DESC)AS row_num,t1.*FROM polls_answered_obj AS t1 LEFT JOIN polls_obj AS t2 ON t1.fk_poll_id=t2.id WHERE t1.fk_poll_id='{input1}' AND t2.status_approved=TRUE AND t2.status_removed=FALSE)SELECT *FROM cte1 WHERE row_num=1 AND cte1.poll_answer_submitted!='Skip this question' AND cte1.fk_user_id IN (SELECT fk_user_id FROM polls_answered_obj WHERE fk_poll_id='{input2}');"
    },
    'select_query_general_7': {
      'raw_query': f"SELECT*FROM shows_obj WHERE id!='show_user_attributes' ORDER BY RANDOM()LIMIT 1;"
    },
    'select_query_general_8': {
      'raw_query': f"SELECT*FROM shows_obj WHERE id!='show_user_attributes' ORDER BY RANDOM();"
    }
  }
  # ------------------------ select queries end ------------------------
  # ------------------------ general query start ------------------------
  result_obj = db.session.execute(select_queries_dict[tag_query_to_use]['raw_query'])
  # ------------------------ general query end ------------------------
  # ------------------------ existing result start ------------------------
  result_arr_of_dicts = []
  for i_row in result_obj:
    result_dict = dict(i_row) # convert to dict keyed by column names
    result_arr_of_dicts.append(result_dict)
  # ------------------------ existing result end ------------------------
  return result_arr_of_dicts
# ------------------------ individual function end ------------------------