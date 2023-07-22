# -------------------------------------------------------------- Imports
from datetime import datetime
import os, time

# -------------------------------------------------------------- Main
def create_timestamp_function():
  os.environ['TZ'] = 'US/Eastern'
  time.tzset()
  return datetime.now().strftime('%Y-%m-%d %H:%M:%S')