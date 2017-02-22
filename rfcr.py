# RFCR
# Tracks class attendance by recording 'enter' and 'leave' events.

# import external modules
from datetime import datetime

# initialize a new, empty "dictionary" variable to store student ids/names
students = {}

# initialize a new, empty "list" variable to store ids present
idsPresent = []


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: a student has entered the class
def enter(id):
    idsPresent.append(id)
    print('{} entered the class.'.format(students.get(id)))
    speak('Hello, ' + students.get(id) + '.')
    log(1, id)


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: a student has left the class
def leave(id):
    idsPresent.remove(id)
    print('{} left the class.'.format(students.get(id)))
    speak('Goodbye, ' + students.get(id) + '.')
    log(0, id)


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: log the event
#   opt = 1 (enter) or  0 (leave)
def log(opt, id):
    # just print for now
    print('log: {},{},{},{}'.format(datetime.now(), opt, id, len(idsPresent)))


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: convert the text to "speech"
def speak(text):
    # just print for now
    print('speak: ' + text)


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
