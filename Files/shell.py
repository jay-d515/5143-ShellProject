#!/usr/bin/env python
"""
This file is about using getch to capture input and handle certain keys 
when the are pushed. The 'command_helper.py' was about parsing and calling functions.
This file is about capturing the user input so that you can mimic shell behavior.

"""
import os
import sys
import stat
import shutil # used for file "handling" (cp, rm)
import getpass # used for whoami function
from time import sleep
from rich import print
from getch import Getch

##################################################################################
##################################################################################

# create instance of our getch class
getch = Getch()
# a list to store the command history
cmd_history = []
# index for navigating history
history_index = -1
# current position of the cursor
cursor_position = 0

'''
parse_cmd:
parses the command line input into a list of dictionaries
'''
def parse_cmd(cmd_input):
    command_list = []
    cmds = cmd_input.split("|") # split piping on the | character
    for cmd in cmds:
        # add in/outfile and append to our dictionary
        parts = {"input":None,"cmd":None,"params":[],"flags":None, "infile": None, "outfile": None, "append": None}
        subparts = cmd.strip().split()
        i = 0
        while i < len(subparts):
            # command part
            part = subparts[i]
            # read the input from a file
            if part == "<":
                # grab filename, save it to dictionary
                parts["infile"] = subparts[i+1]
                i += 2
            # write the output TO file
            elif part == ">":
                parts["outfile"] = subparts[i+1]
                parts["append"] = False     # do not append
                i += 2
            # write output to a file, but append
            elif part == ">>":
                parts["outfile"] = subparts[i+1]
                parts["append"] = True
                i += 2
            # separate the flag and add to "flags"
            elif part.startswith("-"):
                if parts["flags"]:
                    parts["flags"] += part[1:]
                else:
                    parts["flags"] = part[1:]
                #i += 1
            else:
                # parameter handling
                if parts["cmd"] is None:
                    parts["cmd"] = part
                else:
                    parts["params"].append(part)
                i += 1
        # once finished, append the dictionary to command list
        command_list.append(parts)
    return command_list

def print_cmd(cmd):
    """This function "cleans" off the command line, then prints
    whatever cmd that is passed to it to the bottom of the terminal.
    """
    padding = " " * 80
    sys.stdout.write("\r" + padding)

    try:
        cwd = os.getcwd()
    except:
        cwd = "/"

    sys.stdout.write(f"\r{cwd}$ {cmd}")
    sys.stdout.flush()

'''
help
- displays correct use of commands.
'''
def help(parts, command_map=None):
    '''
    provides more information on a given command.

    - displays correct use of commands.
    - if no command, lists all available commands.
    '''

    params = parts.get("params") or []
    if not params:
        cmds = sorted(command_map.keys())   # sorts cmds in alpha order
        line = ["Commands list:\n"]
        for cmd in cmds:
            doc = command_map[cmd].__doc__  # print the associated docstr
            if doc:
                summary = doc.strip().split("\n")[0] 
            # used chatgpt for this part
            line.append(f" {cmd:<10} {summary}")    # left-aligns and pads right until 10 chars reached
        return {"output": "\n".join(line), "error": None}

    cmd_name = params[0].lower()
    if cmd_name in command_map:
        docstr = command_map[cmd_name].__doc__ or "No documentation available."
        return {"output": docstr, "error": None}
    else:
        return {"output": None, "error": f"help: no such command '{cmd_name}'"}
    
    # If one or more commands are given: show docs
    results = []
    for cmd_name in params:
        cmd_name = cmd_name.lower()
        if cmd_name in command_map:
            docstr = command_map[cmd_name].__doc__ or "No documentation available."
            results.append(f"{cmd_name}:\n{docstr.strip()}")
        else:
            results.append(f"help: no such command '{cmd_name}'")

    return {"output": "\n\n".join(results), "error": None}


    
