from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os
from question_answering_bot import manage_query

class Bot:
    def __init__(self, sys_message: str | None = None):
        # messages will hold SystemMessage / HumanMessage / AIMessage objects
        self.messages = []
        self.system_message = None

        if sys_message:
            self.set_sysMessage(sys_message)

        # Use .get on env to avoid KeyError during dev runs; ensure key is present in production
        self.chat_api = ChatOpenAI(
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            model="gpt-4.1-mini"
        )

    def set_sysMessage(self, sys_message: str):
        """Set or replace the system message and reset the conversation history."""
        self.system_message = SystemMessage(content=sys_message)
        # Start a fresh conversation whenever system message changes
        self.messages = [self.system_message]

    def handle_input(self, query):
        """
        Accepts either:
          - a HumanMessage instance
          - a plain string
          - any object with a .content attribute
        Appends the user message, invokes the model, appends and returns the assistant message.
        """
        # Normalize user message
        if isinstance(query, HumanMessage):
            user_msg = query
        elif isinstance(query, str):
            user_msg = HumanMessage(content=query)
        elif hasattr(query, "content"):
            # assume it's message-like (e.g., passed HumanMessage already)
            user_msg = HumanMessage(content=query.content)
        else:
            user_msg = HumanMessage(content=str(query))

        self.messages.append(user_msg)

        # IMPORTANT: use invoke() — ChatOpenAI is not callable
        response = self.chat_api.invoke(self.messages)

        # Normalize response to AIMessage if necessary
        if hasattr(response, "content"):
            assistant_msg = response
        else:
            assistant_msg = AIMessage(content=str(response))

        self.messages.append(assistant_msg)
        return assistant_msg


def BotUser_dialogue_cycle(bot: Bot, user: str):
    """
    Simple interactive loop writing to chatlog/chat{user}.txt.
    Assumes a manage_query(user_input: str) -> str function exists elsewhere.
    """
    os.makedirs("chatlog", exist_ok=True)

    with open(f"chatlog/chat{user}.txt", "a") as f:
        # Kick things off with a greeting to the assistant
        ai_message = bot.handle_input(HumanMessage(content="Hi"))

        print(
            "You are talking to SFU Indigenous information Chatbot. "
            "If you wish to exit the conversation, please type in the word: exit"
        )
        end_flag = False

        while not end_flag:
            content = getattr(ai_message, "content", str(ai_message))

            # Print & log assistant message
            print("Bot>> " + content)
            print("Bot>> " + content, file=f)
            print(file=f)

            # Read user input and log it
            user_inpt = input("User>>")
            print("User>>" + user_inpt, file=f)
            print(file=f)

            # Exit condition
            if user_inpt.strip().lower() == "exit":
                end_flag = True
                break

            # Augment/clean the user query (you must have manage_query implemented)
            augmented_prompt = manage_query(bot.messages, user_inpt)

            # Pass the augmented prompt to the bot (string OK)
            ai_message = bot.handle_input(augmented_prompt)

    return
