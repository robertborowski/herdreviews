# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import os, time
from datetime import datetime, timedelta, date
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
# ------------------------ imports end ------------------------

# ------------------------ set timezone start ------------------------
# Set the timezone of the application when user creates account is will be in US/Easterm time
os.environ['TZ'] = 'US/Eastern'
time.tzset()
# ------------------------ set timezone end ------------------------

# ------------------------ individual function start ------------------------
def get_years_from_date_function(input_year, input_month, input_day):
  start_date = date(int(input_year), int(input_month), int(input_day))
  todays_date = date.today()
  year_difference = float((todays_date - start_date).days // 365)
  return year_difference
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def return_ints_from_str_function(input_str):
  try:
    arr = input_str.split(' / ')
    month = int(arr[0])
    day = int(arr[1])
    year = int(arr[2])
  except:
    return False, False, False
  return year, month, day
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def user_years_old_at_timestamp_function(timestamp_submitted, user_birth_year, user_birth_month, user_birth_day):
  # timestamp_submitted > type: <class 'datetime.datetime'>
  # user_birth_year, user_birth_month, user_birth_day > type: <class 'int'>
  birth_date = date(int(user_birth_year), int(user_birth_month), int(user_birth_day))
  submitted_date = timestamp_submitted.date()
  year_difference = int(float((submitted_date - birth_date).days // 365))
  return year_difference
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def unix_timestamp_to_est_function(unix_timestamp):
    # Convert Unix timestamp to a datetime object
    utc_datetime = datetime.utcfromtimestamp(unix_timestamp)
    # Create a timezone object for EST
    est_timezone = utc_datetime + timedelta(hours=-4)
    return est_timezone
# ------------------------ individual function end ------------------------