RF Class Registrator
====================

## Objective
Build a RFID-based student register/attendance system for classroom use.

## Features
- Tracks students entering and leaving classroom
- Configurable list of id card assigments to students
- Visual feedback:
  - Displays students name and event (enter/leave)
  - Displays number of students in class
  - Displays current class register
- Audio feedback: an event-appropriate salutation is "spoken" to the student
- Save/load (and clear) state
- Graph number of students in class over time

## Technologies
### Hardware
- Raspberry Pi Zero
- USB RFID card reader, with RFID card(s)/fob(s)

### Software
- Python scripting language
- Google Text-to-speech (TTS) engine
- Bokeh visualization library (graphing)

## Future
- TBD


## License
RFCR is free software: you can redistribute it and/or modify it under the terms of the [GNU General Public License](http://www.gnu.org/licenses/gpl.html) as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

RFCR is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
