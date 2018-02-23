from colored import fg, bg, attr
from serial import Serial
import argparse
from embedded_utils.handle_config import load_config

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-s', '--silent', help='Runs with config.yml without \
                    prompting user or does nothing if invalid config',
                    required=False, action='store_true')
args = vars(parser.parse_args())


def viza_highlight(**kw):
    "Function responsible for taking the output and highligting it for debug"
    # Getting the string
    output = kw['string'].upper()

    # Guard against empty lines
    if output.strip() == '' or output.strip() == '\n':
        return

    # Getting the lists of colors
    for highlight in kw['highlight']:
        for color, flags in highlight.items():
            if len([flag for flag in flags if flag in output]) > 0:
                print(fg(color) + output + attr('reset'))
                return
    # If no color valid for output we print normal
    print(output)


def output_from_file(file):
    with open(file, 'r') as f:
        return [line for line in f]


def output_from_serial(config):
    port = config['input_source']
    print("Connecting to USB_UART at " + str(port))
    with Serial(port, 115200, timeout=1) as ser:
        while True:
            output = read_debug(ser)
            viza_highlight(string=output, highlight=config['highlight'])

def main():
    "Handles the upper layer logic"
    # First get the configurations
    print("Silent mode is %s " % args.get('silent'))
    config = load_config(args.get('silent'))
    if not config:
        return

    # Evaluate the input source and action
    if config['input_type'] is 'F':
        output = output_from_file(config['input_source'])
        for line in output:
            viza_highlight(string=line, highlight=config['highlight'])
    elif config['input_type'] is 'S':
        output_from_serial(config)

if __name__ == '__main__':
    main()
