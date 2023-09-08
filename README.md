# Auto RTF
This script was made by an annoyed CS3714 student to instantly compile all his
code into one rtf file that could easily be used to export to a PDF.

## Usage
### Windows/macOS
1. Drop `auto-rtf.py` into your Android Studio project
2. Double click on the file in File Explorer or Finder
3. You should see an RTF file appear with the same name as the project folder
4. Open this RTF file and print to PDF
5. Any time you make changes to the code, simply run the script again!

### Linux/CLI
If you use Linux, or you prefer running this script from the command line,
this section is for you!

Running the script with no arguments will have the same effect as Windows/macOS.
However, you have more control over what the script does over the command line.
Here are some helpful options:
- `--help`, `-h`: Shows a help message describing what each option does
- `--output-file`, `-o`: Specifies a different file name or location for the resulting RTF file
- `--project-root`, `-p`: Specifies a root directory for an Android Studio project
