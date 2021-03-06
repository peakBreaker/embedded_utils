from serial import Serial
from serial.tools import list_ports
from datetime import datetime
import time
import re
import os


def get_port_by_name(portname):
    "Looks up all connected ports and gets the one with portname string in it"
    port = [port for port in list_ports.comports()
            if portname in str(port.product)][0]
    return port


def get_port_by_manufacturer(manufacturer):
    "Looks up ports by manufacturer"
    port = [port for port in list_ports.comports()
            if manufacturer in str(port.manufacturer)][0]
    return port


def read_debug(ser, return_false=False):
    "Reads the output from serial and cleans it up a bit"
    try:
        output = str(ser.readline(), 'utf-8')
        # print(output)
    except UnicodeDecodeError:
        print("Unable to parse output from modem")
        output = '' if not return_false else False
    finally:
        return output


ENABLE_MANUAL = False
def reset_devices():
    "Gets port for arduino and sends reset signal"
    #ino = get_port()
    if ENABLE_MANUAL:
        input("Reset the device and press enter to continue")
        return
    port = get_port_by_manufacturer("Arduino")
    device = port.device
    print("connecting to Arduino at " + str(device))
    with Serial(device, 9600, timeout=1) as ser:
        reset_state = False
        reset_timeout = 0
        while True:
            # Reset logic
            output = str(ser.read(1000), 'utf-8')
            if output != '' and not reset_state:
                print(output)
            elif reset_state and "Done" in output:
                reset_state = False
                print("Reset successful!")
                return
            elif reset_timeout > 15:
                break
            elif reset_state:
                print(".", end='', flush=True)
            elif not reset_state and reset_timeout > 4:
                print("Resetting devices!")
                ser.write(b'R')
                reset_state = True
            else:
                reset_timeout += 1
    print("Failed at resetting devices, try again later")
    with open('./errors.log', 'a') as f:
        f.write('Arduino reset failure at : ' + str(datetime.now().isoformat())  + '\n')
    return False


def get_port(**kw):
    "Lists information about a port - edit port for now"
    # choosing device TODO: There are better ways of doing this
    dev = kw.get('dev', None)
    silent = kw.get('silent', False)
    print("GETTING PORT FOR :: %s" % dev)
    conf_file = 'device.conf' if dev is "device" else 'default.conf'
    if conf_file in os.listdir('./'):
        with open(conf_file, 'r') as f:
            device = f.readline()
            user_decide = False
            if not silent:
                user_decide = input("Press any key except q to connecting to " + device + " > ")
            if silent or user_decide != 'q':
                print("Connecting to " + device)
                return device

    # First get the ports
    print("Avaliable devices:")
    ports = {}
    for idx, port in enumerate(list_ports.comports()):
        print(str(idx) + " - " + str(port))
        ports[idx] = port

    # Then get user select
    select = None
    while True:
        select = input("Select device by index > ")
        select = re.match(r"(\d+)", select)
        if select is not None:
            select = int(select.groups()[0])
            print("You selected " + str(select))
            break
        else:
            print("Invalid argument!")

    # Write it to file
    with open(conf_file, 'w') as f:
        f.write(ports.get(select, 0).device)

    return ports.get(select, 0).device


def connect_serial(port=False, baud=115200):
    "Helper function for getting the serial connection"
    if not port:
        port = get_port()
    return serial.Serial(port, baud, timeout=1)


if __name__ == '__main__':
    reset_modem()


############################ MOCK TEST CLASS ################################
# When creating application unittests, use this class instead of the module #
# To get a mock serial object -- Its a simple little machine for now, but   #
# I will make it more proper                                                #
#############################################################################

class mock_serial():
    "Serial mocking class"
    def __init__(self, *args):
        print("Initializing mock serial")
        self._debug = args
        self.outputgen = self.read_debug_gen()

    def __enter__(self):
        print("Entered mock serial object")
        return self

    def read_debug_gen(self):
        while True:
            for arg in self._debug:
                yield arg
                time.sleep(1)

    def read_debug(self):
        print("Reading debug")
        return next(self.outputgen)

    def __exit__(self, arg1, arg2, arg3):
        print("Exited mock serial object .. got args :: ")
        print("arg1 :: %s" % arg1)
        print("arg2 :: %s" % arg2)
        print("arg3 :: %s" % arg3)
