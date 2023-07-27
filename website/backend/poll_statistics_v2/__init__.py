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
def get_poll_statistics_v2_function(current_user, page_dict):
  localhost_print_function(' ------------- 50 ------------- ')
  localhost_print_function(pprint.pformat(page_dict, indent=2))
  localhost_print_function(' ------------- 50 ------------- ')
  return page_dict
# ------------------------ individual function end ------------------------