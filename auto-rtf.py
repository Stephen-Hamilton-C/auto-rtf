# Settings
HEADER_FONTS = "Liberation Sans;Sans Serif"
HEADER_SIZE_PT = 20
CODE_FONTS = "FreeMono"
CODE_SIZE_PT = 10

# Imports
import os
import sys
import re
import argparse

# Constants
VERSION = "1.1.0"
BUG_URL = "https://github.com/Stephen-Hamilton-C/auto-rtf/issues/new?assignees=Stephen-Hamilton-C&labels=&projects=&template=bug_report.md"
SCRIPT_PATH = __file__
SCRIPT_NAME = os.path.basename(SCRIPT_PATH)

# Setup argument parser
def getDefaultOutputFile():
    parentDir = os.getcwd()
    parentDirName = os.path.basename(parentDir)
    if parentDirName.startswith(".") and parentDirName.endswith("."):
        parentDirName = os.path.basename(os.path.dirname(parentDir))

    return parentDirName + ".rtf"

# Setup arguments
parser = argparse.ArgumentParser(prog="auto-rtf", description="Compiles all Kotlin and relevant XML files from an Android Studio project and stuffs it into an RTF file. This can be used to export to PDF.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-o", "--output-file", help="Specify file different file name or location. Default is script directory's name.", default=getDefaultOutputFile())
parser.add_argument("-p", "--project-root", help="Specify a different location for the Android Studio root.", default=os.getcwd())
parser.add_argument("-v", "--version", help="Prints current version", action="store_true")
parser.add_argument("-b", "--report-bug", help="Opens a web browser to report a bug", action="store_true")
parser.add_argument("-w", "--remove-watermark", help="Removes the watermark placed at the top of the RTF file", action="store_true")
args = vars(parser.parse_args())

# Open browser if report_bug option is present
if args["report_bug"]:
    print("Opening web browser to "+BUG_URL)
    import webbrowser
    webbrowser.open(BUG_URL)
    exit(0)

# Report version if version option is present
if args["version"]:
        print("auto-rtf version "+VERSION)
        exit(0)

# Validate arguments

# Validate project_root is a directory
PROJECT_DIR = args["project_root"]
if not os.path.isdir(PROJECT_DIR):
    print("Invalid path provided.")
    print("Use -h for usage info")
    exit(1)

# Check that project_root is indeed an Android Studio project
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

print("Found project at "+PROJECT_DIR)

# Find all kt and relevant xml files
ktFiles = []
xmlFiles = []

for root, dirs, files in os.walk(MAIN_PATH):
    for file in files:
        if file.endswith(".kt"):
            filePath = os.path.join(root, file)
            ktFiles.append(filePath)
        elif file.endswith(".xml"):
            if "layout" in root or root.endswith("navigation") or file == "strings.xml":
                filePath = os.path.join(root, file)
                xmlFiles.append(filePath)

# Add an s if there are multiple files
ktS = "s" if len(ktFiles) != 1 else ""
xmlS = "s" if len(xmlFiles) != 1 else ""
# Report number of files
print("Found "+str(len(ktFiles))+" Kotlin file"+ktS)
print("Found "+str(len(xmlFiles))+" XML file"+xmlS)

# Converts files to RTF
def codeToRTF(files) -> str:
    rtf = ""
    for file in files:
        # Set font size
        # RTF uses half-px units
        rtf += "\\fs"+str(round(HEADER_SIZE_PT * 2))+"\n"
        # Set font to header font
        rtf += "\\f0\n"
        # Set bold
        rtf += "\\b "
        # Insert file name to header
        if file.lower().endswith(".xml"):
            # Add directory name to xml files
            fileDirectoryPath = os.path.dirname(file)
            fileDirectoryName = os.path.basename(fileDirectoryPath)
            rtf += fileDirectoryName + "/"
        rtf += os.path.basename(file)
        # End bold
        rtf += "\\b0"
        # End line
        rtf += "\\line\n"

        # Set font size for code
        rtf += "\\fs"+str(round(CODE_SIZE_PT * 2))+"\n"
        # Set font to code font
        rtf += "\\f1\n"

        # Place contents of code into RTF string
        with open(file, 'r') as codeFile:
            for codeFileLine in codeFile:
                # Make spaces smaller
                replacedSpaces = re.sub("    ", "  ", codeFileLine)
                # Ensure braces are shown
                replacedOpenBraces = re.sub("{", "\\{", replacedSpaces)
                replacedCloseBraces = re.sub("}", "\\}", replacedOpenBraces)
                # Add modified line to RTF string
                rtf += replacedCloseBraces
                rtf += "\\line\n"
        rtf += "\\line\n"

    return rtf


# RTF Syntax things
# You can blame macOS for this being excessively complicated
fontTable = "{\\fonttbl\\f0\\fswiss\\fcharset0 "+HEADER_FONTS+";\\f1\\fswiss\\fcharset0 "+CODE_FONTS+";}"
rtfHeader = """{\\rtf1\\ansi\\ansicpg1252\\cocoartf2709
\\cocoatextscaling0\\cocoaplatform0""" + fontTable + """
{\\colortbl;\\red255\\green255\\blue255;}
{\\*\\expandedcolortbl;;}
\\margl1440\\margr1440\\vieww13440\\viewh7800\\viewkind0
\\pard\\tx720\\tx1440\\tx2160\\tx2880\\tx3600\\tx4320\\tx5040\\tx5760\\tx6480\\tx7200\\tx7920\\tx8640\\pardirnatural\\partightenfactor0

"""
watermark = """\\fs16
This file was generated with auto-rtf version """ + VERSION + """\\line
\\line

"""
rtfFooter = "}\n"

# Create output file
with open(outputFilePath, 'w') as outputFile:
    outputFile.write(rtfHeader)
    if not args["remove_watermark"]:
        outputFile.write(watermark)
    outputFile.write(codeToRTF(ktFiles))
    outputFile.write(codeToRTF(xmlFiles))
    outputFile.write(rtfFooter)

print("Gathered file contents into "+outputFilePath+". Be sure to open the file in Microsoft Word or LibreOffice Writer and print to PDF!")

