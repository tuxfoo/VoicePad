import speech_recognition as sr
import playsound as snd
import json
import random

with open('kate.json') as file:
    data = json.load(file)

sounds = '/home/jacob/Music/Sounds/hcspack-KATE/'

r = sr.Recognizer()
phrase = ""


def respond(words):
    global sounds
    for trigger in data['triggers']:
        if check_pattern(words, trigger['patterns']) and phrase.lower() in words and phrase != "":
            print("It works")
            if trigger['Files'] != "none":
                snd.playsound(sounds + random.choice(trigger['Files']))
            run_cmd(trigger['Command'])


def check_pattern(words, patterns):
    global phrase
    hit = False
    for pattern in patterns:
        if type(pattern) == list:
            if not check_pattern(words, pattern):
                return False
        elif phrase == "":
            if pattern.lower() in words:
                hit = True
                phrase = pattern
        elif phrase + " " + pattern.lower() in words:
            hit = True
            phrase += " " + pattern
        elif pattern == patterns[-1] and not hit:
            return False
    return True


def run_cmd(commands):
    # This function will take a list of commands and tasks to execute
    if type(commands) != list:
        return
    for cmd in commands:
        # The commands will be performed in this loop
        # Maybe use a dictionary???
        if cmd == "wait":
            # Will wait
            pass
        elif cmd == "keybind":
            # Will forward keystroke to SC
            pass
        elif cmd == "play":
            # Will play a file
            pass
        elif cmd == "disable-cat":
            # Will disable catagory.
            pass


while True:
    with sr.Microphone() as source:
        print("Listening")
        r.adjust_for_ambient_noise(source, duration=1)
        answer = r.listen(source, phrase_time_limit=4)
        try:
            ai = r.recognize_wit(answer, key="AJFK24SWSLG2CSKDB2AYRJQWIM47HVFB")
            ans = r.recognize_sphinx(answer)
            print(ans)
            print(ai)
            respond(ai.lower())
            phrase = ""
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
