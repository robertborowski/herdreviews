# ------------------------ imports start ------------------------
import requests
import os
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def spotify_api_get_access_token_function():
  client_id = os.environ.get('SPOTIFY_CLIENT_ID')
  client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
  auth_url = 'https://accounts.spotify.com/api/token'
  auth_response = requests.post(auth_url, {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
  })
  auth_response_data = auth_response.json()
  access_token = auth_response_data['access_token']
  return access_token
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def spotify_search_show_function(input_show_name):
  # ------------------------ results max start ------------------------
  max_result = 5
  # ------------------------ results max end ------------------------
  # ------------------------ spotify get access token for API start ------------------------
  access_token = spotify_api_get_access_token_function()
  # ------------------------ spotify get access token for API end ------------------------
  # ------------------------ API request start ------------------------
  headers = {
    'Authorization': f'Bearer {access_token}'
  }
  params = {
    'q': input_show_name,
    'type': 'show',
    'limit': max_result,
    'market': 'US'
  }
  base_url = 'https://api.spotify.com/v1/search'
  response = requests.get(base_url, headers=headers, params=params)
  # ------------------------ API request start ------------------------
  # ------------------------ convert API results start ------------------------
  response_dict = response.json()
  # ------------------------ explore response start ------------------------
  # for k,v in response_dict['shows']['items'][0].items():
  #   print(f'k: {k} | v: {v}')
  # ------------------------ explore response end ------------------------
  # ------------------------ if none start ------------------------
  if response_dict['shows']['items'] == None or response_dict['shows']['items'] == [] or response_dict['shows']['items'] == '':
    return None
  # ------------------------ if none end ------------------------
  pulled_arr_of_dicts = []
  for i in range(0, max_result):
    pulled_dict = {
      'id': None,
      'name': None,
      'description': None,
      'img_large': None,
      'img_medium': None,
      'img_small': None,
      'show_url': None
    }
    try:
      pulled_dict['id'] = response_dict['shows']['items'][i]['id']
      pulled_dict['name'] = response_dict['shows']['items'][i]['name']
      pulled_dict['description'] = response_dict['shows']['items'][i]['description'][0:999]
      pulled_dict['img_large'] = response_dict['shows']['items'][i]['images'][0]['url']
      pulled_dict['img_medium'] = response_dict['shows']['items'][i]['images'][1]['url']
      pulled_dict['img_small'] = response_dict['shows']['items'][i]['images'][2]['url']
      pulled_dict['show_url'] = response_dict['shows']['items'][i]['external_urls']['spotify']
      pulled_arr_of_dicts.append(pulled_dict)
    except:
      pass
  # ------------------------ convert API results end ------------------------
  # ------------------------ check none start ------------------------
  if pulled_arr_of_dicts == [] or pulled_arr_of_dicts == None:
    return None
  # ------------------------ check none end ------------------------
  return pulled_arr_of_dicts
# ------------------------ individual function end ------------------------