'''
ls
- lists the entire working directory
'''
def ls(parts):
    '''
    lists all of the contents in the current working directory.

    flags:
     -l : displays file details in long format
     -a : shows all files, including hidden ones
     -h : makes file details human-readable
    '''
    input = parts.get("input",None)
    flags = parts.get("flags",None) or ""
    params = parts.get("params",None) or []

    # determine which directory to list
    if len(params) > 0:
        # use a specified directory
        directory = params[0]
    else:
        # use the current directory
        directory = "."

    try:
        # get a list of files in the current directory
        files = os.listdir(directory)

        # handles -a flag
        if 'a' in flags:
            # show all files, including hidden ones
            files = os.listdir(directory)
        else:
            # hide files that start with a dot
            files = os.listdir(directory)
            files = [f for f in files if not f.startswith('.')]

        # sorts the files alphabetically
        files.sort()

        # handles -l flag
        if 'l' in flags:
            # long format with file details
            output_lines = []
            for file in files:
                filepath = os.path.join(directory, file)
                try:
                    stat_info = os.stat(filepath)
                    size = stat_info.st_size

                    if 'h' in flags:
                        if size >= 1024**3:
                            size_str = f"{size/1024**3:.1f}G"
                        elif size >= 1024**2:
                            size_str = f"{size/1024**2:.1f}M"
                        elif size >= 1024:
                            size_str = f"{size/1024:.1f}K"
                        else:
                            size_str = f"{size}B"
                    else:
                        size_str = str(size)

                    # deternmine if it is a directory or file
                    file_type = "d" if os.path.isdir(filepath) else "-"
                    output_lines.append(f"{file_type}rwxr-xr-x {size_str:>8} {file}")
                except OSError:
                    output_lines.append(f"?--------- {'?':>8}  {file}")
            ouput = "\n".join(output_lines)
        else:
            # short format with just file names
            ouput = "  ".join(files)

        return {"output":ouput, "error":None}

    except FileNotFoundError:
        return {"output": None, "error": f"ls: cannot access '{directory}': No such file or directory"}
    except PermissionError:
        return {"output": None, "error": f"ls: cannot open directory '{directory}': Permission denied"}
    except Exception as e:
        return {"output": None, "error": f"ls: {str(e)}"}
'''
exit:
exit the shell
'''
def exit():
    '''
    forces termination of command shell.
    '''
    os.exit

'''
mkdir:
creates a new directory 
'''
def mkdir(parts):
    '''
    creates a new directory within the current directory.
    '''
    params = parts.get("params")    
    if not params:
        return {"output": None, "error": "mkdir: missing operand"}

    # returns the inputted directory name
    path = params[0]  

    try:
        os.mkdir(path)
        return {"output": None, "error": None}
    except FileExistsError:
        return {"output": None, "error": f"mkdir: cannot create directory '{path}': File exists"}
    except PermissionError:
        return {"output": None, "error": f"mkdir: cannot create directory '{path}': Permission denied"}
    except Exception as e:
        return {"output": None, "error": f"mkdir: {str(e)}"}


'''
cd:
changes the current working directory
'''
def cd(parts):
    '''
    changes the current working directory.
    '''

    try:
        # retrieves the list of parameters from parts
        params = parts.get("params",None) or []

        # if there are no params, default to the home directory
        if not params:
            target_directory = os.path.expanduser("~")
        # if there is at least one param, store the first one in arg
        else:
            arg = params[0]

            # if the argument is "~", go to the home directory
            if arg == "~":
                target_directory = os.path.expanduser("~")
            # if the argument is "..", move up one directory from the current one
            elif arg == "..":
                target_directory = os.path.dirname(os.getcwd())
            # otherwise, assume the user provided a valid path
            else:
                target_directory = os.path.expanduser(arg)

        # changes the current working directory
        os.chdir(target_directory)
        # if successful, return no output or error
        return {"output": None, "error": None}

    # if the directory doesn't exist, return an error message
    except FileNotFoundError:
        return {"output": None, "error": f"cd: no such file or directory: {params[0]}"}
    # if the path is not a directory, return an error message
    except NotADirectoryError:
        return {"output": None, "error": f"cd: not a directory: {params[0]}"}
    # if the user doesn't have permission to access the directory, return an error message
    except PermissionError:
        return {"output": None, "error": f"cd: permission denied: {params[0]}"}
    # if anything else goes wrong, return a error message
    except Exception as e:
        return {"output": None, "error": f"cd: {str(e)}"}
    

