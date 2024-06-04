from bot import BotUser_dialogue_cycle, Bot
from set_key import set_api_key_from_file

def main():
    set_api_key_from_file()
    # Initiate chatbot
    bot_sysMessage = "You are an information chatbot to answer students' questions based on content that is given to you from SFU counselling website."
    bot = Bot(bot_sysMessage)

    # perform the conversation
    BotUser_dialogue_cycle(bot, "user5")

if __name__ == "__main__":
    main()