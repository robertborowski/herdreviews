# ------------------------ imports start ------------------------
import re
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_letters_numbers_spaces_only_function(user_input):
  try:
    if len(user_input) == 0 or len(user_input) > 100:
      return False
  except:
    return False
  desired_regex_pattern = "^[a-zA-Z0-9 ]{1,100}$"
  if(re.fullmatch(desired_regex_pattern, user_input)):
    return user_input
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_letters_numbers_spaces_specials_only_function(user_input):
  try:
    if len(user_input) == 0 or len(user_input) > 100:
      return False
  except:
    return False
  desired_regex_pattern = r'^[a-zA-Z0-9\s\-\$\@\!\?\,]{1,100}$'
  if(re.fullmatch(desired_regex_pattern, user_input)):
    return user_input
  return False
# ------------------------ individual function end ------------------------

# ------------------------ individual arr start ------------------------
replace_from_str_arr_v1 = ['select','update','delete','insert','drop','<','>','{','}','[',']','~','`','_']
replace_from_str_arr_v2 = ['<','>','{','}','[',']','~','`','_','^','%']
# ------------------------ individual arr end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_text_v1_function(ui_text, ui_text_limit, status_required):
  try:
    # ------------------------ if none start ------------------------
    if ui_text == ' ' or ui_text == '' or ui_text == None:
      return None
    # ------------------------ if none end ------------------------
    # ------------------------ if required start ------------------------
    if status_required == False:
      if len(ui_text) > int(ui_text_limit):
        return False
    if status_required == True:
      if len(ui_text) == 0 or len(ui_text) > int(ui_text_limit):
        return False
    # ------------------------ if required end ------------------------
    # ------------------------ cleanup start ------------------------
    ui_text = ui_text.lower()
    for i in replace_from_str_arr_v1:
      if i in ui_text:
        ui_text = ui_text.replace(i,'_')
    ui_text = ui_text.strip()
    # ------------------------ cleanup end ------------------------
    return ui_text
  except:
    return False
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def sanitize_text_v2_function(ui_text, ui_text_limit, status_required):
  try:
    ui_text = ui_text.strip()
    # ------------------------ if none start ------------------------
    if ui_text == ' ' or ui_text == '' or ui_text == None:
      return False
    # ------------------------ if none end ------------------------
    # ------------------------ if required start ------------------------
    if status_required == False:
      if len(ui_text) > int(ui_text_limit):
        return False
    if status_required == True:
      if len(ui_text) == 0 or len(ui_text) > int(ui_text_limit):
        return False
    # ------------------------ if required end ------------------------
    # ------------------------ cleanup start ------------------------
    # ui_text = ui_text.lower()
    for i in replace_from_str_arr_v2:
      if i in ui_text:
        ui_text = ui_text.replace(i,'_')
    ui_text = ui_text.strip()
    # ------------------------ cleanup end ------------------------
    return ui_text
  except:
    return False
# ------------------------ individual function end ------------------------