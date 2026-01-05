import text_to_speech_microsoft
import speech_to_text_microsoft
import eliza
import time

done = False
eliza = eliza.Eliza()
written = True

eliza.load('doctor.txt')

def say(utterance):
    text_to_speech_microsoft.say(utterance)
    if written:
        print(utterance)

def process_utterance(said):
    global done
    if written:
        print(said)
    response = eliza.respond(said.lower()[:-1])
    time.sleep(1)
    if response is None:
        done = True
    else:
        say(response)

speech_to_text_microsoft.process_utterance = process_utterance

text_to_speech_microsoft.start()
speech_to_text_microsoft.start()
time.sleep(1)

say(eliza.initial())
while not done:
    time.sleep(1)
say(eliza.final())
while ((not speech_to_text_microsoft.listen) or
       len(text_to_speech_microsoft.things_to_say)>0):
    time.sleep(1)

speech_to_text_microsoft.stop()
text_to_speech_microsoft.stop()
