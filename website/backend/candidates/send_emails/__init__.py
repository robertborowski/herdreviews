# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import os
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def send_email_template_function(output_email, output_subject_line, output_message_content):
  sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY_TRIVIAFY'))
  from_email = Email(email = os.environ.get('HR_SUPPORT_EMAIL'), name = "HerdReviews")  # Change to your verified sender
  to_email = To(output_email)  # Change to your recipient
  subject = output_subject_line
  content = Content("text/html", output_message_content)
  mail = Mail(from_email, to_email, subject, content)
  # Get a JSON-ready representation of the Mail object
  mail_json = mail.get()
  # Send an HTTP POST request to /mail/send
  #response = sg.client.mail.send.post(request_body=mail_json)
  try:
    sg.client.mail.send.post(request_body=mail_json)
    localhost_print_function('email sent successfully! ' + output_subject_line + " - To: " + output_email)
  except:
    localhost_print_function('email did not send successfully...' + output_subject_line)
    return False
  return True
# ------------------------ individual function end ------------------------