
# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import redis
import os
from flask import request
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def redis_connect_to_database_function():
  try:
    """
    # Connecting to Redis non-pool
    redis_connection = redis.Redis(
      host = os.environ.get('HR_REDIS_HOST_NAME'),
      port = str(os.environ.get('HR_REDIS_PORT')),
      password = os.environ.get('HR_REDIS_PASSWORD'))
    """
    # Connecting to Redis pool method
    pool = redis.ConnectionPool(
      host = os.environ.get('HR_REDIS_HOST_NAME'),
      port = str(os.environ.get('HR_REDIS_PORT')),
      password = os.environ.get('HR_REDIS_PASSWORD'),
      db=0)
    #redis_connection = redis.Redis(connection_pool=pool)
    redis_connection = redis.StrictRedis(connection_pool=pool)
  except:
    localhost_print_function('redis connection failed!')
    return 'redis connection failed!'
  # Return the connection
  return redis_connection
# ------------------------ individual function end ------------------------


# ------------------------ individual function start ------------------------
def redis_check_if_cookie_exists_function():
  try:
    get_cookie_value_from_browser = request.cookies.get('user_candidates_browser_cookie')
  except:
    get_cookie_value_from_browser = None
  return get_cookie_value_from_browser
# ------------------------ individual function start ------------------------

# ------------------------ individual function start ------------------------
def redis_check_if_employees_cookie_exists_function():
  try:
    get_cookie_value_from_browser = request.cookies.get('user_employees_browser_cookie')
  except:
    get_cookie_value_from_browser = None
  return get_cookie_value_from_browser
# ------------------------ individual function start ------------------------

# ------------------------ individual function start ------------------------
def redis_set_browser_cookie_function():
  set_browser_cookie_key = 'user_candidates_browser_cookie'
  set_browser_cookie_value = create_uuid_function('bcooke_')
  return set_browser_cookie_key, set_browser_cookie_value
# ------------------------ individual function start ------------------------

# ------------------------ individual function start ------------------------
def redis_set_employees_browser_cookie_function():
  set_browser_cookie_key = 'user_employees_browser_cookie'
  set_browser_cookie_value = create_uuid_function('b2cooke_')
  return set_browser_cookie_key, set_browser_cookie_value
# ------------------------ individual function start ------------------------