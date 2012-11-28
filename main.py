import tornado.ioloop, tornado.web, os, json, random, logging
import util, conf, sse, player

logging.basicConfig(filename='mote.log', level=logging.DEBUG)

class showDirectory(tornado.web.RequestHandler):
    def post(self):
        try:
            dir = self.get_argument("dir")
            assert util.isInRoot(dir)
            self.write(util.dirToJSON(dir))
        except:
            self.write(util.entriesToJSON(conf.root))

class play(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        t = self.get_argument('target')
        if os.path.isfile(t):
            fileList = [t]
        elif os.path.isdir(t):
            fileList = util.deepListDir(t)
        else:
            fileList = json.loads(t)
        if self.get_argument('shuffle', False):
            random.shuffle(fileList)
        serverStatus.write_message_to_all('playing', fileList)
        self._on_play(fileList)

    def _on_play(self, fileList):
        for f in fileList:
            player.playQ.put(f)

class serverStatus(sse.SSEHandler): 
    _msg_timeout = None
    counter = 0
    def on_open(self):
        self.write_message('connection_id', self.connection_id)

    def on_close(self):
        self.write_message_to_all('left', self.connection_id)

    def broadcast(self, title, body):
        self.write_message_to_all(title, body)

class command(tornado.web.RequestHandler):
    def post(self):
        cmd = self.get_argument('command')
        logging.debug(["GOT COMMAND", cmd])
        serverStatus.write_message_to_all('command', cmd)
        player.commandQueue.put(cmd)

class index(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/static/web-mote.html", permanent=True)

urls = [(r"/show-directory", showDirectory),
        (r"/play", play),
        (r"/command", command),
        (r"/status", serverStatus),
        (r".*", index)]

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
    }

app = tornado.web.Application(urls, **settings)

if __name__ == "__main__":
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
