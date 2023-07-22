# ------------------------ imports start ------------------------
from website import create_app_function
import os
# ------------------------ imports end ------------------------

# ------------------------ app start ------------------------
app = create_app_function()
# ------------------------ app end ------------------------

# =========================================================================================================== Run app
# ------------------------ call app directly start ------------------------
if __name__ == '__main__':
  # ------------------------ additional configs start ------------------------
  # Check environment variable that was passed in from user on the command line, assume false
  server_env = os.environ.get('TESTING', 'false')
  # ------------------------ Running on localhost START ------------------------
  if server_env and server_env == 'true':
    print('RUNNING ON LOCALHOST')
    app.run(debug = True, host='0.0.0.0', port=80, use_reloader=False)
  # ------------------------ Running on localhost END ------------------------
  # ------------------------ Running on heroku server START ------------------------
  else:
    # port and run for Heroku
    print('RUNNING ON PRODUCTION')
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)
  # ------------------------ Running on heroku server END ------------------------
  # ------------------------ additional configs end ------------------------
# ------------------------ call app directly end ------------------------