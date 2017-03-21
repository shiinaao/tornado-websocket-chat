import tornado.ioloop
import tornado.web
import tornado.websocket
import os
from datetime import datetime


class ChatSocket(tornado.websocket.WebSocketHandler):
    pool = set()

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        print(args, kwargs)
        ChatSocket.pool.add(self)
        # self.write_message('Connected')

    def on_message(self, message):
        # uid = self.get_secure_cookie('uid').decode()
        # print(uid)
        # ChatSocket.update({
        #     'uid': uid,
        #     'msg': message,
        #     'time': datetime.now().strftime('%m-%d %H:%M:%S')
        # })
        pass

    def on_close(self):
        print('1 member logout')

    def send_error(self, *args, **kwargs):
        # self.write_message('send_error')
        pass

    def write_error(self, status_code, **kwargs):
        # self.write_message('write_message')
        pass

    @classmethod
    def update(cls, msg):
        for item in cls.pool:
            item.write_message(msg)

class ChatWebHandel(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')

    def get(self, *args, **kwargs):
        self.render('web-chat/dist/index.html')

    def post(self, *args, **kwargs):
        uid = self.get_argument('uid', None)
        if uid:
            self.write({'hashid': hash(uid)})

route = [
    (r'/chatws', ChatSocket),
    (r'/chat', ChatWebHandel)
]


def make_app(*args, **kwargs):
    return tornado.web.Application(route, *args, **kwargs, static_path=basedir+'/web-chat/dist/static')


basedir = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()