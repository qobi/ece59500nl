# https://azure.microsoft.com/en-us/products/ai-services/text-to-speech
# https://github.com/Azure-Samples/cognitive-services-speech-sdk
# https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech
# https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/quickstart/python/text-to-speech
# venv/bin/pip install azure-cognitiveservices-speech
import azure.cognitiveservices.speech as speechsdk
import keys

speech_synthesizer = None

def set_up():
    global speech_synthesizer
    speech_config = speechsdk.SpeechConfig(
        subscription=keys.azure_key,
        region=keys.azure_region)
    speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

def say(thing_to_say):
    result = speech_synthesizer.speak_text_async(thing_to_say).get()
    if result.reason==speechsdk.ResultReason.SynthesizingAudioCompleted:
        pass
    elif result.reason==speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(
            cancellation_details.reason))
        if cancellation_details.reason==speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(
                    cancellation_details.error_details))
            print("Did you update the subscription info?")
set_up()
say("This is a test of the speech synthesizer for the Purdue experimental undergraduate course in Electrical and Computer Engineering on Natural Language Processing")
say("This is a simple example.")
