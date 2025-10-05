# 5143 Advanced Operating Systems
### Shell Project - Implementation of a Basic Shell
##### Group Members: Jadyn Dangerfield, Andrew Huff, Laxminarasimha Soma
##### jadangerfield0515@my.msutexas.edu
##### adhuff0205@my.msutexas.edu
##### lsoma0109@my.msutexas.edu

## Overview
##### In this project, we implemented a basic shell using Python. Below, we have listed the assignment rubric which includes who worked on each command, and their completion status.

## Instructions
#### To run this shell, you must execute the following:
#### 1. Ensure access to the repository
#### 2. Switch over to the Files directory
#### 3. Type the command "python shell.py"
#### 
#### Now that the program is running, similarly use it to navigate the emulated terminal!

## Commands
|**Command**|**Flags/Parameters**|**Description**|**Author**|
|-------|------------------------|---------------|----------|
|`ls`|`-a`|Lists all files, including hidden ones|Jadyn|
||`-l`|Long listing format|Jadyn|
||`-h`|Human-readable file sizes|Jadyn|
|`mkdir`||Creates a direactory|Andrew|
|`cd`||Change to the home directory if no argument is provided|Jadyn|
||`directory`|Change to a named directory|Jadyn|
||`~`|Returns to the home directory|Jadyn|
|`pwd`||Prints the current working directory|Jadyn|
|`cp`|`file1 file2`|Copy file1 to file2|Andrew|
|`mv`|`file1 file2`|Move or rename file1 to file2|Soma|
|`rm`|`-r`|Recursively deletes a directory|Andrew|
|`cat`|`file`|Displays contents of a file|Soma|
|`head`|`file -n`|Displays the first `n` lines of a file|Jadyn|
|`tail`|`file -n`|Displays the last `n` lines of a file|Jadyn|
|`grep`|`'pattern'` `file`|Search for a pattern in a file|Andrew|
|`wc`|`-l`|Counts lines in a file|Soma|
||`-w`|Counts words in a file|Soma|
|`chmod`|`xxx`|Change file permissions|Soma|
|`history`||Show a history of all executed commands|Andrew|
|`!x`||Re-execute command x from history|Andrew|
|`help`||Prints help information about a command|All|
|`cls`||clears the terminal|Jadyn|
|`whoami`||Prints who the user is|Andrew|
|`Arrow Keys`|`Up`|Gets the previous command from history|Jadyn|
||`Down`|Gets the next command from history (if there is one) or clears the command line|Jadyn|
||`Left`|Moves the cursor to the left|Jadyn|
||`Right`|Moves the cursor to the right|Jadyn|
|`Prompt line acts correct`|||Jadyn|
|`Piping`|||Andrew|

## References
#### Our references used were as follows:
#### 1. GeeksforGeeks
#### 2. Stackoverflow (whoami)
#### 3. Chatgpt
