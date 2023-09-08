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



# Setup argument parser
def getDefaultOutputFile():
    parentDir = os.path.dirname(SCRIPT_PATH)
    parentDirName = os.path.basename(parentDir)
    if parentDirName.startswith(".") and parentDirName.endswith("."):
        parentDirName = os.path.basename(os.path.dirname(parentDir))

    return parentDirName + ".rtf"

parser = argparse.ArgumentParser(description="Compiles all Kotlin and relevant XML files from an Android Studio project and stuffs it into an RTF file. This can be used to export to PDF.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-o", "--output-file", help="Specify file different file name or location. Default is script directory's name.", default=getDefaultOutputFile())
parser.add_argument("-p", "--project-root", help="Specify a different location for the Android Studio root.", default="./")
args = vars(parser.parse_args())

# Validate arguments
PROJECT_DIR = args["project_root"]
if not os.path.isdir(PROJECT_DIR):
    print("Invalid path provided.")
    print("Use -h for usage info")
    exit(1)

MAIN_PATH = os.path.join(PROJECT_DIR, "app", "src", "main")

if not os.path.exists(MAIN_PATH):
    print("Not a valid Android Studio project!")
    if PROJECT_DIR == "./":
        print("Provide a path to the root of an Android Studio project")
    else:
        print("Run this script at the root of an Android Studio project")
    print("Use -h for usage info")
    exit(1)

outputFilePath = args["output_file"]

ktFiles = []
xmlFiles = []

print("Found project at "+PROJECT_DIR)

for root, dirs, files in os.walk(MAIN_PATH):
    for file in files:
        if file.endswith(".kt"):
            filePath = os.path.join(root, file)
            ktFiles.append(filePath)
        elif file.endswith(".xml"):
            if root.endswith("layout") or file == "strings.xml":
                filePath = os.path.join(root, file)
                xmlFiles.append(filePath)

ktS = "s" if len(ktFiles) != 1 else ""
xmlS = "s" if len(xmlFiles) != 1 else ""
print("Found "+str(len(ktFiles))+" Kotlin file"+ktS)
print("Found "+str(len(xmlFiles))+" XML file"+xmlS)

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

with open(outputFilePath, 'w') as outputFile:
    outputFile.write(rtfHeader)
    outputFile.write(fontTable)
    outputFile.write(codeToRTF(ktFiles))
    outputFile.write(codeToRTF(xmlFiles))
    outputFile.write(rtfFooter)

print("Gathered file contents into "+outputFilePath+". Be sure to open the file in Microsoft Word or LibreOffice Writer and print to PDF!")
