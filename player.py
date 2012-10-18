from multiprocessing import Queue, Process
from subprocess import Popen, PIPE
import web, os
import util

try:
    activePlayer ## Global flag keeping track of whether there's an active player
    commandQueue ## Global multi-process queue to accept player commands
except:
    activePlayer = False
    commandQueue = Queue()

try:
    call(["omxplayer"])
    playerTable = { 'mp4': ["omxplayer"], 'ogv': ["omxplayer"] }
except:
    ## If omxplayer is unavailable, use the default player for everything
    playerTable = {}

def getPlayerCommand(filename):
    global playerTable
    name, ext = os.path.splitext(filename)
    return playerTable.get(ext[1:], ["mplayer"])

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

def play(fileList):
    global commandQueue, activePlayer, commandTable
    web.debug(fileList)
    if activePlayer:
        commandQueue.put("stop")
    for aFile in fileList:
        if util.isInRoot(aFile):
            playerCmd = getPlayerCommand(aFile)
            cmdTable = commandTable[playerCmd[0]]
            if not playFile(playerCmd, aFile, cmdTable):
                return "Done"

def playFile(playerCmd, fileName, cmdTable):
    global activePlayer, commandQueue
    web.debug(fileName)
    player = Popen(playerCmd + [fileName], stdin=PIPE)
    activePlayer = True
    while player.poll() == None:
        try:
            res = commandQueue.get(timeout=1)
            if unicode(res) == unicode("stop"):
                player.terminate()
                activePlayer = False
                return False
            else:
                player.stdin.write(cmdTable[res])
        except:
            None
    activePlayer = False
    return True
