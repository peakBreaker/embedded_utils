"Utilities file, here you may find things like config handeling etc"
import json


def getConfig(config):
    "Gets some config"
    if config == 'port':
        with open('config.json', 'r') as f:
            fileText = f.read()
            configs = json.loads(fileText)
            port = configs.get('port', False)
            if not port:
                print "Port is not configured, ending!"
                return False
            else:
                return port
    else:
        print "Asked for invalid config, returning False"
        return False

def portConfig(port):
    "Configures the port used for sending the commands"
    settings = {}
    # First we check the initial configurations
    with open('./config.json', 'r') as cfg:
        fileText = cfg.read()
        print "read file! -- %s" % fileText
        try:
            settings = json.loads(fileText)
        except:
            print "File doesnt exist, or isnt properly encoded to json"
        finally:
            settings['port'] = port if port is not False else settings['port']
    # Next we update the config file
    with open('./config.json', 'w') as cfg:
        saveJson = json.dumps(settings)
        print saveJson
        cfg.write(saveJson)
    # Finally we print something useful and return
    print "Successfully set port to %s" % settings['port']
    return