'''
pwd:
prints the current working directory to the terminal
'''
def pwd(parts):
    '''
    prints the current working directory to the terminal.
    '''
    try:
        # asks the OS for the current working directory
        current_directory = os.getcwd()
        # if everything works, return the current directory with no error
        return {"output":current_directory, "error":None}
    # if anything goes wrong, return an error message
    except Exception as e:
        return {"output":None, "error": f"pwd:{str(e)}"}

'''
mv:
moves files/directories to a different location and renames files
'''
def mv(parts):
    '''
    moves files/directories to a different location and renames files
    '''

    params = parts.get("params") or []
    if len(params)<2:
        return {"output":None, "error":"mv: missing file operation"}

    source, dest = params[0], params[1]

    try:
        os.rename(source, dest)
        return {"output":None, "error":None}
    except FileNotFoundError:
        return {"output":None, "error":f"mv:{source}: There is no such file exixts"}
    except PermissionError:
        return{"output":None, "error":f"mv:permission denied"}        
    except Exception as e:
        return{"output":None, "error":f"mv:{str(e)}"}    
    

'''
cp:
makes a copy of the first argument into the second argument
'''
def cp(parts):
    '''
    makes a copy of the first argument into the second argument.
    '''
    params = parts.get("params") or []
    if len(params)<2:
        return {"output":None, "error":"cp: missing file operation"}

    source, dest = params[0], params[1]

    try:
        shutil.copy(source, dest)   # copies contents of a given source file, 
                                    # and creates a destination file with those contents.
        return {"output":None, "error":None}
    except FileNotFoundError:
        return {"output":None, "error":f"cp:{source}: There is no such file exixts"}
    except PermissionError:
        return{"output":None, "error":f"cp:permission denied"}
    except Exception as e:
        return{"output":None, "error":f"cp:{str(e)}"} 

'''
rm:
allows the user to delete a file/directory by passing its name
'''
def rm(parts):
    '''
    allows the user to delete a file/directory by passing its name.

    flags:
     -r : recursively deletes directory and its contents, will ask for confirmation.
     -f : forces a recursive deletion on a directory and its contents
    '''
    params = parts.get("params",None) or []
    flags = parts.get("flags",None) or ""

    if not params:
        return {"output": None, "error": "rm: missing operand"}

    # makes it easier to understand in Andrew's mind
    flag_r = "r" in flags   
    flag_f = "f" in flags

    try:
        for path in params:
            # remove a single file, stand-alone or within a directory
            if os.path.isfile(path):
                os.remove(path)

            # recursive rm, with -r flag set
            elif os.path.isdir(path): # if the parameter is a directory, recursively delete
                if flag_r:  
                    for files in os.listdir(path):
                        #shutil.rmtree(path) 
                        check = input(f"Are you sure you want to delete '{path}' and its contents? [y/n] ").strip().lower()
                        if check == "n":
                            continue     # continue with the program
                        else:
                            shutil.rmtree(path) # removes entire "tree" of files
                else:
                    if not flag_f:
                        return {"output": None, "error": f"rm: cannot remove '{path}: is a directory"}

            # if the file/directory doesn't exits, print error message
            else: 
                if not flag_f:
                    return {"output": None, "error": f"rm: cannot remove '{path}': No such file or directory"}
            
    except Exception as e:
        if not flag_f:
            return{"output":None, "error":f"rm:{str(e)}"} 

    return {"output":None, "error":None}



'''
cat:
allows the user to view the contents of a file
'''
def cat(parts):
    """
    cat command: prints the contents of a file
    """
    params = parts.get("params") or []
    if not params:
        return {"output": None, "error": "cat: missing file operand"}
    
    filename = params[0]
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return {"output": f.read(), "error": None}
    except FileNotFoundError:
        return {"output": None, "error": f"cat: {filename}: No such file"}
    except PermissionError:
        return {"output": None, "error": f"cat: {filename}: Permission denied"}
    except Exception as e:
        return {"output": None, "error": f"cat: {str(e)}"}


