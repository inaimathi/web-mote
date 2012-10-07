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
    def GET(self):
        if web.input() == {}:
            return util.entriesToJSON(conf.root)
        elif web.input()['dir'] == "root":
            return util.entriesToJSON(conf.root)
        else:
            return util.dirToJSON(web.input()['dir'])

class shuffleDirectory:
    def POST(self):
        web.debug(web.input())

class play:
    def POST(self):
        global player
        player = Popen(
            ["mplayer", "/home/inaimathi/videos/friendship-is-magic/1s01e--pilot-mare-in-the-moon.mp4"],
            stdin=PIPE, stdout=PIPE, stderr=PIPE)
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

