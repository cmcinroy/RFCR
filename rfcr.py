# RFCR
# Tracks class attendance by recording 'enter' and 'leave' events.

# - - - - - - - - - - - - - - - - - - - - - - - - -
# Import external modules
from datetime import datetime
from gtts import gTTS
import logging
import os
import subprocess

# - - - - - - - - - - - - - - - - - - - - - - - - -
# Global variables

# Set name of temporary directory where sound files are stored
gTemp = 'temp'

# Initialize a new, empty "dictionary" variable to store student ids/names
students = {}

# Initialize a new, empty "list" variable to store ids present
idsPresent = []

# Set language (en/fr) and salutations
gLang = 'en'
salutations = {
    'en': ('Goodbye','Hello'),
    'fr': ('Au revoir','Bienvenue')
}

# Create a logger to log events
logger = logging.getLogger(__name__)


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: Main script logic
def main():
    finished = False;
    # Start a loop
    while not finished:
        # Accept input from RFID scanner (same as keyboard)
        scan = input('\nPlease scan your card:\n')
        # If someone pressed enter with no data, exit the loop
        if scan == '':
            finished = True
        elif scan == '?':
            # Dump class list
            print('{} student(s) in class:'.format(len(idsPresent)))
            for id in idsPresent:
                print('  {}'.format(students[id]))
        else:
            # Otherwise, check whether the card is registered
            if scan in students:
                # If the student is already present, this is a 'leave' event
                if scan in idsPresent:
                    leave(scan)
                # Otherwise, this is an 'enter' event
                else:
                    enter(scan)
            else:
                print('Card {} is not registered for this class.'.format(scan))


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: First things first...
def initialize():
    # Ensure temporary directory exists
    global gTemp
    gTemp = os.path.abspath(gTemp)
    os.makedirs(gTemp, exist_ok=True)
    
    # Initialize logging
    logger.setLevel(logging.INFO)
    # create a logging format for audit log
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    # create a handler for the audit log and add the formatter
    ###handler = logging.FileHandler('rfcr.log')
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    # add the handler to the logger
    logger.addHandler(handler)
    # create a logging format for graph log 
    formatter = logging.Formatter('%(message)s,%(asctime)s')
    # create a file handler for the graph log and add the formatter
    ###handler = logging.FileHandler('rfcr_graph.log')
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    # add the handler to the logger
    logger.addHandler(handler)

    # Read student list from file into our dictionary
    with open('students.dat', 'r') as datafile:
        for line in datafile:
            try:
                (id, name) = line.split(',')
                students[id] = name.rstrip()
            except ValueError:
                # ValueError occurs if the line does not have two values separated by a comma
                # If this happens, ignore this line and go on to the next line
                continue


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: A student has entered the class
def enter(id):
    idsPresent.append(id)
    print('{} entered the class.'.format(students.get(id)))
    log(1, id)


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: A student has left the class
def leave(id):
    idsPresent.remove(id)
    print('{} left the class.'.format(students.get(id)))
    log(0, id)


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: Log the event
#   opt = 1 (enter) or  0 (leave)
def log(opt, id):
    # Just print for now
    ###print('log: {},{},{},{}'.format(datetime.now(), opt, id, len(idsPresent)))
    logger.info('action={},id={},count={}'.format(opt, id, len(idsPresent)))
    # Also, "speak" the event
    speak(opt, id)


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: "Speak" a salutation based on the event and id
#   opt = 1 (enter) or  0 (leave)
def speak(opt, id):
    # Set the sound file name to "{student_name}_{opt}_{lang}.mp3" (in temp directory)
    fname = os.path.join(gTemp, students.get(id).replace(' ', '_') + '_' + str(opt) + '_' + gLang + '.mp3')
    # If the necessary sound file doesn't already exist, create it
    if not os.path.isfile(fname):
        # Phrase to be spoken is "{salutation} {student name}"
        phrase = salutations.get(gLang)[opt] + ' ' + students.get(id) + '.'
        try:
            tts = gTTS(text=phrase, lang=gLang)
            # Save spoken sound to file
            tts.save(fname)
        except:
            # Ignore any erros
            pass
    # Play the sound file (in a subprocess, so we don't wait while the file plays)
    try:
        subprocess.Popen("mpg123 -q " + fname)
    except:
        # Ignore any errors
        pass


# = = = = = = = = = = = = = = = = = = = = = = = = =
# Main program
# - - - - - - - - - - - - - - - - - - - - - - - - -

initialize()
main()