'''
mv:
moves files/directories to a different location and renames files
'''
def mv(parts):
    '''
    moves files/directories to a different location and renames files.
    '''
    params = parts.get("params") or []
    if len(params)<2:
        return {"output":None, "error":"mv: missing file operation"}

    source, dest = params[0], params[1]

    try:
        os.rename(source, dest)
        return {"output":None, "error":None}
    except FileNotFoundError:
        return {"output":None, "error":f"mv:{source}: There is no such file exixts"}
    except PermissionError:
        return{"output":None, "error":f"mv:permission denied"}        
    except Exception as e:
        return{"output":None, "error":f"mv:{str(e)}"}        



'''
chmod
- changes the permissions of a file
'''
def chmod(parts):
    '''
    changes the permissions of a file 
    
    first argument must be three integer values long
    [0] = owner
    [1] = group
    [2] = others 
    "0": "---", "1": "--x", "2": "-w-", "3": "-wx",
    "4": "r--", "5": "r-x", "6": "rw-", "7": "rwx"
    '''
    params = parts.get("params") or []

    if len(params) < 2:
        return{"output":None, "error": "chmod:missing operand \n usage: chmod <mode> <filename>"}
    
    mode_str, filename = params[0], params[1]

    try:
        #this convert the strings like "777" into octal int (example 0o777)

        mode = int(mode_str, 8)

        os.chmod(filename, mode)

        permissions = stat.filemode(mode)

        return {"output": f"permission of '{filename}' changed to {mode_str}", "error":None}

    except ValueError:
        return {"ouput":None, "error": f"chmod invalid mode:'{mode_str}'", "error":None}
    except FileNotFoundError:
        return{"output":None, "error":f"chmod: there no such file '{filename}'"}
    except PermissionError:
        return {"output": None, "error": f"chmod: changing permissions of '{filename}': Permission denied"}
    except Exception as e:
        return {"output": None, "error": f"chmod: {str(e)}"}

