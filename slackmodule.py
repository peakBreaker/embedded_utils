from slackclient import SlackClient
from getpass import getpass
from time import sleep
from subprocess import check_output
import os


class slack_post():
    "simple class for creating empty posts for other programs"
    def __init__(self, string):
        self.id = None
        self.s = string

    def __repr__(self):
        return "STATIC POST " + self.s


class slack_tester_adapter():
    "SlackAdapter design pattern for modemtesting"
    def __init__(self, **kw):
        # Declare the valid commands
        self.valid_commands = {
            "status": self.send_status,
            "sendmsg": self.send_channel_message,
            "help": self.send_help_message
        }
        # First initialize some basic slack things - Mandatory args:
        self.sc = SlackClient(kw['slack_token'])
        self.channel = kw.get('channel', None)
        # Optional arguments:
        self.modules = kw.get('modules', [])
        self.module_threads = {}
        self.version = kw.get('git_version', 'N/A')
        self.ver_desc = kw.get('ver_desc', 'N/A')
        self.test_desc = kw.get('test_desc', 'N/A')
        if kw.get('RTM', False):
            # Connect to rtm -- SlackLoginError -- with_team_state=False
            if self.sc.rtm_connect():
                print("## Successfully initialized the slackmodule with RTM! ##")
            else:
                print("An error occured in connecting to rtm")

    def init_testing(self):
        "Writes test descriptions and threads to slack channel"
        self.desc_thread = self.send_channel_message(self.version +
                              " || VERSION DESC: " + self.ver_desc +
                              " || TEST DESC: " + self.test_desc)

        # Iterate through the modules and assign a thread
        for i, m in enumerate(self.modules):
            m.id = i
            module_desc = "*:: MODULE %i ::* %s " % (i, repr(m))
            _thread = self.send_channel_message(module_desc)
            self.module_threads[i] = _thread
            print("Thread is %s for module number %i" % (_thread, i))
            # Write a logfile - first find lognum
            _testnum = len(os.listdir('./tests/'))
            print('found %i number of prev tests' % _testnum)
            m.filename = './tests/' + str(_testnum) + "_" + str(_thread) + '.txt'
            # Write the data to a file for logs
            with open(m.filename, 'a') as f:
                f.write(self.ver_desc + " || " + self.test_desc + "\n")
                f.write(self.channel + "\n")
                # Write threads
                f.write(str(_thread) + "\n")


    def __repr__(self):
        git_version = check_output(['git', 'rev-parse', '--short', 'HEAD'])
        return "Currently running slackmodule version : " + str(git_version)

    def send_channel_message(self, msg):
        "Sends a new message to the channel and returns its thread"
        send_success = self.sc.api_call(
           "chat.postMessage",
           channel=self.channel,
           text=msg,
           as_user=True
        )
        return send_success.get('ts', 'no thread avaliable!')

    def post_to_thread(self, msg, module):
        "Posts a message to the thread"
        if msg is None:
            return
        resp = self.sc.api_call(
          "chat.postMessage",
          channel=self.channel,
          text=msg,
          thread_ts=self.module_threads.get(module.id,
                                            00.000), # TODO: add some id here
          as_user=True
        )
        with open(module.filename, 'a') as f:
            f.write(resp.get('ts', '--- no thread ---') + "\n")
        return resp

    def send_status(self, *args):
        "returns status on the module to slack"
        # First get some parameters on the object
        status = ":: Getting status from the execution :: \n\n"
        status += "SLACKBOT :: "
        status += repr(self)
        status += "\n\n*----- MODULES -----*\n"
        for i, m in enumerate(self.modules):
            status += "*MODULE #%i* : " % i
            status += "\n      REPR :: " + repr(m) + "\n"
            if getattr(m, 'status_cb', False):
                status += "\n      STATUS CB :: " + m.status_cb() + "\n"
            else:
                status += "--- NO STATUS CALLBACK ON MODULE ---\n"
        status += "*-----------------------*"
        # Finally send the message
        self.send_channel_message(status)

    def send_help_message(self, *args):
        "returns a helpmessage to slack"
        help_message = ":: HELP -- VALID COMMANDS :: \n\n"
        for k in self.valid_commands.keys():
            help_message += str(k) + " :: "
            help_message += self.valid_commands[k].__doc__
            help_message += "\n"
        help_message += "\n Type one of the [\]commands to do stuff"
        self.send_channel_message(help_message)
        
    def get_commands_messages(self):
        "Gets command from slack"
        # First do the rtm call
        while True:
            data = self.sc.rtm_read()
            data = data[0] if data != [] else False
            if not data:
                return None
            print(data)
            # Next get the text from the data and check for command flag
            if data.get('text', 'F')[0] == '\\':
                cmd, args = data['text'].split(' ')[0], data['text'].split(' ')[1:]
                # Finally run the command
                print(self.valid_commands.keys())
                self.valid_commands.get(cmd[1:], self.send_help_message)(args)
                
    def clean_thread(self, thread_ts):
        "Cleans the thread with the thread_ts timestamp identifier"
        # First parse the thread
        # try:
        #     print("Trying to parse thread id")
        #     thread_ts = float(thread_ts)
        # except:
        #     print("thread is not float!")
        #     return "Invalid thread"
        # # Delete the thread
        retval = self.sc.api_call(
            "chat.delete",
            channel=self.channel,
            ts=str(thread_ts),
            as_user=True
        )
        print(retval)
        print("## Successfully cleared thread! ##")
        return True
        
    @classmethod
    def init_from_prompt(cls, **kw):
        "Prompts the user for some basic information about the test"
        kw['git_version'] = input("What is the git version or tag? > ")
        kw['slack_token'] = getpass("Insert slack api token > ")
        #TODO: Look up previous versions to get descripions
        kw['ver_desc'] = input("Describe the version > ")
        kw['test_desc'] = input("Describe the test > ")
        return cls(**kw)


if __name__ == '__main__':
    st = slack_tester_adapter.init_from_prompt()
    while True:
        sleep(1)
        print(st.get_commands_messages())
