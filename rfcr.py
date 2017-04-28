# RFCR
# Radio Frequency Class Registrator
#
# Tracks class attendance by recording 'enter' and 'exit' events.

# - - - - - - - - - - - - - - - - - - - - - - - - -
# Import local modules
from phrases import *
# Import external modules
from datetime import datetime
from gtts import gTTS
import hashlib
import json
from json import JSONDecoder, JSONEncoder
import logging
import os
import subprocess

# - - - - - - - - - - - - - - - - - - - - - - - - -
# Global variables

# Set language (en/fr)
language = 'en'

# Set name of student data file
DATA_FILE = 'students.dat'

# Set name of temporary directory where state and log and sound files are stored
TEMP_DIR = 'temp'

# Set names of log files
LOG_FILE = os.path.join(TEMP_DIR, 'rfcr.log')
LOG_GRAPH_FILE = os.path.join(TEMP_DIR, 'rfcr_graph.log')

# Set name of temporary file where current state is stored
STATE_FILE = os.path.join(TEMP_DIR, 'state.json')

# Initialize student data file checksum
data_check = ''

# Initialize a new, empty "dictionary" variable to store student ids/names
students = {}

# Set the list of states and the corresponding action names
student_states = ['absent', 'present']
actions = ['enter', 'exit']

# Initialize dictionary variable to store absent/present ids (and the date/time of exit/entry)
#   ids['absent'] will return a dictionary of students that have left (key=id, value=date/time of exit)
#   ids['present'] will return a dictionary of students that have entered (key=id, value=date/time of entry)
# ids = {'absent': {}, 'present': {}}
ids = {key: {} for key in student_states}
# Create a "view" of student ids that are present in class
ids_present = ids[student_states[1]].keys()

# Initialize dictionary to store current state
state = {}

