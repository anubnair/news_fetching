import tornado.autoreload
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado import gen

import jwt
import datetime
import json

from utils import mongodb
from bson import json_util


def authenticate(func):
    """
    Basic authentication
    """
    def inner(self):

        username = self.get_argument('username')
        password = self.get_argument('password')

        if username == 'anu' and password == 'pass':
            encoded = jwt.encode(
                    {username: password,
                     'exp': datetime.datetime.utcnow() +
                            datetime.timedelta(seconds=1000000)},
                    'secret', algorithm='HS256'
            )

            encoded = {'error': None,
                    'key': encoded
            }
            func(self, encoded)
        else:
            func(self, {'error': 'Invalid username/Password',
            'key': None
            })
    return inner


def authentication_required(func):
    """
    Check authentication
    """
    def inner(self):
        key = self.get_argument('key')
        try:
            decoded = jwt.decode(key, 'secret')
        except jwt.ExpiredSignatureError:
            decoded = {'error': 'ExpiredSignatureError'}
            self.clear()
            self.set_status(401)
            self.finish(json.dumps(decoded))
            return
        except jwt.InvalidTokenError:
            decoded = {'error': 'InvalidTokenError'}
            self.clear()
            self.set_status(401)
            self.finish(json.dumps(decoded))
            return
        func(self, decoded)

    return inner


class MainHandler(tornado.web.RequestHandler):
    @authenticate
    def post(self, encoded):
        self.write(json.dumps(encoded))


class JsonObject:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


def get_news_details(keyword):
    """
    Get the news details from the DB
    Args:
        keyword: keyword from the client
    Returns:
        data: curresponding news details
    """
    db = mongodb.connect_to_db()
    news_data = mongodb.grep_news_using_regex(db, keyword)
    return_data = {}
    count = 1
    if news_data:
        for news in news_data:
            news_count = 'news' + str(count)
            return_data[news_count] = news
            count += 1
    return json_util.dumps(return_data)


class GetNewsDetails(tornado.web.RequestHandler):
    @authentication_required
    @tornado.web.asynchronous
    @gen.engine
    def post(self, decoded):
        """
        API to get the news
        """
        keyword = self.get_argument('keyword')
        data = get_news_details(keyword)
        # return success to the caller
        self.write(json.dumps(data))
        self.finish()


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/fetch_news", GetNewsDetails)
])

if __name__ == "__main__":

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
