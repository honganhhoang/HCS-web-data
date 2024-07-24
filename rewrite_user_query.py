from openai import OpenAI
import os

from set_key import set_api_key_from_file

def rewrite_prompt(c_history, query):
    history = f""" A: {c_history[0]} 
    B: {c_history[1]}
    """
    prompt = f"""rewrite the query in the form of a CLEAR and CONCISE question. Use the provided conversation history for clearification.
    Conversation history: [{history}]
    Query: [{query}] """
    return prompt


def rewrite_users_query(last_messages, Q):
    if len(last_messages) == 0:
        return Q
    message = rewrite_prompt(last_messages, Q)
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
        model="gpt-3.5-turbo",
        max_tokens=50,
    )
    new_query = chat_completion.choices[0].message.content

    out = open(f"Q_rewrite/queries.txt", "a")
    print("User: " + message, file=out)
    print("Rewrite: " + new_query, file=out)
    print(file=out)
    out.close()

    return new_query

'''q = "how can i contact them"
history = ["what services are available for indigenious people at sfu counselling?", """At SFU's Indigenous Student Centre and SFU, the following support services are available for Indigenous students:

Wholistic wellness programs
Wellness Program
Indigenous Clinical Counsellors
Elders Program Drop-in
Cultural Connections workshop
Black Counsellor (Tricia Kay Williams)
Online Resilience Course
Group counselling
Online self-help resources
MindShift Application
Additional support options and counselling services from SFU Health and Counselling Services
For more information, you can visit the SFU Indigenous Wellness page at: SFU Indigenous Wellness"""]


new_q = rewrite_users_query(history, q)
print(new_q)'''