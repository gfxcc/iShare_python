#
# created by Yong Cao on May/3/2017
#
#
#
from time import gmtime, strftime

class Log(object):
    def __init__(self, msg):
        self.msg = msg
        print('%10s IN', self.msg)

    def __del__(self):
        print('%10s OUT', self.msg)

    def print_log(self, level, msg):
        print strftime("%Y-%m-%d %H:%M:%S ", gmtime())
        print ('[%6s]:%s', level, msg)

    def omit_syntax(self):
        pass

