# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
from website.models import EmailSentObj
from website.backend.candidates.string_manipulation import breakup_email_function
from website.backend.candidates.send_emails import send_email_template_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
from website import db
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def email_share_with_team_function(current_user):
  # ------------------------ check if share with team email has been sent start ------------------------
  output_subject = f"Successfully Verified Email"
  db_email_obj = EmailSentObj.query.filter_by(to_email=current_user.email,subject=output_subject).first()
  if db_email_obj == None or db_email_obj == []:
    # ------------------------ send email start ------------------------
    try:
      guessed_name = breakup_email_function(current_user.email)
      output_to_email = current_user.email
      output_body = f"<p>Hi {guessed_name},</p>\
                      <p>Thank you for creating an account with HerdReviews!</p>\
                      <p>Your team members can access the same team building activities <a href='https://herdreviews.com/signup'>here</a>, simply forward this email to your team.</p>\
                      <p style='margin:0;'>Best,</p>\
                      <p style='margin:0;'>HerdReviews Support Team</p>"
      send_email_template_function(output_to_email, output_subject, output_body)
      # ------------------------ insert email to db start ------------------------
      try:
        new_row = EmailSentObj(
          id = create_uuid_function('email_'),
          created_timestamp = create_timestamp_function(),
          from_user_id_fk = current_user.id,
          to_email = output_to_email,
          subject = output_subject,
          body = output_body
        )
        db.session.add(new_row)
        db.session.commit()
      except:
        pass
      # ------------------------ insert email to db end ------------------------
    except:
      pass
    # ------------------------ send email end ------------------------
  # ------------------------ check if share with team email has been sent end ------------------------
  return True
# ------------------------ individual function end ------------------------