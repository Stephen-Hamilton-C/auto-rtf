# Changelog <!-- omit in toc -->
All notable changes to auto-rtf will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
auto-rtf uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# 1.1.0 - 2023-10-03
- Fixed some layout XML files not being included
- Added watermark to the top of the file
  - This can be removed using the `--remove-watermark` or `-w` option
  - This is here mostly to help with bug reports
- Added directory name to XML file headers
- Changed automatic project discovery to use current working directory rather than script directory
  - This makes the script more command-line friendly

# 1.0.3 - 2023-09-18
- Fixed nav graphs not being included in the PDF
- Fixed macOS TextEdit not being able to open generated RTF files ([#1](https://github.com/Stephen-Hamilton-C/auto-rtf/issues/1))

# 1.0.2 - 2023-09-10
- Fixed braces not showing up in RTF file
- Added `--report-bug` option

# 1.0.1 - 2023-09-08
- Fixed double-click run not working on Windows
- Added `--version` option

# 1.0.0 - 2023-09-08
- Initial Release

