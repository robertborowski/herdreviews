
# ------------------------ imports start ------------------------
from backend.utils.localhost_print_utils.localhost_print import localhost_print_function
import os
from backend.utils.uuid_and_timestamp.create_uuid import create_uuid_function
from backend.utils.uuid_and_timestamp.create_timestamp import create_timestamp_function
import openai
from website.models import UserCelebrateObj,ActivityACreatedQuestionsObj, UserObj
from website.backend.candidates.dict_manipulation import arr_of_dict_all_columns_single_item_function
from sqlalchemy import and_, or_
from datetime import date
from website import db
import random
from website.backend.candidates.send_emails import send_email_template_function
# ------------------------ imports end ------------------------

# ------------------------ individual function start ------------------------
def openai_chat_gpt_prompt_result_function(message):
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
  return reply
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def openai_chat_gpt_parse_results_to_arr_function(chatgpt_response_str):
  chatgpt_start_index = chatgpt_response_str.find("[")
  chatgpt_end_index = chatgpt_response_str.find("]")
  chatgpt_response_substring = None
  if chatgpt_start_index != -1 and chatgpt_end_index != -1:
    chatgpt_response_substring = chatgpt_response_str[chatgpt_start_index + 1 : chatgpt_end_index].strip()  # Extract the substring
    chatgpt_response_substring = chatgpt_response_substring.replace('"','')
    chatgpt_response_substring = chatgpt_response_substring.replace("'","")
  chatgpt_response_arr = None
  if chatgpt_response_substring != None:
    chatgpt_response_arr = chatgpt_response_substring.split(', ')
  return chatgpt_response_arr
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
      question_pulled = question_segments[1].strip()
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
  except:
    pass
  return result_arr_of_dict
# ------------------------ individual function end ------------------------

# ------------------------ individual function start ------------------------
def create_openai_starter_poll_questions_function(show_name):
  # ------------------------ clean show name start ------------------------
  show_name = show_name.replace(':','')
  # ------------------------ clean show name end ------------------------
  # ------------------------ openai start ------------------------
  chatgpt_message = f"I would like you to create 10 polling questions for me that follow the following rules. Rule #1: The polling questions should be aimed at the average listener of the podcast '{show_name}'. Rule #2: Please avoid general polling questions that could be asked about any other podcast. Rule #3: Each polling question should have at least 5 options as answer choices. Rule #4: Each question number should be preceded with the word 'polling_question_' (lowercase), for example question 1 should be titled 'polling_question_1' (lowercase) and so on until 'polling_question_10' (lowercase). Rule #5: Each answer option should be preceded with the word 'polling_answer_' (lowercase), for example answer option 1 should be titled 'polling_answer_1' (lowercase) and so on until 'polling_answer_5' (lowercase). Rule #6: Do not include 'a) ,b) ,c) ,d) ,e) ' as separators for the answer choices. Rule #7: Do not include '-' as separators for the answer choices. Rule #8: The only answer choice separators should be polling_answer_1 through polling_answer_5. Rule #9: Each question number should not have any additional separators or numbering except for polling_question_1 through polling_question_10."
  chatgpt_response_str = openai_chat_gpt_prompt_result_function(chatgpt_message)
  chatgpt_response_arr_of_dicts = openai_chat_gpt_parse_results_to_arr_polling_function(chatgpt_response_str)
  # ------------------------ openai end ------------------------
  # ------------------------ sanitize/check results as expected start ------------------------
  if chatgpt_response_arr_of_dicts == None or chatgpt_response_arr_of_dicts == []:
    # ------------------------ email self start ------------------------
    try:
      output_to_email = os.environ.get('HR_SUPPORT_EMAIL')
      output_subject = f'Failure on ChatGPT parsing polls for {show_name}'
      output_body = f'Failure on ChatGPT parsing polls for {show_name}'
      send_email_template_function(output_to_email, output_subject, output_body)
    except:
      pass
    # ------------------------ email self end ------------------------
  # ------------------------ sanitize/check results as expected end ------------------------
  return chatgpt_response_arr_of_dicts
# ------------------------ individual function end ------------------------