from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
from question_answering_bot import manage_query


class Bot():
    def __init__(self, sys_message=None):
        self.messages = []
        if sys_message:
            self.set_sysMessage(sys_message)
        self.chat_api = ChatOpenAI(
                        openai_api_key=os.environ["OPENAI_API_KEY"],
                        model='gpt-3.5-turbo'
                        )

    def set_sysMessage(self, sys_message):
        self.system_message = SystemMessage(content=sys_message)
        # Initiating the bot from scratch if System Message has changed
        self.messages = [self.system_message]

    def handle_input(self, query):
        self.messages.append(HumanMessage(content=query.content))
        response = self.chat_api(self.messages)
        self.messages.append(response)
        return response


def BotUser_dialogue_cycle(bot, user):

    f = open(f"chatlog/chat{user}.txt", "a")

    # Initiate Bot Dialogue
    ai_message = bot.handle_input(HumanMessage(content="Hi"))

    print("You are talking to SFU counselling information Chatbot. If you wish to exit the conversation, please type in the word: exit")
    end_flag = False

    while end_flag != True:
        # Store Bot message
        print("Bot>> " + ai_message.content)
        print("Bot>> " + ai_message.content, file=f)
        print(file=f)

        # Get and Store User Response
        user_inpt = input("User>>")
        print("User>>" + user_inpt, file=f)
        print(file=f)
        if user_inpt=="exit":
            end_flag = True

        augmented_prompt = manage_query(user_inpt)

        #print("\n *** "+ augmented_prompt + " ***\n", file=f)

        ai_message = bot.handle_input(HumanMessage(content=augmented_prompt))
    return