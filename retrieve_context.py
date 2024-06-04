import numpy as np
import pandas as pd
from generate_embeddings import get_embedding
from merge_data_with_embeddings import add_embedding_to_df

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def print_context_in_file(results, f):
    if len(results) == 0:
        print("No Context or too much was retrieved.", file=f)
        return
    
    if len(results)>10:
        length = 10
    else : 
        length = len(results)

    for idx in range(length):
        print(f"Index: {idx}", file=f)
        print("Question: " + results.iloc[idx]["Question"], file=f)
        print("Answer: " + results.iloc[idx]["Answer"], file=f)
        print("File: " + results.iloc[idx]["File"], file=f)
        print("URL: " + results.iloc[idx]["URL"], file=f)
        sim = results.iloc[idx]["Similarity"]
        print(f"Similarity: {sim}" , file=f)
        print(file=f)

def context_in_applicable_form(results):
    context = []
    resources = []
    if len(results) == 0 or len(results)>10:
        length = 10
    else:
        length = len(results)
        
    for idx in range(length):
        context.append("Question: " + results.iloc[idx]["Question"] + "Answer: " + results.iloc[idx]["Answer"])
        resources.append(results.iloc[idx]["URL"])
    return {"Text":context, "URL":set(resources)}
    

def retrieve_context(query):
    doc_df = add_embedding_to_df('StructuredQA.csv', 'Embeddings.csv')

    query_embedding = get_embedding(query)
    doc_df["Similarity"] = doc_df.QuestionEmbedding.apply(lambda x: cosine_similarity(x, query_embedding))
    results = (doc_df.sort_values("Similarity", ascending=False))

    f = open(f"QAlogs1/{query[:-1]}.txt", "a")
    print("Query: " + query, file=f)
    print(file=f)

    relevant_context = results[results['Similarity']>= 0.9]
    slightly_relevant_context = results[results['Similarity']>= 0.8]

    if len(relevant_context) > 0 :
        print_context_in_file(relevant_context, f)
        return context_in_applicable_form(relevant_context), 2
    
    elif len(slightly_relevant_context) > 0 :
        print_context_in_file(slightly_relevant_context, f)
        return context_in_applicable_form(slightly_relevant_context), 1
    
    else:
        print_context_in_file([], f)
        return "", 0

'''query = "who is Tricia-Kay Williams?"
print(retrieve_context(query))'''