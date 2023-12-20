import openai
import pyttsx3
import speech_recognition as s1
import time

openai.api_key = "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"

engine = pyttsx3.init()

def audio_to_text(filename):
    recognizer = s1.Recognizer()
    with s1.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping unknown error')

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-803",
        prompt=prompt,
        max_token = 4000,
        n=1,
        stop=None,
        temperature = 0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        print("Say 'Genius' ")
        with s1.Microphone() as source:
            recognizer = s1.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "genius":
                    filename = "input.wav"
                    print("Say your question...")
                    with s1.Microphone() as source:
                        recognizer = s1.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename,"wb") as f:
                            f.write(audio.get_wav_data())

                            text  = audio_to_text(filename)
                            if text:
                                print(f"You said : {text}")

                                response = generate_response(text)
                                print(f"GPT-3 Says : {response}")

                                speak_text(response)
            except Exception as e:
                print("An error occurred : {}".format(e))
if __name__ == "__main__":
    main() 