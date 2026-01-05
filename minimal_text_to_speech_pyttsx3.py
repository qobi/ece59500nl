# venv/bin/pip install pyttsx3
import pyttsx3

speech_engine = None

def set_up():
    global speech_engine
    speech_engine = pyttsx3.init()
    rate = speech_engine.getProperty("rate")
    speech_engine.setProperty("rate", rate-50)
    speech_engine.setProperty("voice", "english-us")
    speech_engine.setProperty("gender", "female")

def say(thing_to_say):
    speech_engine.say(thing_to_say)
    speech_engine.runAndWait()

set_up()
say("This is a test of the speech synthesizer for the Purdue experimental undergraduate course in Electrical and Computer Engineering on Natural Language Processing")
say("This is a simple example.")