'''
wc
- counts the total number of words in a file
'''
def wc(parts):
    '''
    counts the total number of words in a file.

    flags:
    -l : counts the number of lines
    -w : counts the number of words
    '''
    params = parts.get("params") or []
    flags = parts.get("flags") or ""
    text = ""

    # If there is a filename, read it
    if params:
        filename = params[0]
        try:
            with open(filename, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            return {"output": None, "error": f"wc:{filename}: No such file"}
        except PermissionError:
            return {"output": None, "error": f"wc:{filename}: Permission denied"}
    
    # If input from previous pipe exists, use it
    elif parts.get("input"):
        text = parts["input"]
    
    else:
        return {"output": None, "error": "wc: missing the command or input"}

    #output = ""
    if "l" in flags:
            output = str(len(text.splitlines()))
    elif "w" in flags:
            output = str(len(text.split()))
    if not flags:
            output = str(len(text.split()))

    return {"output": output, "error": None}

    #try: 
    #    with open(filename, "r", encoding="utf -8") as f:
    #        text = f.read()
    #        lines = text.splitlines()
    #        words = text.split()

        # list that handles the display
    #    display = []

        # flag handling
    #    if "l" in flags:
    #        display.append(f"Total lines: {len(lines)}")
    #    if "w" in flags:
    #        display.append(f"Total words: {len(lines)}")
    #    if not flags:
    #        display.append(f"Total words: {len(lines)}")

    #    return {"output": "  ".join(output_parts), "error": None}

    #except FileNotFoundError:
    #    return{"output":None, "error":f"wc:{filename}: no such file or file does not exists"}
    #except PermissionError:
    #    return{"output":None, "error": f"wc:{filename}:Permission denied"}                

'''sort:
sorts the contents of a file(s) in ASCII order
'''
def sort(parts):
    '''
    sorts the contents of a file(s) in ASCII order.
    '''
    params = parts.get("params") or []
    lines = []
    #if not params:
    #    return{"output":None, "error": "sort:missing file operand"}

    # if input is piped
    if parts.get("input"):
        lines = parts["input"].splitlines()
    elif params:
        filename = params[0]
        try:
            with open(filename, "r", encoding ="utf-8") as f:
                lines = f.read().splitlines()
            #sorted_lines = sorted(line.strip() for line in lines)
            #result ="\n".join(sorted_lines)
            #return {"output": result, "error":None}
        except FileNotFoundError:
            return{"output":None, "error":f"sort: {filename}: no such file exists"}
        except PermissionError:
            return{"output":None, "error":f"sort:{filename}: permisiion denied"}
    else:
        return {"output": None, "error": "sort: missing file or input"}

    lines.sort()
    return {"output": "\n".join(lines), "error": None}

'''
less:
allows the user to only see snippets of files
'''
def less(parts):
    """
    less command: page through a file interactively.
    Controls:
      - Space : next page
      - Enter : next line
      - q     : quit back to shell
    """

    params = parts.get("params") or []
    if not params:
        return {"output": None, "error": "less: missing file operand"}

    filename = params[0]

    try:
        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return {"output": None, "error": f"less: {filename}: No such file"}
    except PermissionError:
        return {"output": None, "error": f"less: {filename}: Permission denied"}
    except Exception as e:
        return {"output": None, "error": f"less: {str(e)}"}

    # get terminal size, fallback to 20 lines
    try:
        term_lines = shutil.get_terminal_size().lines
        page_size = max(5, term_lines - 2)
    except Exception:
        page_size = 20

    i = 0
    total = len(lines)

    while i < total:
        end = min(i + page_size, total)
        for ln in lines[i:end]:
            print(ln.rstrip())

        # show prompt
        sys.stdout.write("-hit space for more\n")
        sys.stdout.write("-hit q to end")
        sys.stdout.flush()

        # wait for one key
        ch = getch()   

        # clear the prompt
        sys.stdout.write("\r" + " " * len("--More--") + "\r")
        sys.stdout.flush()

        if ch == "q":
            break
        elif ch == " ":  # space → next page
            i = end
        elif ch in ("\r", "\n"):  # hit enter to next line  next line
            i = i + 1
        elif ch == "\x03":  # Ctrl+C
            raise KeyboardInterrupt
        else:
            # any other key = next page
            i = end

    return {"output": None, "error": None}
   

'''
head:
displays the first ten lines of a file
'''
def head(parts):
    '''
    displays the first ten lines of a file.
    '''
    # if params doesn't exist, defaults to an empty list
    params = parts.get("params") or []
    # if flags doesn't exist, defaults to an empty string
    flags = parts.get("flags") or ""

    # if a filename is not provided, return an error message
    if not params:
        return {"output": None, "error": "Head: missing file operand"}
    
    # assumes the first parameter is a filename
    filename = params[0]
    # default number of lines to show
    n = 10

    if "n" in flags:
        # check that there's at least one more parameter after the filename
        if len(params) > 1:
            # tries to convert the second parameter to an integer
            try:
                n = int(params[1])
            # if the second parameter isn't an integer return an error message
            except ValueError:
                return {"output": None, "error": "head: invalid number of lines"}
        # if the user typed head {filename} -n without a number after the n
        # return an error message
        else:
            return {"output": None, "error": "head: option requires an argument -- 'n'"}
    # tries to open the file and read its lines    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            # reads all lines into a list
            lines = f.readlines()
            # returns the first n lines as a single string
            return {"output": "".join(lines[:n]), "error": None}
    # if the file doesn't exist, return an error message
    except FileNotFoundError:
        return {"output": None, "error": f"head: {filename}: No such file or directory"}
    # if the user doesn't have permission to read the file, return an error message
    except PermissionError:
        return {"output": None, "error": f"head: {filename}: Permission denied"}
    
'''
tail:
prints the data at the end of a file
'''
def tail(parts):
    '''
    prints the data at the end of a file.

    - defaults to ten lines
    - if n is given as an argument, print n lines
    '''
    # if params doesn't exist, defaults to an empty list
    params = parts.get("params") or []
    # if flags doesn't exist, defaults to an empty string
    flags = parts.get("flags") or ""

    # if a filename is not provided, return an error message
    if not params:
        return {"output": None, "error": "tail: missing the file operand"}
    
    # assumes the first parameter is a filename
    filename = params[0]
    # default number of lines to show
    n = 10

    # if the user included the "n" flag
    if "n" in flags:
        # check that there's at least one more parameter after the filename
        if len(params) > 1:
            # tries to convert the second parameter to an integer
            try:
                n = int(params[1])
            # if the second parameter isn't an integer return an error message
            except ValueError:
                return {"output": None, "error": "tail: invalid number of lines"}
        # if the user typed tail {filename} -n without a number after the n
        # return an error message
        else:
            return {"output": None, "error": "tail: option requires an argument -- 'n'"}
    # tries to open the file and read its lines   
    try:
        with open(filename, "r", encoding="utf-8") as f:
            # reads all lines into a list
            lines = f.readlines()
            # returns the last n lines as a single string
            return {"output": "".join(lines[-n:]), "error": None}
    # if the file doesn't exist, return an error message
    except FileNotFoundError:
        return {"output": None, "error": f"tail: cannot open '{filename}': No such file"}
    # if the user doesn't have permission to read the file, return an error message
    except PermissionError:
        return {"output": None, "error": f"tail: cannot open '{filename}': Permission denied"}
'''
grep:
finds matching words within text files
'''
def grep(parts):
    '''
    runs a search on a file or through input.

    flags:
    -l : display the file name when matching
    -i : when matching, ignore the case
    '''
    params = parts.get("params") or []
    flags = parts.get("flags") or ""
    input_txt = parts.get("input")
    # flag functions and initializations
    ignore_case = 'i' in flags
    list_files = 'l' in flags

    # if there are more than two parameters, pass error
    if len(params) < 2:
        return {"output": None, "error": "grep: usage: grep [flags] pattern file(s)"}
    # if grep doesn't have parameters, error message
    if not params:
        return {"output": None, "error": "grep: missing search pattern"}

    # the string to match, and search all files
    to_match = params[0]
    files = params[1:]
    # if no file(s) give, print error
    if not files:
        return {"output": None, "error": "grep: no file specified"}

    

    # empty list to put the lines into
    lines_match = []
    # empty set to put files into
    files_match = set()

    # Reading from the files
    if files:
        for filename in files:
            try:
                with open(filename, "r", encoding = "utf-8") as f:
                    # check the lines
                    for line in f:
                        line_to_check = line
                        pattern_to_check = to_match
                        # if -i is set, ignore the case
                        if ignore_case:
                            line_to_check = line.lower()
                            pattern_to_check = to_match.lower()
                        # if the pattern is in the line, add the file to the match set
                        if pattern_to_check in line_to_check:
                            if list_files:
                                files_match.add(filename)
                                break
                            else:
                                lines_match.append(f"{filename}:{line.rstrip()}")

            except FileNotFoundError:
                return {"output": None, "error": f"grep: {filename}: No such file"}
            except PermissionError:
                return {"output": None, "error": f"grep: {filename}: Permission denied"}

    elif input_txt:
        for line in input_txt.splitlines():
            line_to_check = line
            pattern_to_check = to_match
            if ignore_case:
                line_to_check = line.lower()
                pattern_to_check = to_match.lower()

            if pattern_to_check in line_to_check:
                lines_match.append(line.rstrip())

    else:
        return {"output": None, "error": "grep: no file specified and no input piped"}
        
    # if the -l flag is set, display
    if list_files:
        return {"output": "\n".join(files_match), "error": None}
    else:
        return {"output": "\n".join(lines_match), "error": None}

    


'''
history:
prints the entire history of commands used as an enumerated list, beginning from 1 to i
'''
def history(parts=None):
    '''
    prints the entire history of commands used as an enumerated list, beginning from 1 to i.
    '''
    lines = []
    # enumerate and append each cmd to cmd_history
    for i, cmd in enumerate(cmd_history):
        lines.append(f"{i+1} {cmd}")
    return {"output": "\n".join(lines), "error": None}

'''
exclamation (!):
runs the command specified by the history index
'''
def exclamation(user_input):
    '''
    runs the command specified by the history index.
    '''
    # if an exclamation is not attached
    if not user_input.startswith("!"):
        return None

    num_str = user_input[1:]

    # if num is NOT a digit, error message
    if not num_str.isdigit():
        return None # only handle numbers after !

    num = int(num_str)  # typecast num as an int to check for boundary issue

    # if num is out of the range of cmd history, error message
    if num < 1 or num > len(cmd_history):
        return None
    return cmd_history[num - 1]

'''
whoami: 
displays the username of the logged in user
'''
def whoami(parts):
    '''
    displays the username of the logged in user.
    '''
    try:
        # get the user from getpass library
        user = getpass.getuser()
        return {"output": user, "error": None}
    except Exception as e:
        return {"output": None, "error": f"whoami: {str(e)}"}

'''
clear
clears the terminal screen
'''
def cls(parts=None):
    '''
    clears the terminal screen.
    '''

    # ANSI escape sequence to clear the screen and move the cursor to the top-left corner
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

    # prints an empty command prompt after clearing the terminal
    redraw_prompt("", 0)
    return {"output": None, "error": None}

'''
piping: 
handles piping of commands as well as redirects
'''
def piping(command_list):
    prev_output = None
    results = []

    # handles redirection if requested
    for cmd_dict in command_list:
        if cmd_dict.get("infile"):
            try:
                with open(cmd_dict["infile"], "r", encoding = "utf-8") as f:
                    cmd_dict["input"] = f.read()
            except FileNotFoundError:
                return {"output": None, "error": f"{cmd_dict['cmd']}: {cmd_dict['infile']}: No such file"}

        # piping the last output command
        if prev_output is not None:
            cmd_dict["input"] = prev_output
    
    # executes the command
    result = execute_command(cmd_dict)

    # grab the outfile
    if cmd_dict.get("outfile"):
        # grab the output
        #if cmd_dict.get("output"):
            # change to append mode
        #    mode = "a"
        #else:
            # change to write mode
        #    mode = "w"
        # open the output file
        mode = "a"
        try:
            with open(cmd_dict["outfile"], mode, encoding = "utf-8") as f:
                if result.get("output"):
                    # write to the output file
                    f.write(result["output"] + "\n")
        except Exception as e:
            return {"output": None, "error": f"{cmd_dict['cmd']}: {str(e)}"}
        
    prev_output = result.get("output")
    results.append(result)

    # return the results
    if results:
        return results[-1]
    else:
        return {"output": None, "error": None}

'''
execute_command
executes the command given on the command dictionary 
'''
def execute_command(command_dict):
    """
    Command dispatcher - routes commands to their respective functions
    input: dict: {"input":string,"cmd":string,"params":list,"flags":string}
    output: dict: {"output":string,"error":string}
    """
    command_map = {
        # Add more commands here as you implement them
        'pwd': pwd,
        'ls': ls,
        'history': history,
        'mkdir': mkdir,
        'whoami': whoami,
        'exit': exit,
        'cd': cd,
        'wc':wc,
        'sort': sort,
        'mv' : mv, 
        'head': head, 
        'tail': tail,
        'cat': cat,
        'less': less,
        'rm': rm,
        'cp': cp,
        'grep': grep,
        'help': help,
        'cls': cls,
        'chmod': chmod
        # etc.ex
    }

    cmd_name = command_dict.get('cmd', '').lower()

    # snippet to handle the 'help' command
    if cmd_name in command_map:
        if cmd_name == "help":
            return command_map[cmd_name](command_dict, command_map = command_map)
        else:
            return command_map[cmd_name](command_dict)
    else: # if command does not exist
        return {"output": None, "error": f"Command '{cmd_name}' not found"}

'''
redraw_prompt
redraws the current prompt and command, placing the cursor at the correct position
'''
def redraw_prompt(cmd, cursor_position):
    '''
    redraws the current prompt and command, placing the cursor at the correct position
    '''
    # clears the current line
    sys.stdout.write("\r\033[K")

    try:
        cwd = os.getcwd()

    except:
        cwd = "/"
    # prints the prompt with the current working directory and command
    sys.stdout.write(f"{cwd}$ {cmd}")
    sys.stdout.flush()

    # moves the cursor to the correct position
    prompt_length = len(f"{cwd}$ ")
    move = prompt_length + cursor_position
    sys.stdout.write(f"\r\033[{move+1}C")
    sys.stdout.flush()


if __name__ == "__main__":
    # initial command is empty
    cmd = ""
    # curson position starts at 0
    cursor_position = 0
    # print the initial command prompt
    redraw_prompt(cmd, cursor_position)

    # loop forever
    while True:  
        # grab a character from the user
        char = getch()  

        # if ctrl-c or exit command is pressed, exit the program
        if char == "\x03" or cmd == "exit":
            raise SystemExit("\nBye.")

        # if backspace is pressed, remove the last character from cmd
        elif char == "\x7f":
            if cursor_position > 0:
                cmd = cmd[:cursor_position - 1] + cmd[cursor_position:]
                cursor_position -= 1
            redraw_prompt(cmd, cursor_position)

        # identify arrow keys and handle accordingly
        elif char in "\x1b":
            # detect the full excape sequence
            null = getch()
            # grab the direction character
            direction = getch()

            # if the up arrow is pressed
            if direction in "A":
                # get the previous command from history (if there is one)
                if history_index > 0:
                    history_index -= 1
                    cmd = cmd_history[history_index]
                    # set the cursor position to the end of the command line
                    cursor_position = len(cmd)

            # if the down arrow is pressed
            elif direction in "B":
                # get the next command from history (if there is one)
                if history_index < len(cmd_history) - 1:
                    history_index += 1
                    cmd = cmd_history[history_index]
                # if there is no next command, clear the command line
                else:
                    history_index = len(cmd_history)
                    cmd = ""
                # set the cursor position to the end of the command line
                cursor_position = len(cmd)
            # if the right arrow is pressed
            elif direction == "C":
                # move the cursor right, if not at the end of the command
                if cursor_position < len(cmd):
                    cursor_position += 1
            # if the left arrow is pressed
            elif direction == "D":
                # move the cursor left, if not at the beginning of the command
                if cursor_position > 0:
                    cursor_position -= 1
            
            redraw_prompt(cmd, cursor_position)

        # if enter is pressed, execute the command
        elif char in "\r":
            # move to a new line
            sys.stdout.write("\n")
            user_input = cmd.strip()

            # Executes the !x history command
            history_cmd = exclamation(user_input)
            if history_cmd:
                # if a valid history command was found, use it as the user input
                user_input = history_cmd
                print(user_input)   # prints the command before executing it
            
            # Add the command to history if it's not empty
            if user_input:
                # avoid duplicate consecutive entries
                cmd_history.append(user_input)
                # set the history index to the end of the list
                history_index = len(cmd_history)

                # parse the command into a list of commands (for piping)
                command_list = parse_cmd(user_input)
                if command_list:
                    # execute the command(s)
                    result = piping(command_list)
                    # print the output and error (if any)
                    if result["output"]:
                        print(result["output"])
                    if result["error"]:
                        print(f"Error: {result['error']}")
            
            # reset the command line and cursor position
            cmd = ""
            cursor_position = 0
            redraw_prompt(cmd, cursor_position)
        # if a regular character is pressed
        else:
            # insert the character at the current cursor position
            cmd = cmd[:cursor_position] + char + cmd[cursor_position:]
            cursor_position += 1
            redraw_prompt(cmd, cursor_position)


