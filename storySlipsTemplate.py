import os
from gpiozero import Button
import time
# for classic lit stories
import csv
import serial
import random
# for student stories
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# for gpt stories
from openai import OpenAI


#Preps system
os.system("pip install openai")
os.system("sudo chmod 666 /dev/serial0")

#put the gpio pin your button goes to here
oneButton = Button("buttonGPIO1")
twoButton = Button("buttonGPIO2")
threeButton = Button("buttonGPIO3")

# Sets up google Sheet API
# Initializing the google spreadsheet
# Fill out marked places
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('FILL OUT path to service account .json secret key', scopes=scopes)
file = gspread.authorize(creds)
workbook = file.open("FILL OUT file name for story responses")
sheet = workbook.sheet1
 
# Needed for the OpenAI API usage
client = OpenAI(api_key="FILL OUT openAI api key")

# Needed for the classic story feature
file = open('FILL OUT path for .csv file with classic storys/poems')

# Used to format text, refers to grammatical orphans, meaning words arn't split onto different lines
def orphans(text):
    lines = text.split("\\n")
    output = ""
    #print(lines)
    for line in lines:
        output+="\n"
        words = line.split(" ")
        leng = 0
        add = ""
        for word in words:
            if len(add) + len(word) > 32:
                output += add + "\n"
                add = word + " "
            else:
                add += word + " " 
        output += add
    return output


# returns student stories
def studentStories():
    print("you pressed student stories")
    # Getting response
    responseNum = (str)(random.randint(2, sheet.row_count))
    author = sheet.row_values(responseNum)[1]
    lit = sheet.row_values(responseNum)[2]
    title = sheet.row_values(responseNum)[4]
    numRows = sheet.row_count
    appropriate = sheet.row_values(responseNum)[5] # Either TRUE or FALSE

    # Appropriate check
    while appropriate != "TRUE":
        # Getting response
        responseNum = (str)(random.randint(2, sheet.row_count))
        author = sheet.row_values(responseNum)[1]
        lit = sheet.row_values(responseNum)[2]
        title = sheet.row_values(responseNum)[4]
        numRows = sheet.row_count
        appropriate = sheet.row_values(responseNum)[5] # Either TRUE or FALSE
    
    # Updates data in sheet
    sheet.update_cell(2, 8, int(sheet.cell(2,8).value) + 1)

    print("Number of entries: " + str(numRows - 1))
    print(orphans(title) + "\n" + orphans("By: " + author) + "\n" + orphans(lit) + "\n\nCC BY-NC-SA")

# returns chatGPT stories
def chatGPTStories():
    print("you pressed GPT button")
    # Writes somthing and removes punctuation that makes the string difficult
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a literature writer, skilled in writing appropriate poems, songs, and stories for a K-12 school that always starting with a title followed by a blank line."},
            {"role": "user", "content": "Compose an age appropriate poem, song, or story."}
        ]
    )
    # Outputs to console
    message = str(completion.choices[0].message)[31:-57]
    print(message + "\n\nOrphans:\n")
    print(orphans(message))
    # Updates data in sheet
    sheet.update_cell(2, 9, int(sheet.cell(2,9).value) + 1)
    
    
# returns classic lit poems
def realStories():
    print("you pressed Real stories")
    
    # Gets data from the CSV
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)
    file.close()

    # Updates data in sheet
    sheet.update_cell(2, 10, int(sheet.cell(2,10).value) + 1)

    # Returns data to be printed
    num = random.randint(0,len(rows)-1)
    print(orphans(str(rows[num][0])) + "\n" + orphans(str("By: " + rows[num][1])) + "\n" + orphans(str(rows[num][3])) + "\n")

 

# Uncomment these as for test cases
#realStories()
#chatGPTStories()
#studentStories()

while True:
    oneButton.when_pressed = studentStories()
    twoButton.when_pressed = chatGPTStories()
    threeButton.when_pressed = realStories()