import speech_recognition as sr
import playsound as snd
import json
import random
import keyboard
import time

with open('kate.json') as file:
    data = json.load(file)

sounds = '/home/jacob/Music/Sounds/hcspack-KATE/'
r = sr.Recognizer()
phrase = ""
k = keyboard


def respond(words):
    global sounds
    global phrase
    for trigger in data['triggers']:
        phrase = ""
        if check_pattern(words, trigger['patterns']) and phrase.lower() in words and phrase != "":
            print("Event Triggered: " + trigger['Name'])
            run_cmd(trigger['Command'])
            if trigger['Files'] != "none":
                snd.playsound(sounds + random.choice(trigger['Files']))


def check_pattern(words, patterns):
    global phrase
    hit = False
    for pattern in patterns:
        if type(pattern) == list:
            if not check_pattern(words, pattern):
                return False
        elif phrase == "":
            if contains_phrase(words, pattern.lower()):
                hit = True
                phrase = pattern.lower()
        elif contains_phrase(words, (phrase + " " + pattern).lower()):
            hit = True
            phrase += " " + pattern.lower()
        elif pattern == patterns[-1] and not hit:
            return False
    return True


def contains_phrase(s, w):
    if (' ' + w + ' ') in (' ' + s + ' '):
        return True
    return False


def run_cmd(commands):
    global sounds
    # This function will take a list of commands and tasks to execute
    # It does not do anything at the moment, it is here for planning features.
    if type(commands) != list and commands != "none":
        return
    for cmd in commands:
        # The commands will be performed in this loop
        cmd2 = cmd.split("=")
        print(cmd2)
        if cmd2[0] == "wait":
            # Will take a interger and wait that amount of time
            time.sleep(int(cmd2[1]))
        elif cmd2[0] == "keybind":
            # Will take a string, which will be entered on a virtual keyboard
            keyboard.press_and_release(cmd2[1])
        elif cmd2[0] == "play":
            # Will take a file, and play it
            snd.playsound(sounds + cmd2[1])
        elif cmd == "disable-cat":
            # Will disable catagory.
            # Maybe add disabled catagories to a list so they can be ignored?
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
