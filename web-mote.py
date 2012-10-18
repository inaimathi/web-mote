import web, os, json
import util, conf, player 

urls = (
    '/show-directory', 'showDirectory',
    '/shuffle', 'shuffle',
    '/play', 'play',
    '/command', 'command',
    '.*', 'index'
)

app = web.application(urls, globals())
        
class showDirectory:
    def POST(self):
        i = web.input()
        if i == {} or i['dir'] == "root":
            return util.entriesToJSON(conf.root)
        else: 
            assert util.isInRoot(i['dir'])
            return util.dirToJSON(i['dir'])

class shuffle:
    def POST(self):
        web.debug(["ERRY DAY I'M SHUFFLIN", web.input()])

class play:
    def POST(self):
        t = web.input()['target']
        if os.path.isfile(t):
            web.debug(["PLAYING A SINGLE FILE", t])
            player.play([t])
        elif os.path.isdir(t):
            web.debug(["PLAYING A DIRECTORY", t])
        else:
            files = json.loads(t)
            web.debug(["DEALING WITH A FILE LIST", files])

class command:
    def POST(self):
        assert player.activePlayer and web.input()['command']
        player.commandQueue.put(web.input()['command'])

class index:
    def GET(self):
        raise web.seeother("/static/web-mote.html")

if __name__ == "__main__":
    app.run()
