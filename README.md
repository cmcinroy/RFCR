RF Class Registrator
====================

##Objective
Build a RFID-based student register/attendance system for classroom use.

##Features
- Tracks students entering and leaving classroom
- Configurable list of id card assigments to students
- Visual feedback:
  - Displays students name and event (enter/leave)
  - Displays number of students in class
  - Displays current class register
- Audio feedback: an event-appropriate salutation is "spoken" to the student

##Technologies
###Hardware
- Raspberry Pi Zero
- USB RFID card reader, with RFID card(s)/fob(s)

###Software
- Python scripting language
- Google Text-to-speech (TTS) engine

##Future
- graphing number of students in class over time

##Install
### Prerequisites
- Python 3 (and pip)
- pip3 install gTTS --user
- Ensure audio is directed to HDMI output:
```
  sudo nano /boot/config.txt
```
- ... and uncomment the following line:
```
    hdmi_drive=2
```

###Linux
- Ensure distro is up to date:
```
  sudo apt-get clean
  sudo apt-get autoremove
  sudo apt-get update
  sudo apt-get upgrade
```
- Ensure the alsa sound utilities are installed:
```
  sudo apt-get install alsa-utils
```
- ... and ensure that /etc/modules has the following line:
```
    snd_bcm2835
```

- Install mpg123 audio player:
```
  sudo apt-get install mpg123
```
(Per [RPi Text to Speech (Speech Synthesis) - eLinux.org](http://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)).)

###Windows
- Download and install [mpg123](https://www.mpg123.de) (static build)


##License
RFCR is free software: you can redistribute it and/or modify it under the terms of the [GNU General Public License](http://www.gnu.org/licenses/gpl.html) as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

RFCR is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
