from openai import OpenAI
import os
from colorama import Fore, Style
from set_key import set_api_key_from_file

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_answers(question, text):
    prompt = f"Answer the question based on the provided context.\n\nQuestion: {question}\n\nContext: {text}"
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4.1-nano", 
        messages=[
            {
                "role": "user",
                "content": prompt + " only write the answers.",
            }
        ],
        n=1,
        stop=None,
        temperature=0.7
    )
    questions = response.choices[0].message.content
    return questions
    

def process_files(input_directory, context_directory, output_directory):
    if filename.endswith(".txt"):
        core_name = filename.strip('_questions.txt')
        question_file_path = os.path.join(input_directory, filename)
        context_file_path = os.path.join(context_directory, core_name +'.txt')
        context = read_text_file(context_file_path).split('\n')
        questions = read_text_file(question_file_path).split('\n')
        answers = []
        for question in questions:
            #generate answers from question file according to data file
            answers.append(generate_answers(context, question))
        output_file_path = os.path.join(output_directory, f"{os.path.splitext(core_name)[0]}_answers.txt")
        #output generated answers in a file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for i, answer in enumerate(answers):
                q_number = i+1
                output_file.write(str(q_number)+'.\n')
                output_file.write(answer + '\n\n')
        print(f"Answers for {filename} have been generated and saved to {output_file_path}")

            
            

set_api_key_from_file()
input_directory = 'questions'
output_directory = 'answers'
context_directory = 'data'
all_data_files = os.listdir(input_directory)

print()
start = 0
for i, filename in enumerate(all_data_files[start:]):
    print(f"{i+start}", end=' ')
    process_files(input_directory, context_directory, output_directory)
