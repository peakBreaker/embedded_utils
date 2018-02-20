from serial import Serial
from serial.tools import list_ports
from datetime import datetime
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


def read_debug(ser):
    "Reads the output from serial and returns it"
    try:
        output = str(ser.readline(), 'utf-8')
        # print(output)
    except UnicodeDecodeError:
        # print("Unable to parse output from modem")
        output = ''
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


def get_port():
    "Lists information about a port - edit port for now"
    # Check if we have a device conf
    if 'device.conf' in os.listdir('./'):
        with open('./device.conf', 'r') as f:
            device = f.readline()
            user_decide = input("Press any key except q to connecting to " + device + " > ")
            if user_decide != 'q':
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
    with open("./device.conf", 'w') as f:
        f.write(ports.get(select, 0).device)
    
    return ports.get(select, 0).device
    
if __name__ == '__main__':
    reset_modem()
