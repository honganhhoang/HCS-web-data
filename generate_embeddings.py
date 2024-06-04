from openai import OpenAI
import pandas as pd
from set_key import set_api_key_from_file


def get_embedding(text, model="text-embedding-ada-002"):
    client = OpenAI()
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


'''set_api_key_from_file()
df = pd.read_csv('StructuredQA.csv')
#df.to_csv('ToyStructuredQA.csv', index=False)

embedding_df = pd.DataFrame(columns=[i for i in range(1536)])

embeddings = df.Question.apply(lambda x: get_embedding(x))
for embedding in embeddings:
    row = {}
    for i in range(1536):
        row[i] = embedding[i]
    embedding_df = pd.concat([embedding_df, pd.DataFrame([row])], ignore_index=True)

embedding_df.to_csv('Embeddings.csv', index=False)'''