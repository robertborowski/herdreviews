# -------------------------------------------------------------- Imports
import psycopg2
from psycopg2 import Error
import os
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function

# -------------------------------------------------------------- Main Function
def postgres_connect_to_database_function():
  # Heroku Postgres connection
  DATABASE_URL = os.environ.get('HR_DB_URI')
  postgres_connection = psycopg2.connect(DATABASE_URL, sslmode='require')
  postgres_cursor = postgres_connection.cursor()
  return postgres_connection, postgres_cursor
  