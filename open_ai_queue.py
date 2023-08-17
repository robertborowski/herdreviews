# ------------------------ imports start ------------------------
import os, time
from backend.db.connection.postgres_connect_to_database import postgres_connect_to_database_function
from backend.db.connection.postgres_close_connection_to_database import postgres_close_connection_to_database_function
from backend.db.queries.select_queries.polling import select_manual_function
from backend.db.queries.insert_queries.polling import insert_manual_function
from backend.db.queries.delete_queries.polling import delete_manual_function
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
import openai
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
    print('email sent successfully! ' + output_subject_line + " - To: " + output_email)
  except:
    print('email did not send successfully...' + output_subject_line)
    return False
  return True
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def openai_chat_gpt_prompt_result_function(message):
  try:
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}
      ]
    )
    # Retrieve and return the assistant's reply
    reply = response['choices'][0]['message']['content']
  except Exception as e:
    # ------------------------ email self start ------------------------
    try:
      output_to_email = os.environ.get('HR_SUPPORT_EMAIL')
      output_subject = f'Failure on ChatGPT openai_chat_gpt_prompt_result_function'
      output_body = f'Failure on ChatGPT openai_chat_gpt_prompt_result_function: {e}'
      send_email_template_function(output_to_email, output_subject, output_body)
    except:
      pass
    # ------------------------ email self end ------------------------
    return None
  return reply
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def openai_chat_gpt_parse_results_to_arr_polling_function(chatgpt_response_str):
  result_arr_of_dict = None
  try:
    # ------------------------ remove line breaks from str start ------------------------
    chatgpt_response_str = chatgpt_response_str.replace('\n','')
    chatgpt_response_str = chatgpt_response_str.replace('~','')
    # ------------------------ remove line breaks from str end ------------------------
    # ------------------------ split the string into questions arr start ------------------------
    result_arr = chatgpt_response_str.split('polling_question_')
    # ------------------------ split the string into questions arr end ------------------------
    # ------------------------ remove any strings that are not part of the desired result start ------------------------
    result_arr_copy = result_arr[:]
    for i_str in result_arr_copy:
      if 'polling_answer_' not in i_str:
        result_arr.remove(i_str)
    # ------------------------ remove any strings that are not part of the desired result end ------------------------
    # ------------------------ manipulate to array of dicts start ------------------------
    result_arr_of_dict = []
    for i in result_arr:
      i_dict = {}
      # ------------------------ breakup question start ------------------------
      question_segments = i.split(":")
      question_pulled = ''
      try:
        question_pulled = question_segments[1].strip()
      except:
        question_pulled = question_segments[0].strip()
      question = question_pulled.replace('polling_answer_1','').strip()
      i_dict['question'] = question
      # ------------------------ breakup question end ------------------------
      # ------------------------ breakup answers start ------------------------
      answer_segments = i.split(":")[2:]
      answers_arr = []
      for i_answer in answer_segments:
        # ------------------------ answer parsing start ------------------------
        search_string = 'polling_answer'
        if search_string in i_answer:
          found_index = i_answer.find(search_string)
          i_answer = i_answer[:found_index]
        # ------------------------ answer parsing end ------------------------
        # ------------------------ answer cleanup edges start ------------------------
        i_answer = i_answer.strip()
        if i_answer[0] == "'" or i_answer[0] == '"' or i_answer[0] == '-':
          i_answer = i_answer[1:]
        if i_answer[-1] == "'" or i_answer[-1] == '"' or i_answer[-1] == '-':
          i_answer = i_answer[:-1]
        i_answer = i_answer.strip()
        # ------------------------ answer cleanup edges end ------------------------
        answers_arr.append(i_answer)
      i_dict['answer_choices'] = answers_arr
      # ------------------------ breakup answers end ------------------------
      result_arr_of_dict.append(i_dict)
    # ------------------------ manipulate to array of dicts end ------------------------
  except Exception as e:
    # ------------------------ email self start ------------------------
    try:
      output_to_email = os.environ.get('HR_SUPPORT_EMAIL')
      output_subject = f'Failure on ChatGPT openai_chat_gpt_parse_results_to_arr_polling_function'
      output_body = f'Failure on ChatGPT openai_chat_gpt_parse_results_to_arr_polling_function: {e}'
      send_email_template_function(output_to_email, output_subject, output_body)
    except:
      pass
    return None
    # ------------------------ email self end ------------------------
  return result_arr_of_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def create_openai_starter_poll_questions_function(show_name, show_description):
  # ------------------------ clean show name start ------------------------
  show_name = show_name.replace(':','')
  # ------------------------ clean show name end ------------------------
  # ------------------------ openai start ------------------------
  chatgpt_message = f"Please generate 5 polling questions that meet the following rules. Rule #1: The polling questions should be directed towards listeners of the podcast '{show_name}'. Gather research/information about the podcast before writing these questions. Rule #2: Avoid general polling questions. Rule #3: Each polling question should have at least 6 options as answer choices. Rule #4: Each question number should be preceded with the word 'polling_question_' (lowercase), for example question 1 should be titled 'polling_question_1' (lowercase) and so on until 'polling_question_5' (lowercase). Rule #5: Each answer option should be preceded with the word 'polling_answer_' (lowercase), for example answer option 1 should be titled 'polling_answer_1' (lowercase) and so on until 'polling_answer_6' (lowercase). Rule #6: Do not include 'a) ,b) ,c) ,d) ,e) ' as separators for the answer choices. Rule #7: Do not include '-' as separators for the answer choices. Rule #8: The only answer choice separators should be polling_answer_1 through polling_answer_6. Rule #9: Each question number should not have any additional separators or numbering except for polling_question_1 through polling_question_5. Rule #10: Do not include the podcast name '{show_name}' in polling_question_1 through polling_question_5 titles. Rule #11: In your response DO NOT INCLUDE any variation of the following questions [“What is your preferred episode length for the podcast?”,“How did you discover the podcast?”,“Would you like to see more live events or meet-ups organized by the podcast?”,“Have you ever recommended the podcast to others?”,“How likely are you to recommend the podcast to a friend or colleague?”,“Which country are you from?”,“How do you prefer to listen to the podcast?”,“How often do you share episodes of the podcast with others?”,“How would you rate the hosts chemistry and banter?”,“Which social media platform do you primarily use to engage with the podcast?”,“What is your preferred format for consuming the podcast?”,“How do you typically consume the podcast?”,“On average, how many episodes of the podcast do you listen to in a week?”,”How do you discover new episodes of the podcast?”,“How frequently do you listen to new episodes of the podcast?”,“How would you rate the audio quality of the podcast?”,“How often do you listen to the podcast?”,“How long have you been listening to the podcast”,”How likely are you to attend a live podcast event hosted by the podcast?”,”How frequently do you listen to the podcast?”,”Which social media platform do you primarily use for engaging with the podcast?”]."
  chatgpt_response_str = openai_chat_gpt_prompt_result_function(chatgpt_message)
  chatgpt_response_arr_of_dicts = openai_chat_gpt_parse_results_to_arr_polling_function(chatgpt_response_str)
  # ------------------------ openai end ------------------------
  # ------------------------ sanitize/check results as expected start ------------------------
  if chatgpt_response_arr_of_dicts == None or chatgpt_response_arr_of_dicts == []:
    return None
  # ------------------------ sanitize/check results as expected end ------------------------
  return chatgpt_response_arr_of_dicts
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def run_function():
  queue_on = True
  failure_counter = 0
  while queue_on == True:
    # ------------------------ open db connection start ------------------------
    # Connect to Postgres database
    postgres_connection, postgres_cursor = postgres_connect_to_database_function()
    # ------------------------ open db connection end ------------------------
    # ------------------------ select start ------------------------
    queue_result_arr_of_dict = select_manual_function(postgres_connection, postgres_cursor, 'select1')
    # ------------------------ select end ------------------------
    # ------------------------ if no results start ------------------------
    if queue_result_arr_of_dict == None:
      # ------------------------ close db connection start ------------------------
      postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
      # ------------------------ close db connection end ------------------------
      # ------------------------ logs start ------------------------
      print('show queue empty')
      # ------------------------ logs end ------------------------
      time.sleep(60)
    # ------------------------ if no results end ------------------------
    # ------------------------ if yes results start ------------------------
    else:
      for i_queue_dict in queue_result_arr_of_dict:
        # ------------------------ check if show already exists start ------------------------
        show_exists_in_db_check = select_manual_function(postgres_connection, postgres_cursor, 'select2', i_queue_dict['platform_reference_id'])
        if show_exists_in_db_check != None and show_exists_in_db_check != []:
          try:
            delete_manual_function(postgres_connection, postgres_cursor, 'delete_queue', i_queue_dict['id'])
          except:
            pass
          continue
        # ------------------------ check if show already exists end ------------------------
        pulled_show_id=i_queue_dict['fk_show_id']
        try:
          # ------------------------ openai get starter polls start ------------------------
          chatgpt_response_arr_of_dicts = create_openai_starter_poll_questions_function(i_queue_dict['name'], i_queue_dict['description'])
          if chatgpt_response_arr_of_dicts != None and chatgpt_response_arr_of_dicts != []:
            # ------------------------ add to db start ------------------------
            for i_chat_dict in chatgpt_response_arr_of_dicts:
              answers_str = "~".join(i_chat_dict['answer_choices'])
              id=create_uuid_function('poll_')
              created_timestamp=create_timestamp_function()
              # ------------------------ insert to db start ------------------------
              insert_inputs_arr = [id,created_timestamp,'show',pulled_show_id,i_chat_dict['question'],answers_str,True,True,False]
              insert_manual_function(postgres_connection, postgres_cursor, 'insert_poll', insert_inputs_arr)
              # ------------------------ insert to db end ------------------------
            # ------------------------ add to db end ------------------------
            # ------------------------ insert to db start ------------------------
            created_timestamp=create_timestamp_function()
            insert_inputs_arr = [pulled_show_id,created_timestamp,i_queue_dict['name'],i_queue_dict['description'],i_queue_dict['fk_platform_id'],True,i_queue_dict['platform_reference_id'],i_queue_dict['img_large'],i_queue_dict['img_medium'],i_queue_dict['img_small'],i_queue_dict['show_url']]
            insert_manual_function(postgres_connection, postgres_cursor, 'insert_show', insert_inputs_arr)
            # ------------------------ insert to db end ------------------------
            # ------------------------ delete show from queue start ------------------------
            try:
              delete_manual_function(postgres_connection, postgres_cursor, 'delete_queue', i_queue_dict['id'])
            except Exception as e:
              print(f'error : {e}')
              pass
            # ------------------------ delete show from queue end ------------------------
          else:
            failure_counter += 1
            # ------------------------ email self start ------------------------
            try:
              output_to_email = os.environ.get('HR_SUPPORT_EMAIL')
              output_subject = f"Failure on ChatGPT {i_queue_dict['name']}"
              output_body = f"Failure on ChatGPT {i_queue_dict['name']} - failure_counter: {failure_counter}"
              send_email_template_function(output_to_email, output_subject, output_body)
            except:
              pass
            # ------------------------ email self end ------------------------
            # ------------------------ while loop force end start ------------------------
            if failure_counter == 5:
              return False
            # ------------------------ while loop force end end ------------------------
          # ------------------------ openai get starter polls end ------------------------
        except:
          try:
            delete_manual_function(postgres_connection, postgres_cursor, 'delete_polls', pulled_show_id)
          except:
            pass
          try:
            delete_manual_function(postgres_connection, postgres_cursor, 'delete_shows', pulled_show_id)
          except:
            pass
          try:
            delete_manual_function(postgres_connection, postgres_cursor, 'delete_shows_following', pulled_show_id)
          except:
            pass
        # ------------------------ openai rate limit start ------------------------
        time.sleep(30)
        # ------------------------ openai rate limit end ------------------------
      # ------------------------ close db connection start ------------------------
      postgres_close_connection_to_database_function(postgres_connection, postgres_cursor)
      # ------------------------ close db connection end ------------------------
    # ------------------------ if yes results end ------------------------
  return True
# ------------------------ individual function end ------------------------

# ------------------------ run function start ------------------------
if __name__ == "__main__":
  run_function()
# ------------------------ run function end ------------------------