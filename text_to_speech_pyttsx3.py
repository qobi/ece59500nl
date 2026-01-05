# https://azure.microsoft.com/en-us/products/ai-services/speech-to-text
# https://github.com/Azure-Samples/cognitive-services-speech-sdk
# https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-to-text
# https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/quickstart/python/from-microphone
# venv/bin/pip install pyttsx3
import pyttsx3
import threading
import time
import speech_to_text_microsoft

speech_to_text_microsoft.listen = True
speech_engine = None
things_to_say = []
stop_speech_synthesis = False

def set_up():
    global speech_engine
    speech_engine = pyttsx3.init()
    rate = speech_engine.getProperty("rate")
    speech_engine.setProperty("rate", rate-50)
    speech_engine.setProperty("voice", "english-us")
    speech_engine.setProperty("gender", "female")

def clear_things_to_say():
    global things_to_say
    things_to_say = []

def say(thing_to_say):
    things_to_say.append(thing_to_say)

def speech_synthesis_thread_function(name):
    global speech_to_text, listen, stop_speech_synthesis, things_to_say
    while not stop_speech_synthesis:
        if len(things_to_say)>0:
            thing_to_say = things_to_say[0]
            things_to_say= things_to_say[1:]
            speech_to_text_microsoft.listen = False
            speech_engine.say(thing_to_say)
            speech_engine.runAndWait()
            speech_to_text_microsoft.listen = True
        else:
            time.sleep(0.1)
    stop_speech_synthesis = False

def start():
    global speech_synthesis_thread
    set_up()
    speech_synthesis_thread = threading.Thread(
        target = speech_synthesis_thread_function, args = (None,))
    speech_synthesis_thread.start()

def stop():
    global stop_speech_synthesis
    stop_speech_synthesis = True
    speech_synthesis_thread.join()

if __name__=="__main__":
    start()
    say("This is a test of the speech synthesizer for the Purdue experimental undergraduate course in Electrical and Computer Engineering on Natural Language Processing")
    say("This is a simple example.")
    while (not speech_to_text_microsoft.listen) or len(things_to_say)>0:
        time.sleep(1)
    stop()
