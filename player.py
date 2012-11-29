from multiprocessing import Queue, Process
from subprocess import Popen, PIPE, call
import os
import util, conf

############################################################
### MASSIVE AMOUNTS OF CONFIG (this should probably be in a DB somewhere)
############################################################
defaultPlayer = ["mplayer"]

### If `omxplayer` is available, use it for `mp4`s and `ogv`s (with audio output to the HDMI port)
### If not, use the default player for everything
try:
    call(["omxplayer"])
    playerTable = { 
        'mp4': ["omxplayer", "-o", "hdmi"], 
        'ogv': ["omxplayer", "-o", "hdmi"] }
except:
    playerTable = {}

commandTable = {
    'mplayer':
        {'step-backward': "\x1B[B", 'backward': "\x1B[D", 'forward': "\x1B[C", 'step-forward': "\x1B[A",
         ## down | left | right | up
         'volume-down': "9", 'volume-off': "m", 'volume-up': "0",
         'stop': "q", 'pause': " ", 'play': " "},
    'omxplayer':
        {'step-backward': "\x1B[B", 'backward': "\x1B[D", 'forward': "\x1B[C", 'step-forward': "\x1B[A",
         'volume-off': " ", #oxmplayer doesn't have a mute, so we pause instead
         'volume-down': "+", 'volume-up': "-", 
         'stop': "q", 'pause': " ", 'play': " "}
    }
### END THE MASSIVE CONFIG
############################################################
try:
    commandQueue ## Global multi-process queue to accept player commands
    playQ        ## Global multi-process queue to accept files to play
    outQ ## Message queue to communicate with external processes from the player thread
except:
    commandQueue = Queue()
    playQ = Queue()
    outQ = Queue()

def listen():
    while True:
        aFile = playQ.get()
        if util.isInRoot(aFile):
            outQ.put(['playing', aFile])
            playerCmd = __getPlayerTable(aFile)
            cmdTable = commandTable[playerCmd[0]]
            playFile(playerCmd, aFile, cmdTable)

def playFile(playerCmd, fileName, cmdTable):
    __clearQueue(commandQueue)
    activePlayer = Popen(playerCmd + [fileName], stdin=PIPE)
    while activePlayer.poll() == None:
        try:
            res = commandQueue.get(timeout=1)
            activePlayer.stdin.write(cmdTable[res])
            outQ.put(["command", res])
            if unicode(res) == unicode("stop"):
                __clearQueue(playQ)
                activePlayer.terminate()
                return False
        except:
            None
    outQ.put(("finished", fileName))
    activePlayer = False
    return True

### Local Utility
def __getPlayerTable(filename):
    global playerTable, defaultPlayer
    name, ext = os.path.splitext(filename)
    return playerTable.get(ext[1:], defaultPlayer)

def __clearQueue(q):
    while not q.empty():
        q.get()
    return True

### Start the player process
proc = Process(target=listen, args=())
proc.start()
