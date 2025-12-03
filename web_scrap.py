import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_text_from_webpage(url, txt_file_name):

    response = requests.get(url, headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }, allow_redirects=False, verify=True)
    soup = BeautifulSoup(response.content, 'html.parser')

    paragraphs = soup.find_all('p')

    # Extract text from each paragraph and store in a list
    text_data = [p.get_text() for p in paragraphs]

    # Define the output txt file
    file_name = f"data/{txt_file_name}.txt"

    # Open the file in write mode
    with open(file_name, 'w', encoding='utf-8') as file:
        # Write each paragraph to the file
        for paragraph in text_data:
            file.write(paragraph + '\n\n')  # Add extra newline for readability

    print(f'Data successfully saved to {file_name}')

csv_file = 'sfu_indigenous.csv' 
df = pd.read_csv(csv_file)

list_of_exceptions = ["0_3_9_13", "0_2_1_2", "0_2_6"]

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    url = row['link']
    file_name = row['name']
    if file_name in list_of_exceptions:
        continue
    extract_text_from_webpage(url, file_name)