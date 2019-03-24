"Contains some functions for sending AT Commands to devices"

from embedded_utils.serial import read_debug
from time import sleep

def send_cmd_print_resp(ser, cmd):
    "Sends a command and prints the results. returns true if it got response"
    ser.write(cmd + b'\r\n')
    got_response = False
    while True:
        line = read_debug(ser, True)
        if line == '':
            break
        else:
            # print("Command in line? :: %s" % (str(cmd, 'utf-8') not in line))
            got_response = True if str(cmd, 'utf-8') not in line else got_response
            print(line, end='', flush=True)
    return got_response


def send_cmd_get_resp(ser, cmd):
    "Sends a command and prints the results. returns a list of responses"
    print("Sending command :: %s" % cmd)
    ser.write(cmd + b'\r\n')
    responses = []
    while True:
        line = read_debug(ser, return_false=True)
        if line == '':
            break
        elif not line:
            pass
        else:
            # print(line)
            # print("Command in line? :: %s" % (str(cmd, 'utf-8') not in line))
            responses.append(line if str(cmd, 'utf-8') not in str(line) else None)
    responses = list(filter(None.__ne__, responses))
    # print("Responses :: ")
    # print(responses)
    return responses


def send_cmd_persistent(ser, cmd, **kw):
    "Keeps sending command till it gets an OK back"
    retval = True
    retries = kw.get('retries', 5)
    iterations = 0
    while iterations < retries:
        sleep(0.3)
        retval = send_cmd_get_resp(ser, cmd)
        if "OK\r\n" in retval:
            print('Got OK')
            break
        else:
            iterations += 1
            continue
    else:
        return False
    return retval
