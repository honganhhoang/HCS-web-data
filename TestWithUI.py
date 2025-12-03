import gradio as gr

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
from bot import Bot
from question_answering_bot import manage_query
from set_key import set_api_key_from_file


def HCS(message, history):
    global LATEST

    augmented_prompt = manage_query(LATEST, message)
    ai_message = bot1.handle_input(HumanMessage(content=augmented_prompt))
    
    f = open(f"UIchatlog/chat1.txt", "a")
    print("User>>" + message, file=f)
    print(file=f)
    print("Bot>> " + ai_message.content, file=f)
    print(file=f)
    f.close()

    LATEST = [message, ai_message.content]

    return ai_message.content



set_api_key_from_file()
LATEST = []
# Initiate chatbot
bot_sysMessage = "You are an information chatbot to answer students' questions based on content that is given to you from SFU counselling website."
bot1 = Bot(bot_sysMessage)

description = """I'm here to help you find information about the counseling services available at SFU. Whether you have questions about how to book an appointment, what types of services we offer, or where to find self-help resources, I'm here to guide you to the right webpages.

Please note that I am not a counselor and cannot provide counseling services or handle emergencies. If you're experiencing a crisis, please contact SFU's crisis services directly or dial emergency services.

Your privacy is important to us. All conversation histories will be deleted once our chat ends, ensuring that no one can access them.

Feel free to ask me anything about SFU's Health & Counseling Services, and I'll do my best to assist you!"""

initial_msg = "Ask me a question about SFU Health & Counseling Service."

gr.ChatInterface(
    HCS,
    chatbot=gr.Chatbot(height=500),
    textbox=gr.Textbox(placeholder=initial_msg, container=False, scale=7),
    title="Welcome to the SFU Health & Counseling Services Chatbot!",
    description=description,
    theme="soft",
    cache_examples=False,
    retry_btn=None,
    undo_btn=None,
    clear_btn="Clear and Exit",
).launch()