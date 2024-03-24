# StoryBox
Code Necessary for the operation of a StoryBox story printer

## Table of Contents 
### Running on Start
### Making sure modules are downloaded 
### Potential Errors

## Running on Start

## Making sure modules are downloaded
Please note that these are the only modules that were not preinstalled on my raspberry pi, 
and that in some cases, you may have to install other modules in addition to those listed below.

### Gspread
Install the gspread module by using: 
pip install gspread

### oauth2client
Install the oauth2client module by using: 
pip install oauth2client

### openai
Install the openai module by using: 
pip install openai

## Potential Errors:
### "externally-managed-environment" while importing modules
when pip install MODULE_NAME
use pip install MODULE_NAME --break-system-packages 

### "cannot create /dev/serial0: Permission denied" when trying to print through printer
Make sure serial port is turned on in settings for raspberry pi

