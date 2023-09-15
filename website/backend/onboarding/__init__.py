# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.models import UserAttributesObj
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def onboarding_checks_v2_function(current_user):
  # ------------------------ check all attributes table start ------------------------
  attribute_arr = ['attribute_marketing','x_twitter_handle']
  for i_attribute in attribute_arr:
    attribute_obj = UserAttributesObj.query.filter_by(fk_user_id=current_user.id,attribute_code=i_attribute).first()
    if attribute_obj == None or attribute_obj == []:
      return i_attribute
  # ------------------------ check all attributes table end ------------------------
  # ------------------------ check if email verified start ------------------------
  if current_user.verified_email == False:
    return 'verify'
  # ------------------------ check if email verified end ------------------------
  return False
# ------------------------ individual function end ------------------------