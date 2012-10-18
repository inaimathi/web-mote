from multiprocessing import Queue, Process
from subprocess import Popen, PIPE
import web
import util, conf

try:
    activePlayer
    commandQueue
except:
    activePlayer = False
    commandQueue = Queue()

def play(fileList):
    global commandQueue, activePlayer
    web.debug(fileList)
    if activePlayer:
        commandQueue.put("stop")
    for aFile in fileList:
        if util.isInRoot(aFile):
            playerCmd = conf.player[util.typeOfFile(aFile)]
            cmdTable = conf.commands[playerCmd[0]]
            playFile(playerCmd, aFile, cmdTable)

def playFile(playerCmd, fileName, cmdTable):
    global activePlayer, commandQueue
    web.debug(fileName)
    player = Popen(playerCmd + [fileName], stdin=PIPE)
    activePlayer = True
    while player.poll() == None:
        try:
            res = commandQueue.get(timeout=1)
            if res == "stop":
                player.terminate()
                activePlayer = False
                return "Done"
            else:
                player.stdin.write(cmdTable[res])
        except:
            None
    activePlayer = False
