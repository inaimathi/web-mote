from subprocess import Popen, PIPE
import web, os, json
import util, conf

urls = (
    '/show-directory', 'showDirectory',
    '/shuffle-directory', 'shuffleDirectory',
    '/play', 'play',
    '/command', 'command',
    '.*', 'index'
)
app = web.application(urls, globals())

class showDirectory:
    def POST(self):
        if web.input() == {}:
            res = util.entriesToJSON(conf.root)
        elif web.input()['dir'] == "root":
            res = util.entriesToJSON(conf.root)
        else:
            res = util.dirToJSON(web.input()['dir'])
        return res

class shuffleDirectory:
    def POST(self):
        web.debug(["SHUFFLING", web.input()])

class play:
    def POST(self):
        try:
            playFile(web.input()['file'])
        except:
            web.debug(web.input())

def playFile(aFile):
    if os.path.exists(aFile):
        if conf.currentPlayer:
            conf.currentPlayer[1].terminate()
        t = util.typeOfFile(aFile)
    ## mplayer suicides if its stdout and stderr are ignored for a while,
    ## so we're only grabbing stdin here
        conf.currentPlayer = (conf.player[t][0], Popen(conf.player[t] + [aFile], stdin=PIPE))

class command:
    def POST(self):
        cmd = web.input()['command']
        if conf.currentPlayer:
            (playerName, proc) = conf.currentPlayer
            proc.stdin.write(conf.commands[playerName][cmd])
            if cmd == 'stop':
                conf.currentPlayer = False

class index:
    def GET(self):
        raise web.seeother("/static/web-mote.html")

if __name__ == "__main__":
    app.run()

