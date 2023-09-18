HEADER_FONTS = "Liberation Sans;Sans Serif"
HEADER_SIZE_PT = 20
CODE_FONTS = "FreeMono"
CODE_SIZE_PT = 10

import os
import sys
import re
import argparse

VERSION = "1.0.2"
BUG_URL = "https://github.com/Stephen-Hamilton-C/auto-rtf/issues/new?assignees=Stephen-Hamilton-C&labels=&projects=&template=bug_report.md"
SCRIPT_PATH = __file__
SCRIPT_NAME = os.path.basename(SCRIPT_PATH)

# Setup argument parser
def getDefaultOutputFile():
    parentDir = os.path.dirname(SCRIPT_PATH)
    parentDirName = os.path.basename(parentDir)
    if parentDirName.startswith(".") and parentDirName.endswith("."):
        parentDirName = os.path.basename(os.path.dirname(parentDir))

    return parentDirName + ".rtf"

parser = argparse.ArgumentParser(prog="auto-rtf", description="Compiles all Kotlin and relevant XML files from an Android Studio project and stuffs it into an RTF file. This can be used to export to PDF.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-o", "--output-file", help="Specify file different file name or location. Default is script directory's name.", default=getDefaultOutputFile())
parser.add_argument("-p", "--project-root", help="Specify a different location for the Android Studio root.", default="./")
parser.add_argument("-v", "--version", help="Prints current version", action="store_true")
parser.add_argument("-b", "--report-bug", help="Opens a web browser to report a bug", action="store_true")
args = vars(parser.parse_args())

if args["report_bug"]:
    print("Opening web browser to "+BUG_URL)
    import webbrowser
    webbrowser.open(BUG_URL)
    exit(0)

if args["version"]:
        print("auto-rtf version "+VERSION)
        exit(0)

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
            if root.endswith("layout") or root.endswith("navigation") or file == "strings.xml":
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
                replacedSpaces = re.sub("    ", "  ", codeFileLine)
                replacedOpenBraces = re.sub("{", "\\{", replacedSpaces)
                replacedCloseBraces = re.sub("}", "\\}", replacedOpenBraces)
                rtf += replacedCloseBraces
                rtf += "\\line\n"
        rtf += "\\line\n"


    return rtf


fontTable = "{\\fonttbl\\f0\\fswiss\\fcharset0 "+HEADER_FONTS+";\\f1\\fswiss\\fcharset0 "+CODE_FONTS+";}"
rtfHeader = """{\\rtf1\\ansi\\ansicpg1252\\cocoartf2709
\\cocoatextscaling0\\cocoaplatform0""" + fontTable + """
{\\colortbl;\\red255\\green255\\blue255;}
{\\*\\expandedcolortbl;;}
\\margl1440\\margr1440\\vieww13440\\viewh7800\\viewkind0
\\pard\\tx720\\tx1440\\tx2160\\tx2880\\tx3600\\tx4320\\tx5040\\tx5760\\tx6480\\tx7200\\tx7920\\tx8640\\pardirnatural\\partightenfactor0

"""
rtfFooter = "}\n"

with open(outputFilePath, 'w') as outputFile:
    outputFile.write(rtfHeader)
    outputFile.write(codeToRTF(ktFiles))
    outputFile.write(codeToRTF(xmlFiles))
    outputFile.write(rtfFooter)

print("Gathered file contents into "+outputFilePath+". Be sure to open the file in Microsoft Word or LibreOffice Writer and print to PDF!")

