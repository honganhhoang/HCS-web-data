from openai import OpenAI
import os
from colorama import Fore, Style
from set_key import set_api_key_from_file

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_questions(text):
    prompt = f"Generate a list of questions by a user that can be answered using this extracted text from a website.\n\n{text}"
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {
                "role": "user",
                "content": prompt + " only write the questions.",
            }
        ],
        n=1,
        stop=None,
        temperature=0.7
    )
    questions = response.choices[0].message.content
    return questions
    

def process_files(input_directory, output_directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(input_directory, filename)
        text_content = read_text_file(file_path)
        if text_content=="":
            print(Fore.RED + 'Empty file ' + file_path + Style.RESET_ALL)
        else:
            #generate questions from file
            questions = generate_questions(text_content)
            output_file_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}_questions.txt")
            #output generated questions in a file
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(questions)
            print(f"Questions for {filename} have been generated and saved to {output_file_path}")

            
            

set_api_key_from_file()
input_directory = 'data'
output_directory = 'questions'
all_data_files = os.listdir(input_directory)

'''intrupted_indexes = [77] #undefiened characters, pdf

empty_files = ['0_9_2_1.txt', '0_4_5.txt', '0_3_2_6_1.txt',
                '0_3_1_4.txt', '0_3_1_2.txt', '0_3_1_1.txt',
                '0_1_4_2.txt', '0_1_1_2.txt', '0_1_1_11_4_7.txt',
                '0_1_1_11_4_10.txt', '0_1_1_11_2_1.txt']
# others not traced : link to youtube, pdf, not informative business websites
traced_manually = ['0_9_2_1.txt', '0_1_4_2.txt']'''

start = 78
for i, filename in enumerate(all_data_files[start:]):
    print(f"{i+start}", end=' ')
    process_files(input_directory, output_directory)
