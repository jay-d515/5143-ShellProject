#!/usr/bin/env python
"""
This file is about using getch to capture input and handle certain keys 
when the are pushed. The 'command_helper.py' was about parsing and calling functions.
This file is about capturing the user input so that you can mimic shell behavior.

"""
import os
import sys
from time import sleep
from rich import print
from getch import Getch

##################################################################################
##################################################################################

getch = Getch()  # create instance of our getch class

prompt = "$"  # set default prompt

def parse_cmd(cmd_input):
    command_list = []
    cmds = cmd_input.split("|")
    for cmd in cmds:
        d = {"input":None,"cmd":None,"params":[],"flags":None}
        subparts = cmd.strip().split()
        d["cmd"]= subparts[0]
        for item in subparts[1:]:
            if "-" in item:
                d["flags"]=item[1:]
            else:
                d['params'].append(item)
            
        command_list.append(d)
    return command_list

def print_cmd(cmd):
    """This function "cleans" off the command line, then prints
    whatever cmd that is passed to it to the bottom of the terminal.
    """
    padding = " " * 80
    sys.stdout.write("\r" + padding)
    sys.stdout.write("\r" + prompt + cmd)
    sys.stdout.flush()

def ls(parts):
    '''
    input: dict: {"input":string,"cmd":string,"params":list,"flags":string}
    output dict: {"output":string,"error":string}
    '''
    input = parts.get("input",None)
    flags = parts.get("flags",None) or ""
    params = parts.get("params",None) or []

    directory = params[0] if len(params) > 0 else "."

    try:
        files = os.listdir(directory)

        if 'a' not in flags:
            files = [f for f in files if not f.startswith('.')]
            
        files.sort()  # Sort files alphabetically
        
        if 'l' in flags:
            # Long format - show detailed file information
            import time
            output_lines = []
            for file in files:
                filepath = os.path.join(directory, file)
                try:
                    stat_info = os.stat(filepath)
                    size = stat_info.st_size
                    
                    # Check if -h flag is also present
                    if 'h' in flags:
                        # Human readable size format
                        if size >= 1024**3:
                            size_str = f"{size/1024**3:.1f}G"
                        elif size >= 1024**2:
                            size_str = f"{size/1024**2:.1f}M" 
                        elif size >= 1024:
                            size_str = f"{size/1024:.1f}K"
                        else:
                            size_str = f"{size}B"
                    else:
                        # Regular size in bytes
                        size_str = str(size)
                    
                    # Determine file type (directory vs file)
                    file_type = "d" if os.path.isdir(filepath) else "-"
                    
                    # Format the long listing line
                    line = f"{file_type}rwxr-xr-x  {size_str:>8}  {file}"
                    output_lines.append(line)
                except OSError:
                    # Handle files we can't stat
                    output_lines.append(f"?---------  {'?':>8}  {file}")
            
            output = "\n".join(output_lines)
        else:
            # Simple format - just list filenames
            if 'h' in flags:
                # -h flag without -l doesn't change simple listing
                pass
            
            output = "  ".join(files)
            
        return {"output":output,"error":None}
    except FileNotFoundError:
        return {"output":None,"error":"Directory doesn't exist"}

'''
exit command will exit the shell
'''
def exit():
    # code here
    pass
'''
mkdir:
creates a new directory
'''
def mkdir():
    # code here
    pass

'''
cd:
changes the current working directory
'''
def cd():
    # code here
    pass

'''
pwd:
prints the current working directory to the terminal
'''
def pwd(parts):
    '''
    input: dict: {"input":string,"cmd":string,"params":list,"flags":string}
    output dict: {"output":string,"error":string}
    '''
    try:
        current_directory = os.getcwd()
        return {"output":current_directory, "error":None}
    except Exception as e:
        return {"output":None, "error": f"pwd:{str(e)}"}

'''
mv:
moves files/directories to a different location and renames files
'''
def mv():
    # code here
    pass

'''
cp:
makes a copy of the first argument into the second argument
'''
def cp():
    # code here
    pass

'''
rm:
allows the user to delete a file/directory by passing its name
'''
def rm():
    # code here
    pass

