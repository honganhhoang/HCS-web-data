import gradio as gr
import random
import time

with gr.Blocks(fill_height=True) as demo:
    gr.Markdown(
    """
    # Hello World!
    Start typing below to see the output.
    """)
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Type your message.")
    clear = gr.Button("Exit")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(message, history):
        bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
        history[-1][1] = ""
        for character in bot_message:
            history[-1][1] += character
            time.sleep(0.05)
            yield history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, [msg, chatbot], chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)



demo.launch()
