# RFCR
# Tracks class attendance by recording 'enter' and 'leave' events.

# import external modules
from datetime import datetime
from gtts import gTTS
import os

# initialize a new, empty "dictionary" variable to store student ids/names
students = {}

# initialize a new, empty "list" variable to store ids present
idsPresent = []

# set language (en/fr) and salutations
gLang = 'en'
salutations = {
    'en': ('Goodbye','Hello'),
    'fr': ('Au revoir','Bienvenue')
}


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: a student has entered the class
def enter(id):
    idsPresent.append(id)
    print('{} entered the class.'.format(students.get(id)))
    log(1, id)


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: a student has left the class
def leave(id):
    idsPresent.remove(id)
    print('{} left the class.'.format(students.get(id)))
    log(0, id)


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: log the event
#   opt = 1 (enter) or  0 (leave)
def log(opt, id):
    # just print for now
    print('log: {},{},{},{}'.format(datetime.now(), opt, id, len(idsPresent)))
    # Also, "speak" the event
    speak(opt, id)


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: "speek" a salutation for the event
#   opt = 1 (enter) or  0 (leave)
def speak(opt, id):
    # Set the sound file name to "{student_name}_{opt}_{lang}.mp3"
    fname = students.get(id).replace(' ', '_') + '_' + str(opt) + '_' + gLang + '.mp3'
    if not os.path.isfile(fname):
        # Phrase to be spoken is "{salutation} {student name}"
        phrase = salutations.get(gLang)[opt] + ' ' + students.get(id) + '.'
        tts = gTTS(text=phrase, lang=gLang)
        # Save spoken sound to file
        tts.save(fname)
    # Play the sound file
    os.system("mpg123 -q " + fname)



# = = = = = = = = = = = = = = = = = = = = = = = = =
# Main program
# - - - - - - - - - - - - - - - - - - - - - - - - -

# read student list from file into our dictionary
with open('students.dat', 'r') as datafile:
    for line in datafile:
        (id, name) = line.split(',')
        students[id] = name.rstrip()

# start a loop
finished = False;
while not finished:
    # accept input from RFID scanner (same as keyboard)
    scan = input('\nPlease scan your card:\n')
    # if someone pressed enter with no data, exit the loop
    if scan == '':
        finished = True
    elif scan == '?':
        # Dump class list
        print('{} student(s) in class:'.format(len(idsPresent)))
        for id in idsPresent:
            print('  {}'.format(students[id]))
    else:
        # otherwise, check whether the card is registered
        if scan in students:
            # if the student is already present, this is a 'leave' event
            if scan in idsPresent:
                leave(scan)
            # otherwise, this is an 'enter' event
            else:
                enter(scan)
        else:
            print('Card {} is not registered for this class.'.format(scan))
