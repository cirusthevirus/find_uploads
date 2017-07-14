#!/usr/bin/env python3
''' Finds music that needs to be uploaded from a given timestamp.'''

import os
import time
import shutil
import per_tools

def run(ts):
    # Scan input based on given timestamp and print accepted files
    _file_list = [os.path.join(source, f) for f in os.listdir(source) if
                  (f[-4:] == ".mp3" or f[-4:] == ".aac") and \
                  time.gmtime(os.path.getmtime( os.path.join(source, f))) > ts]


    # Second level of recursive search
    for folder in os.listdir(source):
        if folder[0] != '.':
            for item in os.listdir(os.path.join(source, folder)):
                if (item[-4:] == ".mp3" or item[-4:] == ".aac") \
                        and time.gmtime(os.path.getmtime(
                        os.path.join(source, folder, item))) > ts:
                    _file_list.append(os.path.join(source, folder, item))

    # Display files found
    print("\n%s files found in total.\n" % len(_file_list))

    # Request copy directory
    os.chdir(source)
    destination = input("Please provide destination directory or path\
                        (relative to source):\n")
    if not os.path.exists(destination):
        try:
            os.mkdir(destination)
        except:
            print("Critical error while creating destination directory. \
                  Terminating ...")
            quit()

    print("Preparing for file copying ...")
    iteration = 0
    per_tools.print_progress_bar(iteration, len(_file_list))
    for file in _file_list:
        iteration += 1
        per_tools.print_progress_bar(iteration, len(_file_list))
        shutil.copy2(file, os.path.join(destination, os.path.basename(file)))

    print("Copy complete.")



if __name__ == "__main__":
    _dir_save = os.getcwd()
    source = "/path/to/music/source"
    print("Working with source:\t%s" % source)
    print("Note that the recursive depth of the file search is 2.")
    print("Please enter a timestamp to filter music by: ")
    _input = input("This must have format %d/%m/%y," +
        " e.g. 30/11/01 for 30 Nov 2001\n")
    _input = _input.strip()
    ts = time.strptime(_input, "%d/%m/%y")
    run(ts)
    os.chdir(_dir_save)
