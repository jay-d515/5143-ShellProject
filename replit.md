# Shell Project - Replit Setup Documentation

## Project Overview
- **Type**: Python Console Application
- **Purpose**: Educational assignment to implement a basic shell with command parsing, piping, and redirection
- **Language**: Python 3.11
- **Main Entry Point**: `Files/shell.py`

## Project Structure
```
/
├── Files/
│   ├── shell.py          # Main shell application with command parsing
│   ├── getch.py          # Cross-platform single character input handler  
│   ├── splitcmd.py       # Command splitting examples
│   ├── bacon.txt         # Sample file for testing
│   └── README.md         # Original project README
├── Project Information/
│   ├── README.md         # Assignment instructions
│   ├── command_checklist.md    # Command implementation checklist
│   └── general_checklist.md    # General grading checklist
└── README.md             # Main project README
```

## Recent Changes
- **2025-09-16**: Initial Replit environment setup
  - Installed Python 3.11 and required dependencies (rich library)
  - Configured console workflow to run the shell application
  - Verified application runs and parses commands correctly

## Dependencies
- **Python 3.11**: Main runtime environment
- **rich**: Library for enhanced terminal output formatting
- **Standard library**: os, sys, time, termios (for getch functionality)

## Current State
- ✅ **Environment Setup**: Python 3.11 installed with all dependencies
- ✅ **Application Status**: Runs successfully, parses example commands correctly
- ⚠️ **Interactive Mode**: Currently disabled via sys.exit(0) on line 195 in shell.py
- ⚠️ **Command Implementation**: Most shell commands are stub functions (not fully implemented)

## Workflow Configuration
- **Name**: Shell
- **Command**: `python3 Files/shell.py`  
- **Type**: Console application
- **Status**: Working - parses and displays command structure

## Architecture Notes
- **Command Parsing**: Implemented in `parse_cmd()` function
- **Input Handling**: Cross-platform character input via getch.py
- **Command Structure**: Each command parsed into cmd, params, flags, and input
- **Shell Features**: Designed to support piping, redirection, and standard UNIX commands

## Assignment Requirements
This project implements requirements for CMPS5143 Advanced Operating Systems:
- Shell command parsing and execution
- Support for pipes, redirection, background execution
- Implementation of common UNIX commands (ls, cat, grep, etc.)
- Interactive shell interface with arrow key navigation
- Command history functionality

## Development Status
The project is currently in development stage with:
- Basic parsing framework completed
- Individual command implementations mostly stubbed
- Interactive shell loop present but disabled for testing
- All necessary dependencies and environment setup completed

## User Preferences
- **Coding Style**: Python with clear function separation and comprehensive commenting
- **Project Structure**: Modular organization with separate files for different functionality
- **Documentation**: Comprehensive inline comments and docstrings for educational purposes