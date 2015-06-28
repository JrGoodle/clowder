import os
import time
import config
import sys

def toFile(string):
    '''
    This function receives various login messages during a typical
    'ev' invocation, prints them to the screen, and then puts the 
    messages in the log file for the day in addition to a time stamp.
    If the log file for the day does not exist, which happens during 
    the first invocation of any 'ev' commands, it is created by this
    function. Further, if the login directory does not exits, it
    is also created here.
    '''
    print string
    home = os.path.expanduser('~')
    logDir = home + '/.ev/logs'
    if not os.path.exists(logDir):
        os.makedirs(logDir)

    today = time.strftime('%Y-%m-%d')
    evLogFile = logDir + '/' + today + '.log'
    # if the log file does not exist, open it with 'write' access.
    # otherwise, open it with append access.
    if not os.path.isfile(evLogFile):
        f = open(evLogFile, 'w')
        f.write('\'ev\' command logs for ' + today + '\n\n')
    else:
        f = open(evLogFile, 'a')
    
    timeStamp = time.strftime('%Y-%m-%d %H:%M:%S')
    f.write(timeStamp + '\t\t' + string + '\n')
    f.close()

def adb(arg1):
    d = config.load()
    clear = 'adb logcat -c'
    logDir = d['EVLOGS']
    if not os.path.exists(logDir):
        os.makedirs(logDirs)
    if arg1 == 'all':
        r = subprocess.call(clear, shell=True)
        if r != 0:
            ev.log.toFile('Command "' + command + '" returned:' + str(r))
            ev.log.toFile('Aborting.\n\n')
            sys.exit()
        today = time.strftime('%Y-%m-%d_%H-%M-%S')
        command = 'adb logcat > ' + logDir + '/' + today + '.log'
        ev.utilities.unknownArg(command)
    else:
        ev.utilities.unknownArg('ev log adb', arg1)