'''
cat:
allows the user to view the contents of a file
- how are we going to handle security here?
  only allowed access if the permissions are correctly set
'''
def cat():
    # code here
    pass

'''
less:
allows the user to only see snippets of files
- same security concern here
'''
def less():
    # code here
    pass

'''
head:
displays the first ten lins of a file
'''
def head():
    # code here
    pass

'''
tail:
prints the data at the end of a file
'''
def tail():
    # code here
    pass

'''
grep:
finds matching words within text files
'''
def grep():
    # code here
    pass

'''
wc:
counts the total number of words in a file
'''
def wc():
    # code here
    pass

'''
history:
prints the entire history of commands used
- I think we can just have a cmd_history list that contains each
  command used by simply appending the cmd to the list
'''
def history():
    # code here
    pass

'''
chmod:
changes permissions of files or directories to users
'''
def chmod():
    # code here
    pass

'''
sort:
sorts the contents of a file(s) in ASCII order
'''
def sort():
    # code here
    pass

# def COMMAND OF OUR CHOICE HERE ():

def execute_command(command_dict):
    """
    Command dispatcher - routes commands to their respective functions
    input: dict: {"input":string,"cmd":string,"params":list,"flags":string}
    output: dict: {"output":string,"error":string}
    """
    command_map = {
        'pwd': pwd,
        'ls': ls,
        # Add more commands here as you implement them
        # 'cd': cd,
        # 'mkdir': mkdir,
        # 'cat': cat,
        # etc.
    }
    
    cmd_name = command_dict.get('cmd', '').lower()
    
    if cmd_name in command_map:
        return command_map[cmd_name](command_dict)
    else:
        return {"output": None, "error": f"Command '{cmd_name}' not found"}

if __name__ == "__main__":
    cmd_list = parse_cmd("ls Assignments -lah | grep '.py' | wc -l > output")
    print(cmd_list)
    # sys.exit(0)
    cmd = ""  # empty cmd variable

    print_cmd(cmd)  # print to terminal

    while True:  # loop forever

        char = getch()  # read a character (but don't print)

        if char == "\x03" or cmd == "exit":  # ctrl-c
            raise SystemExit("Bye.")

        elif char == "\x7f":  # back space pressed
            cmd = cmd[:-1]
            print_cmd(cmd)

        elif char in "\x1b":  # arrow key pressed
            null = getch()  # waste a character
            direction = getch()  # grab the direction

            if direction in "A":  # up arrow pressed
                # get the PREVIOUS command from your history (if there is one)
                # prints out 'up' then erases it (just to show something)
                cmd += "\u2191"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            if direction in "B":  # down arrow pressed
                # get the NEXT command from history (if there is one)
                # prints out 'down' then erases it (just to show something)
                cmd += "\u2193"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            if direction in "C":  # right arrow pressed
                # move the cursor to the right on your command prompt line
                # prints out 'right' then erases it (just to show something)
                cmd += "\u2192"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            if direction in "D":  # left arrow pressed
                # moves the cursor to the left on your command prompt line
                # prints out 'left' then erases it (just to show something)
                cmd += "\u2190"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            print_cmd(cmd)  # print the command (again)

        elif char in "\r":  # return pressed
            # Save the current command before processing
            user_input = cmd.strip()
            
            if user_input:  # Only process if there's actually a command
                # Show execution message
                cmd = "Executing command...."
                print_cmd(cmd)
                sleep(0.5)
                
                # Parse the command into structured format
                command_list = parse_cmd(user_input)
                
                # For now, just execute the first command (no pipes yet)
                if command_list:
                    first_cmd = command_list[0]
                    result = execute_command(first_cmd)
                    
                    # Display the result
                    print()  # New line after command
                    if result["output"]:
                        print(result["output"])
                    if result["error"]:
                        print(f"Error: {result['error']}")

            cmd = ""  # reset command to nothing (since we just executed it)
            print_cmd(cmd)  # now print empty cmd prompt
        else:
            cmd += char  # add typed character to our "cmd"
            print_cmd(cmd)  # print the cmd out
