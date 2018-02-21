import json
from serial import Serial
from embedded_utils.serial import read_debug


def get_embedded_json(port, flag):
    """ Reads out uart from port and looks for the flag.  The flag is valid json
    with the values wanted by the programmer.
    """
    with Serial(port, 115200, timeout=1) as ser:
        wd_parse_retries = 0
        while wd_parse_retries < 7:

            # 1. Use read debug to clean up the serial output and look for flag
            output = read_debug(ser)
            if flag in output:

                # 2. Attempt to parse the json - exception handling in case of
                #    corrupted data
                try:
                    print("PARSING TO JSON :: %s" % output)
                    output = json.loads(output)
                    return output
                except Exception as e:
                    print("FAIL AT PARSING BAT VOLT :: RETRY :: %i" %
                          wd_parse_retries)
                    print(e)
                    wd_parse_retries += 1
            else:
                print(output)
        
        # 3. If we fail too many times we just return invalid json
        return json.loads('{"SENSOR_ID": 7, "status": 2, "value": -1}')
