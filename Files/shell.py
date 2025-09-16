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
    flags = parts.get("flags",None)
    params = parts.get("params",None)

    if input:
        pass

    if len(params) > 0:
        pass
        return {"output":None,"error":"Directory doesn't exist"}

    if 'a' in flags:
        pass

    if 'l' in flags:
        pass

    if 'h' in flags:
        pass

    output="something"


    return {"output":output,"error":None}

'''
mkdir command creates a directory
'''
def mkdir():
    # code here
    pass

'''
cd will change the working directory
'''
def cd():
    # code here
    pass

'''
pwd command will print the working directory
- all I THINK we have to do here is just grab the name of the directory
  and just display it
'''
def pwd():
    # code here
    pass

'''
mv command will
- move files/directories to a different location
- rename file
'''
def mv():
    # code here
    pass

'''
cp command makes a copy of the first argument into the second argument
'''
def cp():
    # code here
    pass

'''
rm command lets the user delete a file/directory passing its name
'''
def rm():
    # code here
    pass

'''
cat command lets the user view the contents of a file
- how are we going to handle security here?
  only allowed access if the permissions are correctly set
'''
def cat():
    # code here
    pass

'''
less lets the user only see snippets of files
- same security concern here
'''
def less():
    # code here
    pass

'''
by default, head displays the first ten lins of a file
'''
def head():
    # code here
    pass

'''
tail command prints the data at the end of a file
'''
def tail():
    # code here
    pass

'''
grep command finds matching words within text files
'''
def grep():
    # code here
    pass

'''
wc simply counts the total number of words in a file
'''
def wc():
    # code here
    pass

'''
history prints the entire history of commands used
- I think we can just have a cmd_history list that contains each
  command used by simply appending the cmd to the list
'''
def history():
    # code here
    pass

'''
chmod changes permissions of files or directories to users
'''
def chmod():
    # code here
    pass

'''
sort command sorts the contents of a file(s) in ASCII order
'''
def sort():
    # code here
    pass

# def COMMAND OF OUR CHOICE HERE ():

if __name__ == "__main__":
    cmd_list = parse_cmd("ls Assignments -lah | grep '.py' | wc -l > output")
    print(cmd_list)
    sys.exit(0)
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

            # This 'elif' simulates something "happening" after pressing return
            cmd = "Executing command...."  #
            print_cmd(cmd)
            sleep(1)

            ## YOUR CODE HERE
            ## Parse the command
            ## Figure out what your executing like finding pipes and redirects

            cmd = ""  # reset command to nothing (since we just executed it)

            print_cmd(cmd)  # now print empty cmd prompt
        else:
            cmd += char  # add typed character to our "cmd"
            print_cmd(cmd)  # print the cmd out
