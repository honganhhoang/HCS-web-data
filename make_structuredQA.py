import pandas as pd
import os
import re

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_col_values_from_file(question_directory, answer_directory, filename):

    questions_file_path = os.path.join(question_directory, filename + '_questions.txt')

    questions = read_text_file(questions_file_path).split('\n')
    questions = [q.split('. ')[1] for q in questions]
    count = len(questions)

    answers_file_path = os.path.join(answer_directory, filename + '_answers.txt')
    content_of_answer_file = read_text_file(answers_file_path)
    answers = re.split(r'\n(?=\d+\.\n)', content_of_answer_file)
    answers = [a.strip().split('.\n')[1] for a in answers]

    website_data = pd.read_csv('HCS website.csv')
    filtered_df = website_data[website_data['name'] == filename]

    data = []
    for idx in range(count):
        row = {"Question": questions[idx],
               "Answer": answers[idx],
               "File": filename,
               "URL": filtered_df['link'].values[0]}
        data.append(row)

    return data


q_directory = 'questions'
a_directory = 'answers'
all_files = [file_name.strip('_questions.txt') for file_name in os.listdir(q_directory)]

columns = ['Question', 'Answer', 'File']
df = pd.DataFrame(columns=columns)

start = 0
for i, file in enumerate(all_files[start:]):
    print(i, end=' ')
    rows = read_col_values_from_file(q_directory, a_directory, file)
    df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
    print(f"Question & Answer pairs for {file} have been added to dataframe.")

print(df)
# [1745 rows x 4 columns]

df.to_csv('StructuredQA.csv', index=False)
#test
#df = pd.read_csv('StructuredQA.csv')
#print(df.head(3))




