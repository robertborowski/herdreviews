# ------------------------ imports start ------------------------
import requests
import os
# ------------------------ imports end ------------------------

# os.environ.get('REDDIT_USERNAME')
# os.environ.get('REDDIT_PASSWORD')
# os.environ.get('REDDIT_APP_ID')
# os.environ.get('REDDIT_APP_SECRET')

# ------------------------ individual function start ------------------------
def run_function():
  base_url = 'https://www.reddit.com/'
  data = {'grant_type': 'password', 'username': os.environ.get('REDDIT_USERNAME'), 'password': os.environ.get('REDDIT_PASSWORD')}
  auth = requests.auth.HTTPBasicAuth(os.environ.get('REDDIT_APP_ID'), os.environ.get('REDDIT_APP_SECRET'))
  r = requests.post(base_url + 'api/v1/access_token',
                    data=data,
                    headers={'user-agent': 'APP-NAME by REDDIT-USERNAME'},
                    auth=auth)
  print(r)
  d = r.json()
  print(d)
  return True
# ------------------------ individual function end ------------------------

# ------------------------ call script start ------------------------
if __name__ == '__main__':
  run_function()
# ------------------------ call script end ------------------------