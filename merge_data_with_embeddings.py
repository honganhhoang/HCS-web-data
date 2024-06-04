import pandas as pd

def add_embedding_to_df(file_path, embedding_path):

    df = pd.read_csv(file_path)
    embedding_df = pd.read_csv(embedding_path)

    embedding_list_retrieved = [embedding_df.iloc[i].tolist() for i in range(len(embedding_df))]
    df['QuestionEmbedding'] = embedding_list_retrieved

    return df

#doc_df = add_embedding_to_df('StructuredQA.csv', 'Embeddings.csv')
#print(doc_df)
#[1745 rows x 5 columns]
#print(type(doc_df.iloc[0]['QuestionEmbedding'][0]))
