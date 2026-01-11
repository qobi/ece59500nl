import text_to_speech_microsoft
import speech_to_text_microsoft
import os
# venv/bin/pip install openai
import openai
import time
import keys

done = False
written = True
client = openai.AzureOpenAI(azure_endpoint=keys.azure_openai_endpoint,
                            api_key=keys.azure_openai_key,
                            api_version=keys.azure_openai_api_version)
discourse = [{"role": "system",
              "content":
              "I am an instructor of the Purdue experimental undergraduate course in Electrical and Computer Engineering on Natural Language Processing"}]

def gpt(request):
    discourse.append({"role": "user", "content": request})
    chat = client.chat.completions.create(
        messages = discourse, model = "gpt-4")
    reply = chat.choices[0].message.content
    discourse.append({"role": "assistant", "content": reply})
    return reply

def say(utterance):
    text_to_speech_microsoft.say(utterance)
    if written:
        print(utterance)

def process_utterance(said):
    global done
    if written:
        print(said)
    if "bye" in said:
        done = True
    else:
        response = gpt(said)
        time.sleep(1)
        say(response)

speech_to_text_microsoft.process_utterance = process_utterance

text_to_speech_microsoft.start()
speech_to_text_microsoft.start()
time.sleep(1)

say("How do you do.  Please tell me your problem.")
while not done:
    time.sleep(1)
say("Goodbye.")
while ((not speech_to_text_microsoft.listen) or
       len(text_to_speech_microsoft.things_to_say)>0):
    time.sleep(1)

text_to_speech_microsoft.stop()
speech_to_text_microsoft.stop()