# Create a logger to log events
logger = logging.getLogger(__name__)


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: Main script logic
def main():
    finished = False
    confirm = False
    # Start a loop
    while not finished:
        # Accept input from RFID scanner (same as keyboard)
        scan = input('\n%s:\n' % (phrases.get(language)[PHRASE_INPUT]))
        # If someone pressed enter with no data, exit the loop
        if scan == '':
            finished = True
        elif scan == '=':
            # Clear everything? (if confirmed)
            if confirm:
                # Clear current state
                clear_state()
                confirm = False
                finished = True
            else:
                print(phrases.get(language)[PHRASE_RESET_CONFIRM])
                confirm = True
        elif scan == '?':
            print_state()
            confirm = False
        else:
            # Otherwise, check whether the card is registered
            if scan in students:
                # "Toggle" the current status of the student (present/absent)
                toggle(scan, datetime.today())
            else:
                print(phrases.get(language)[PHRASE_NOTREG].format(scan))
            confirm = False
    # Save current state before exit
    save_state()


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: Toggle state (present/absent) for the specified card id
def toggle(id, event_time):
    # Determine current status (0/false = absent, 1/true = present)
    current = id in ids_present

    # Create a message for the action (student name + action phrase)
    message = [students.get(id), phrases.get(language)[current + PHRASE_ACTION]]
    # Remove from current list and get the previous action event time (if any)
    prev_time = ids.get(student_states[current]).pop(id, 0)
    # Calculate and display difference in time between last action and current
    if (prev_time != 0):
        time_diff = event_time - prev_time
        message.append("(%s %s)" % (phrases.get(language)[current + PHRASE_DELTA], format_timedelta(time_diff)))
    # Print a message for the event
    print(' '.join(message) + ".")

    # Flip status and update class register with event time
    new_state = not current
    ids.get(student_states[new_state])[id] = event_time

    # Log the event
    log(int(current), id, event_time)
    # Also, "speak" the event
    speak(int(current), id)


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: Return a string that represents the value of the specified timedelta
def format_timedelta(td):
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    message = []
    if (td.days > 0):
        message.append("%d %s" % (td.days, phrases.get(language)[PHRASE_DAYS]))
    if (hours > 0):
        message.append("%d %s" % (hours, phrases.get(language)[PHRASE_HRS]))
    if (minutes > 0):
        message.append("%d %s" % (minutes, phrases.get(language)[PHRASE_MINS]))
    if (seconds > 0):
        message.append("%d %s" % (seconds, phrases.get(language)[PHRASE_SECS]))
    return ' '.join(message)


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: Log the event
def log(state, id, event_time):
    # Log the relevant data for the event
    logger.info(students.get(id), extra={'event_time': event_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], 
        'action': actions[state], 'id': id, 'count': len(ids_present)})


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: "Speak" a salutation based on the event and id
def speak(state, id):
    # Set the sound file name to "{student_name}_{opt}_{lang}.mp3" (in temp directory)
    fname = os.path.join(TEMP_DIR, students.get(id).replace(' ', '_') + '_' + str(state) + '_' + language + '.mp3')
    # If the necessary sound file doesn't already exist, create it
    if not os.path.isfile(fname):
        # Phrase to be spoken is "{salutation} {student name}"
        phrase = phrases.get(language)[state] + ' ' + students.get(id) + '.'
        try:
            tts = gTTS(text=phrase, lang=language)
            # Save spoken sound to file
            tts.save(fname)
        except:
            # Ignore any erros
            pass
    # Play the sound file (in a subprocess, so we don't wait while the file plays)
    try:
        subprocess.Popen("mpg123 -q " + fname, shell=True)
    except:
        # Ignore any errors
        pass


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: First things first...
def initialize():
    # Ensure temporary directory exists
    global TEMP_DIR, data_check
    TEMP_DIR = os.path.abspath(TEMP_DIR)
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # Initialize logging
    logger.setLevel(logging.DEBUG)
    # create a logging format for audit log
    formatter = logging.Formatter('%(event_time)s - %(levelname)s - %(message)s (%(id)s) - %(action)s - %(count)s')
    # create a handler for the audit log and add the formatter
    handler = logging.FileHandler(LOG_FILE)
    ###handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    # add the handler to the logger
    logger.addHandler(handler)
    # create a logging format for graph log 
    formatter = logging.Formatter('%(event_time)s,%(count)s')
    # create a file handler for the graph log and add the formatter
    handler = logging.FileHandler(LOG_GRAPH_FILE)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    # add the handler to the logger
    logger.addHandler(handler)
    
    # Check for previously saved state
    if os.path.isfile(STATE_FILE):
        load_state()
    
    # Initialize our checksum
    check = hashlib.sha1()
    # Read student list from file into our dictionary
    print(phrases.get(language)[PHRASE_DATA_READ], end='')
    with open(DATA_FILE, 'r') as datafile:
        for line in datafile:
            try:
                # Update checksum with next line of data
                check.update(line.encode())
                # Split the line into two: before/after comma
                (id, name) = line.split(',')
                # Add the id/name to the student list; strip extra characters from the end of the name
                students[id] = name.rstrip()
                print('.', end='')
            except ValueError:
                # ValueError occurs if the line does not have two values separated by a comma
                # If this happens, ignore this line and go on to the next line
                continue
    print(phrases.get(language)[PHRASE_DATA_COMPLETE])
    # Compare checksums
    #   Note that saved state should be invalidated if the student list changes.
    #   We calculate a check ('checksum') on the student data as it is loaded, and
    #   warn that the checksum/data has changed.
    #   Warning allows the user to decide whether changes to student list
    #   are ok (e.g. new student) or might cause conflicts with saved state 
    #   (e.g. id card changed from one student to another).
    if (data_check != '') and (data_check != check.hexdigest()) and ('ids' in state):
        print(phrases.get(language)[PHRASE_WARN_DATA_CHECK])
    data_check = check.hexdigest()



# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: Print the current class register
def print_state():
    # Dump list of students present in class
    print(phrases.get(language)[PHRASE_QUERY].format(len(ids_present)))
    for id in ids_present:
        print('  {}'.format(students[id]))


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: Save variables to a file
def save_state():
    global state
    # Send a message to the log
    logger.debug('save_state', extra={'event_time': datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], 
        'action': 'save', 'id': '', 'count': ''})
    # Show message indicating whether there are students present in class
    if len(ids_present) > 0:
        print(phrases.get(language)[PHRASE_STATE_NOT_EMPTY])
    else:
        print(phrases.get(language)[PHRASE_STATE_EMPTY])
    # Save important variables in state dictionary
    state['data_check'] = data_check
    # Only save ids/states/events if actions have occurred
    if (ids[student_states[0]]) or (ids[student_states[1]]):
        state['ids'] = ids
        print(phrases.get(language)[PHRASE_STATE_SAVE])
    else:
        # Otherwise, ensure ids/states/events are not saved
        if ('ids' in state):
            del state['ids']
    try:
        # Open the state file for writing
        state_file = open(STATE_FILE, 'w')
        # Save the dictionary to file
        json.dump(state, state_file, cls=JSONDateTimeEncoder)
    except:
        # If there are any errors, reset
        print(phrases.get(language)[PHRASE_ERR_STATE_SAVE])
        clear_state()


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: Load variables from a file
def load_state():
    global state, data_check, ids, ids_present
    # Send a message to the log
    logger.debug('load_state', extra={'event_time': datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], 
        'action': 'load', 'id': '', 'count': ''})
    try:
        # Open the state file for reading
        state_file = open(STATE_FILE, 'r')
        # Load the contents of the file into a dictionary
        state = json.load(state_file, cls=JSONDateTimeDecoder)
        # Load variables from dictionary
        data_check = state['data_check']
        if ('ids' in state):
            # Only display message if ids/states/events are being restored
            print(phrases.get(language)[PHRASE_STATE_LOAD])
            ids.update(state['ids'])
            # (must also update dictionary view)
            ids_present = ids[student_states[1]].keys()
    except:
        # If there are any errors, reset
        print(phrases.get(language)[PHRASE_ERR_STATE_READ])
        clear_state()


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Function: Clear current state
def clear_state():
    global state, ids, ids_present, logger
    # Send a message to the log
    logger.debug('clear_state', extra={'event_time': datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], 
        'action': 'clear', 'id': '', 'count': ''})
    # clear state and ids dictionaries
    state.clear()
    ids = {key: {} for key in student_states}
    # (must also update dictionary view)
    ids_present = ids[student_states[1]].keys()
    try:
        # close all logging handlers
        handlers = logger.handlers.copy()
        for h in handlers:
            logger.removeHandler(h)
            h.flush()
            h.close()
        # remove state file
        if os.path.isfile(STATE_FILE):
            os.remove(STATE_FILE)
        # remove log file???
        # if os.path.isfile(LOG_FILE):
            # os.remove(LOG_FILE)
        # clear graph log file
        with open(LOG_GRAPH_FILE, 'w'):
            pass
    except:
        # If there are any errors, advise user
        print(phrases.get(language)[PHRASE_ERR_STATE_FILE])
    else:
        print(phrases.get(language)[PHRASE_RESET])


# - - - - - - - - - - - - - - - - - - - - - - - - -
# Class: Allow conversion from datetime variable to string
#        Used when saving the current state to file
#        see: https://gist.github.com/abhinav-upadhyay/5300137
class JSONDateTimeDecoder(json.JSONDecoder):

    def __init__(self, *args, **kargs):
        JSONDecoder.__init__(self, object_hook=self.dict_to_object,
                             *args, **kargs)
    
    def dict_to_object(self, d): 
        if '__type__' not in d:
            return d

        type = d.pop('__type__')
        try:
            dateobj = datetime(**d)
            return dateobj
        except:
            d['__type__'] = type
            return d

# - - - - - - - - - - - - - - - - - - - - - - - - -
# Class: Allow conversion from string variable to datetime
#        Used when loading the current state from file
class JSONDateTimeEncoder(JSONEncoder):
    """ Instead of letting the default encoder convert datetime to string,
        convert datetime objects into a dict, which can be decoded by the
        DateTimeDecoder
    """
        
    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                '__type__' : 'datetime',
                'year' : obj.year,
                'month' : obj.month,
                'day' : obj.day,
                'hour' : obj.hour,
                'minute' : obj.minute,
                'second' : obj.second,
                'microsecond' : obj.microsecond,
            }   
        else:
            return JSONEncoder.default(self, obj)


# = = = = = = = = = = = = = = = = = = = = = = = = =
# Main program
# - - - - - - - - - - - - - - - - - - - - - - - - -

initialize()
main()
