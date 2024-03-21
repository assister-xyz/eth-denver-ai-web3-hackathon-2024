import pandas as pd
from utils.data_proccessing import process_body
import os

def save_dataframe_to_csv(df, filename, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    if filename.endswith('.csv'):
        file_path = os.path.join(output_directory, filename)
    else:
        file_path = os.path.join(output_directory, filename+'.csv')

    df.to_csv(file_path, index=False)

def create_dataframe_from_qa(qa):
    question_data = []

    for question in qa:
        question_id = question["question_id"]
        question_title = question.get("title", None)
        question_body = process_body(question.get("body", None))
        tags = question.get("tags", None)
        question_owner_display_name = question["owner"].get("display_name", None)
        question_owner_profile_link = question["owner"].get("link", None)  # Added line
        question_view_count = question.get("view_count", None)
        answer_count = question.get("answer_count", None)
        question_score = question.get("score", None)
        question_creation_date = pd.to_datetime(question["creation_date"], unit='s')

        if question["accepted_answer"]:
            accepted_answer = question["accepted_answer"]
            answer_owner_display_name = accepted_answer["owner"].get("display_name", None)
            answer_owner_profile_link = accepted_answer["owner"].get("link", None)  # Added line
            is_accepted = accepted_answer.get("is_accepted", None)
            answer_score = accepted_answer.get("score", None)
            answer_creation_date = pd.to_datetime(accepted_answer["creation_date"], unit='s')
            answer_body = process_body(accepted_answer.get("body", None))
        else:
            answer_owner_display_name = None
            answer_owner_profile_link = None  # Added line
            is_accepted = None
            answer_score = None
            answer_creation_date = None
            answer_body = None

        question_data.append([
            question_id, question_title, question_body, tags, question_owner_display_name, question_owner_profile_link, question_view_count,
            answer_count, question_score, question_creation_date, answer_owner_display_name, answer_owner_profile_link, is_accepted, answer_score,
            answer_creation_date, answer_body
        ])

    columns = ["Question_ID", "Question_Title", "Question_Body", "Tags", "Question_Owner_Display_Name", "Question_Owner_Profile_Link",
               "Question_View_Count", "Answer_Count", "Question_Score", "Question_Creation_Date", "Answer_Owner_Display_Name",
               "Answer_Owner_Profile_Link", "Is_Accepted", "Answer_Score", "Answer_Creation_Date", "Answer_Body"]

    df_questions = pd.DataFrame(question_data, columns=columns)

    df_questions.replace("", None, inplace=True)

    df_questions = df_questions.where(pd.notnull(df_questions), None)

    return df_questions

