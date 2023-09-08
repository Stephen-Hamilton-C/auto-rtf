#!/bin/python3

HEADER_FONTS = "Liberation Sans;Sans Serif"
HEADER_SIZE_PT = 20
CODE_FONTS = "FreeMono"
CODE_SIZE_PT = 10

import os
import sys
import re
import argparse

VERSION = "1.0.0"
SCRIPT_PATH = __file__
SCRIPT_NAME = os.path.basename(SCRIPT_PATH)

# Messages to show when first running
WELCOME_MSGS = [
        "auto-rtf.py version "+VERSION,
        "Written by Stephen Hamilton"
]
# Get the longest welcome message
longestMsg = ""
for welcomeMsg in WELCOME_MSGS:
    if len(welcomeMsg) > len(longestMsg):
        longestMsg = welcomeMsg
    print(welcomeMsg)

# Generate divider that is twice as long as the longest message
divider = ""
for char in longestMsg:
    divider += "=="
print(divider)
print()

# TODO: These should be options, rather than optional arguments
def showUsage():
    print("Usage: "+SCRIPT_NAME+" [output-file] [android-studio-project-root]")

# Validate arguments
if len(sys.argv) > 1 and sys.argv[1].lower() == "help":
    showUsage()
    exit(0)

if len(sys.argv) > 2:
    PROJECT_DIR = sys.argv[2]
    if not os.path.isdir(PROJECT_DIR):
        print("Invalid path provided.")
        showUsage()
        exit(1)
else:
    PROJECT_DIR = os.path.dirname(SCRIPT_PATH)

MAIN_PATH = os.path.join(PROJECT_DIR, "app", "src", "main")

if not os.path.exists(MAIN_PATH):
    print("Not a valid Android Studio project!")
    if len(sys.argv) > 2:
        print("Provide the path to the root of an Android Studio project")
    else:
        print("Run this script at the root of an Android Studio project")
    showUsage()
    exit(1)

if len(sys.argv) > 1:
    outputFilePath = os.path.splitext(sys.argv[1])[0]
else:
    outputFilePath = os.path.basename(PROJECT_DIR)

ktFiles = []
xmlFiles = []

for root, dirs, files in os.walk(MAIN_PATH):
    for file in files:
        if file.endswith(".kt"):
            filePath = os.path.join(root, file)
            ktFiles.append(filePath)
        elif file.endswith(".xml"):
            if root.endswith("layout") or file == "strings.xml":
                filePath = os.path.join(root, file)
                xmlFiles.append(filePath)

print("Found Kotlin files: "+str(ktFiles))
print("Found XML files: "+str(xmlFiles))

def codeToRTF(files) -> str:
    rtf = ""
    for file in files:
        # Set font size
        rtf += "\\fs"+str(round(HEADER_SIZE_PT * 2))+"\n"
        # Set font to header font
        rtf += "\\f0\n"
        # Set bold
        rtf += "\\b "
        # Insert file name to header
        rtf += os.path.basename(file)
        # End bold
        rtf += "\\b0"
        # End line
        rtf += "\\line\n"

        # Set font size for code
        rtf += "\\fs"+str(round(CODE_SIZE_PT * 2))+"\n"
        # Set font to code font
        rtf += "\\f1\n"
        with open(file, 'r') as codeFile:
            for codeFileLine in codeFile:
                rtf += re.sub("    ", "  ", codeFileLine)
                rtf += "\\line\n"
        rtf += "\\line\n"


    return rtf


rtfHeader = "{\\rtf1 "
fontTable = "{\\fonttbl {\\f0 "+HEADER_FONTS+";}{\\f1 "+CODE_FONTS+";}}\n"
rtfFooter = "}\n"

with open(outputFilePath + ".rtf", 'w') as outputFile:
    outputFile.write(rtfHeader)
    outputFile.write(fontTable)
    outputFile.write(codeToRTF(ktFiles))
    outputFile.write(codeToRTF(xmlFiles))
    outputFile.write(rtfFooter)

