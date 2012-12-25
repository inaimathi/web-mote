import tornado.ioloop, tornado.web, os, json, random, time
import util, conf, sse, player

class ShowDirectory(tornado.web.RequestHandler):
    def post(self):
        try:
            dir = self.get_argument("dir")
            assert util.isInRoot(dir)
            self.write(util.dirToJSON(dir))
        except:
            self.write(util.entriesToJSON(conf.root))

class Play(tornado.web.RequestHandler):
    def post(self):
        t = self.get_argument('target')
        player.commandQueue.put('stop')
        if os.path.isfile(t):
            fileList = [t]
        elif os.path.isdir(t):
            fileList = util.deepListDir(t)
        else:
            fileList = json.loads(t)
        if self.get_argument('shuffle', False):
            random.shuffle(fileList)
        time.sleep(.5)
        ServerStatus.write_message_to_all(json.dumps(fileList), event="new-queue")
        self.write("Ok")
        [player.playQ.put(f) for f in fileList]

class ServerStatus(sse.SSEHandler): 
    _msg_timeout = None
    @classmethod
    def send(self, message, id=False, event=False):
        msg = [message, id, event]
        sse.SSEHandler._history.append(msg)
        self.write_message_to_all(*msg)
    def on_open(self):
        self.write_message(self.connection_id, event='connection_id')
        for msg in sse.SSEHandler._history[-5:len(sse.SSEHandler._history)]:
            self.write_message(*msg)
    def on_close(self):
        self.write_message_to_all(self.connection_id, event='left')

class Command(tornado.web.RequestHandler):
    def post(self):
        cmd = self.get_argument('command')
        player.commandQueue.put(cmd)

class Index(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/static/index.html", permanent=True)

urls = [(r"/", Index),
        (r"/show-directory", ShowDirectory),
        (r"/play", Play),
        (r"/command", Command),
        (r"/status", ServerStatus),
        (r".*", Index)]

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
    }

app = tornado.web.Application(urls, **settings)

if __name__ == "__main__":
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
