# -------------------------------------------------------------- Imports
import redis
import os
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
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