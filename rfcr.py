# RFCR
# Tracks attendance by recording 'enter' and 'leave' actions.

# initialize a new, empty "dictionary" variable to store student ids/names
students = {}

# initialize a new, empty "list" variable to store ids present
idsPresent = []

# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: a student has entered the class
def enter():
    log(1)
    print('{} entered the class.'.format(students.get(scan)))
    idsPresent.append(scan)

# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: a student has left the class
def leave():
    log(0)
    print('{} left the class.' .format(students.get(scan)))
    idsPresent.remove(scan)

# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: log the action
def log(opt):
    # do nothing for now
    opt = 0
    

# - - - - - - - - - - - - - - - - - - - - - - - - -
# Main program
#
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
    else:
        # otherwise, check whether the card is registered
        if scan in students:
            # if the student is already present, call the leave() function
            if scan in idsPresent:
                leave()
            # otherwise, call the enter() function
            else:
                enter()
        else:
            print('Card {} is not registered for this class.'.format(scan))
