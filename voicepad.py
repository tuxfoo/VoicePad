import speech_recognition as sr
import playsound as snd
import json
import random
import keyboard
import mouse
import time
import threading

with open('kate.json') as file:
    data = json.load(file)

sounds = '/home/jacob/Music/Sounds/hcspack-KATE/'
r = sr.Recognizer()
phrase = ""
disabled_categories = []
# Set to one to enable the online speech api
online_api = 1


def respond(words):
    global sounds
    global phrase
    for trigger in data['triggers']:
        phrase = ""
        if not is_disabled(trigger["Categories"]):
            if check_pattern(words, trigger['patterns']) and phrase.lower() in words and phrase != "":
                print("Event Triggered: " + trigger['Name'] + " Matched Phrase: " + phrase)
                if type(trigger['Command']) == list:
                    # Maybe use threading to run this in background?
                    # Maybe make running in background optional via json config?
                    if trigger['Command'][0] != "background=False":
                        cmd_thread = threading.Thread(target=run_cmd, args=[trigger['Command']])
                        cmd_thread.start()
                    else:
                        run_cmd(trigger['Command'])
                if trigger['Files'] != "none":
                    snd.playsound(sounds + random.choice(trigger['Files']))


def check_pattern(words, patterns):
    global phrase
    hit = False
    for pattern in patterns:
        print("Last Phrase: " + phrase)
        if type(pattern) == list:
            if not check_pattern(words, pattern):
                return False
            hit = True
        elif phrase == "":
            if contains_phrase(words, pattern.lower()):
                hit = True
                phrase = pattern.lower()
        elif contains_phrase(words, (phrase + " " + pattern).lower()):
            hit = True
            phrase += " " + pattern.lower()
        if pattern == patterns[-1] and not hit:
            return False
    return True


def contains_phrase(s, w):
    if (' ' + w + ' ') in (' ' + s + ' '):
        return True
    return False


def disable_cat(cat):
    global disabled_categories
    for c in disabled_categories:
        if c == cat:
            # Already disabled
            return
    disabled_categories.append(cat)


def enable_cat(cat):
    global disabled_categories
    if is_disabled(cat):
        disabled_categories.remove(cat)


def is_disabled(cat):
    global disabled_categories
    for c in disabled_categories:
        if c == cat:
            return True
    return False


def run_cmd(commands):
    global sounds
    # This function will take a list of commands and tasks to execute
    # It does not do much at the moment.
    # Maybe use threading to do this in background?
    for cmd in commands:
        # The commands will be performed in this loop
        cmd2 = cmd.split("=")
        print(cmd2)
        if cmd2[0] == "wait":
            # Will take a integer and wait that amount of time
            time.sleep(int(cmd2[1]))
        elif cmd2[0] == "keypress_release":
            # Will take a key, which will be pressed and released
            keyboard.press_and_release(cmd2[1])
        elif cmd2[0] == "play":
            # Will take a sound file, and play it
            snd.playsound(sounds + cmd2[1])
        elif cmd2[0] == "disable-cat":
            # Will disable category.
            disable_cat(cmd2[1])
        elif cmd2[0] == "enable-cat":
            # Enables a category
            enable_cat(cmd2[1])
        elif cmd2[0] == "mouse_click":
            # Clicks a given mouse button
            mouse.click(button=cmd2[1])


while True:
    with sr.Microphone() as source:
        print("Listening")
        r.adjust_for_ambient_noise(source, duration=1)
        answer = r.listen(source, phrase_time_limit=4)
        try:
            if online_api == 1:
                ai = r.recognize_wit(answer, key="AJFK24SWSLG2CSKDB2AYRJQWIM47HVFB")
            ans = r.recognize_sphinx(answer)
            if ai != "":
                print("-----YOU SAID------")
                print("pocketphinx: " + ans)
                if online_api == 1:
                    print("wit: " + ai)
                print("-------------------")
                start = time.time()
                if online_api == 1:
                    respond(ai.lower())
                else:
                    respond(ans.lower())
                end = time.time()
                print("Respond took: " + str(end - start) + " seconds")
            phrase = ""
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
