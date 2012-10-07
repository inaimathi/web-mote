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
player = False

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
        web.debug(web.input())

class play:
    def POST(self):
        global player
        try:
            f = web.input()['file']
            if os.path.exists(f):
                if player:
                    player.terminate()
                player = Popen(["mplayer", f], stdin=PIPE)
        except:
            web.debug(web.input())

class command:
    def POST(self):
        global player
        cmd = web.input()['command']
        if player:
            player.stdin.write(conf.commands['mplayer'][cmd])
            if cmd == 'stop':
                player = False

class index:
    def GET(self):
        raise web.seeother("/static/web-mote.html")

if __name__ == "__main__":
    app.run()

