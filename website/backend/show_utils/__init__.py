# ------------------------ imports start ------------------------
from website.backend.get_create_obj import get_show_based_on_id_function
from website.backend.dict_manipulation import arr_of_dict_all_columns_single_item_function
from website.models import ShowsFollowingObj
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from website import db
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def shows_following_arr_of_dict_function(page_dict):
  if page_dict['shows_following_arr_of_dict'] != None:
    shows_arr_of_dict = []
    for i_obj in page_dict['shows_following_arr_of_dict']:
      show_obj = get_show_based_on_id_function(i_obj.fk_show_id)
      # ------------------------ if following show that has been deleted start ------------------------
      if show_obj == None:
        continue
      # ------------------------ if following show that has been deleted end ------------------------
      show_dict = arr_of_dict_all_columns_single_item_function(show_obj)
      show_dict['description'] = show_dict['description'][0:150] + '...'
      shows_arr_of_dict.append(show_dict)
    sorted_shows_arr_of_dict = sorted(shows_arr_of_dict, key=lambda x: x['name'])
    page_dict['shows_following_arr_of_dict'] = sorted_shows_arr_of_dict
  return page_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def follow_user_polls_show_function(current_user):
  change_made = False
  db_obj = ShowsFollowingObj.query.filter_by(fk_show_id='show_user_attributes',fk_user_id=current_user.id).first()
  if db_obj == None or db_obj == []:
    # ------------------------ insert to db start ------------------------
    new_row = ShowsFollowingObj(
      id=create_uuid_function('following_'),
      created_timestamp=create_timestamp_function(),
      fk_platform_id = 'podcast',
      fk_show_id = 'show_user_attributes',
      fk_user_id = current_user.id
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ insert to db end ------------------------
    change_made = True
  return change_made
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def follow_show_function(current_user, show_id):
  change_made = False
  db_obj = ShowsFollowingObj.query.filter_by(fk_show_id=show_id,fk_user_id=current_user.id).first()
  if db_obj == None or db_obj == []:
    # ------------------------ insert to db start ------------------------
    new_row = ShowsFollowingObj(
      id=create_uuid_function('following_'),
      created_timestamp=create_timestamp_function(),
      fk_platform_id = 'podcast',
      fk_show_id = show_id,
      fk_user_id = current_user.id
    )
    db.session.add(new_row)
    db.session.commit()
    # ------------------------ insert to db end ------------------------
    change_made = True
  return change_made
# ------------------------ individual function end ------------------------