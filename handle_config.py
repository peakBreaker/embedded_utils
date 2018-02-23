import yaml
import os
import re
from embedded_utils.serial import get_port
from glob import glob


def get_log(**kw):
    avaliable_logs = glob('./logs/*')
    if len(avaliable_logs) == 0:
        print("Found no logs!")
        return None

    while True:
        # Print out avaliable_logs with index
        for idx, log in enumerate(avaliable_logs):
            print("%i : %s" % (idx, log))

        # prompt user to select log
        log_select = re.match(r'(\d+)', input("Select log by index > "))
        log_select = int(log_select.groups()[0]) if log_select is not None else None
        if log_select is None:
            print("You must type a number")
        elif log_select <= len(avaliable_logs) - 1:
            print("Selected %s" % avaliable_logs[log_select])
            return avaliable_logs[log_select]


def get_config(silent, cfg=None):
    "Takes a config object and prompts user for missing values"
    # First check if config is None
    if cfg is None:
        print("Seems like we need to create a new config")
        cfg = {}
        # First get the source for input
    else:
        print("              ----- CONFIG INFO -----\n\
              If not in silent mode, you will now be prompted to change/set\n\
              Set values.  All prompts defaults to N, so you can quick skip\n\
              --- INPUT TYPE: F means File - S means Serial\n\n\
              --- NOTE ON HIGHLIGHT:\n\
              You will NOT be prompted about highlighting configs. Change the\n\
              config.yml file with colors and flags in CAPITAL LETTERS to \n\
              configure the highlighting.\n\
              -----------------------")

    while True:
        # First get the input type
        if 'input_type' in list(cfg.keys()) and not silent:
            print("Input type is %s" % cfg['input_type'])
            if input('Change input type? [Y/N] > ') is 'Y':
                del cfg['input_type']

        if 'input_type' not in list(cfg.keys()) and not silent:
            input_type = input('Get input from File or Serial? [S/F] > ')
            if ('S' not in input_type) or ('F' not in input_type):
                cfg['input_type'] = input_type
            else:
                print("invalid input, type S or F")
                continue

        # Next get the source
        if cfg['input_type'] is 'S':
            print("Current port is %s" % cfg.get('input_source', None))
            if not silent:
                change = input('Change? [Y/N] > ')
                change = 'Y' if change is 'Y' else 'N'
                if change is 'Y':
                    print("Getting port")
                    cfg['input_source'] = get_port()

        elif cfg['input_type'] is 'F':
            print("Current file is %s" % cfg.get('input_source', None))
            if not silent:
                # Check if we need to set new file
                if cfg.get('input_source', None) is None:
                    change = 'Y'
                else:
                    change = input('Change? [Y/N] > ')
                    change = 'Y' if change is 'Y' else 'N'

                # Evaluate the change flag
                if change is 'Y':
                    print("Getting logfiles from the logs folder")
                    cfg['input_source'] = get_log()
                    print("PROTIP: Pipe the output from reading logs into less")
                    print("like this: $ python color_debug.py -s | less")
        
        return cfg


def get_highlight(cfg, Mode=None):
    """ Helper function
    
    Looks at the selected highlighting and highlight config and returns
    a new configuration dict based on the set configs.
    
    This enables multi mode highlighting"""
    # Parse the colors
    mode_highlight = cfg.get(Mode, False)
    selected_mode = cfg.get('highlight_select', None)
    # print("Avaliable modes are %s" % cfg.get('highlight_modes'), None)
    # if input("Selected mode is %s. Change? [Y/N] > " % selected_mode) is 'Y'

    # Get the highlighting modes
    mode_highlight = cfg.get(selected_mode, [{}]) if not mode_highlight else mode_highlight
    all_highlight = cfg.get('all', [{}])

    # Append all highlight on mode highlight so mode highligh goes first
    mode_highlight += all_highlight
    # print(cfg['highlight'])
    return mode_highlight


def save_config(cfg):
    with open("config.yml", 'w') as f:
        f.write(yaml.dump(cfg, default_flow_style=False))


def load_config(silent=False):
    "Loads the config.yml file in the directory and returns a dict of conf"
    # First get or prompt for config
    if 'config.yml' in os.listdir('./'):
        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
    elif silent:
        print("Found no valid config and silent mode is on")
        print("Run the program without silent mode or provide a valid config")
        print(" ----- QUITTING ----")
        return False
    else:
        print("No config file, creating one")
        cfg = None

    # Next evaluate the config
    cfg = get_config(silent, cfg)

    # Finally save
    print("Program running with this config:")
    print(yaml.dump(cfg, default_flow_style=False))
    save_config(cfg)

    return cfg
