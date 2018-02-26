""" 
Utilities for getting and handling logfiles.  Note: This involves no processing
of the logfile contents.
"""
from glob import glob

import re


def get_log(**kw):
    "prompts for a valid logfile"
    # Get the avaliable_logs TODO: Change from old to new
    directory = kw.get('directory', './logs')
    extension = kw.get('extension', 'json')
    print("Getting logs in :: %s" % directory)
    avaliable_logs = glob(directory + '/*.' + extension)
    if len(avaliable_logs) == 0:
        print("Found no logs!")
        return

    while True:
        # Print out avaliable_logs with index
        for idx, log in enumerate(avaliable_logs):
            print("%i : %s" % (idx, log))
        print("* : Select all logs")

        # prompt user to select log
        log_select = input("Select log by index > ")
        if log_select == '*':
            return avaliable_logs
        
        # Otherwise we check the index
        log_select = re.match(r'(\d+)', log_select)
        log_select = int(log_select.groups()[0]) if log_select is not None else None
        if log_select is None:
            print("You must type a number")
        elif log_select <= len(avaliable_logs) - 1:
            print("Selected %s" % avaliable_logs[log_select])
            return [avaliable_logs[log_select]]
