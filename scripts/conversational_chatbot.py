from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyDH-GaIM0HOch9haCtqxGy6yKQ2uqU-1UY")
chat = client.chats.create(model="gemini-2.5-flash",
                               config=types.GenerateContentConfig(system_instruction=f"""You are a professional mood assistant who help users based on their mood.

                                   Your tone must be civil and professional.
                                   If the user asks you to do anything outside helping them get over their mood, you must kindly decline.
                                   If the user asks you to do something that is morally or socially unacceptable, you must kindly decline.
                                   All your responses must be logically driving towards helping the user
                                   You must must not bore the user with long-form responses. Say more in less words.
                                   You only speak and understand the English language

                                   """,
                                                                  max_output_tokens=5000
                                                                  ))


def chat_with_model(emotion, user_message):

    if user_message is None:
        message_prompt = f"The user is ```{emotion}```"
        response = chat.send_message(message_prompt)
        return response.text
    else:
        response = chat.send_message(user_message)
        return response.text

