# https://azure.microsoft.com/en-us/products/ai-services/speech-to-text
# https://github.com/Azure-Samples/cognitive-services-speech-sdk
# https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-to-text
# https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/quickstart/python/from-microphone
# venv/bin/pip install azure-cognitiveservices-speech
import azure.cognitiveservices.speech as speechsdk
import threading
import time
import keys

listen = True
speech_recognizer = None
error_in_s2t_session = False
utterance_fragments = []
stop_speech_recognition = False
done = False

def handle_final_result(evt):
    response = "".join([i if ord(i)<128 else " " for i in evt.result.text])
    utterance_fragments.append(response)

def handle_error(evt):
    global error_in_s2t_session
    error_in_s2t_session = True

def handle_intermediate_result(evt):
    global beginning_of_silence
    beginning_of_silence = time.time()

def speech_recognition_thread_function(name):
    global speech_recognizer, utterance_fragments, beginning_of_silence
    global error_in_s2t_session, stop_speech_recognition
    while not stop_speech_recognition:
        reconnect_time = 0.0
        while listen and not stop_speech_recognition:
            time.sleep(reconnect_time)
            try:
                if speech_recognizer==None:
                    speech_config = speechsdk.SpeechConfig(
                        subscription=keys.azure_key,
                        region=keys.azure_region)
                    audio_config = speechsdk.audio.AudioConfig(
                        device_name="pipewire")
                    speech_recognizer = speechsdk.SpeechRecognizer(
                        speech_config=speech_config, audio_config=audio_config)
                    speech_recognizer.recognized.connect(handle_final_result)
                    speech_recognizer.canceled.connect(handle_error)
                    speech_recognizer.recognizing.connect(
                        handle_intermediate_result)
                utterance_fragments = []
                beginning_of_silence = time.time()
                speech_recognizer.start_continuous_recognition()
                while (listen and
                       not error_in_s2t_session and
                       not stop_speech_recognition):
                    now = time.time()
                    if len(utterance_fragments)>0:
                        sanitized_utterance = ""
                        for c in " ".join(utterance_fragments).strip():
                            if 0<=ord(c)<=127:
                                sanitized_utterance += c
                        if sanitized_utterance=="":
                            time.sleep(0.1)
                            continue
                        utterance_fragments = []
                        process_utterance(sanitized_utterance)
                    time.sleep(0.1)
                speech_recognizer.stop_continuous_recognition_async()
                error_in_s2t_session = False
            except Exception as e:
                reconnect_time += 0.1
            time.sleep(0.1)
        if not listen:
            time.sleep(0.1)
    stop_speech_recognition = False

def start():
    global speech_recognition_thread
    speech_recognition_thread  = threading.Thread(
        target = speech_recognition_thread_function, args = (None,))
    speech_recognition_thread.start()

def stop():
    global stop_speech_recognition
    stop_speech_recognition = True
    speech_recognition_thread.join()

if __name__=="__main__":
    def process_utterance(utterance):
        global done
        utterance = utterance.lower()
        print(utterance)
        if "bye" in utterance:
            done = True

    start()
    while not done:
        time.sleep(1)
    stop()
