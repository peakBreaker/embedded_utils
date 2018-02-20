import argparse


class Args():
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-a", "--analysis", action="count",
                            help="Analyze the logs")
        parser.add_argument("-p", "--plot", action="count",
                            help="plot")
        self.args = parser.parse_args()
    
