import httplib
import urllib
import json
import optparse

params = urllib.urlencode({'username': 'anu', 'password': 'pass'})

headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
conn = httplib.HTTPConnection("localhost", 8888)

conn.request("POST", "/", params, headers)
response = conn.getresponse()
key = json.loads(response.read())['key']


def get_news_details(keyword):
    params = urllib.urlencode({'key': key, 'keyword': keyword})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", 8888)
    conn.request("POST", "/fetch_news", params, headers)
    response = conn.getresponse()
    print response.status, response.read()

if __name__ == '__main__':

    parser = optparse.OptionParser(usage="usage: %prog [options] filename",
                                   version="%prog 1.0")

    parser.add_option('-f', '--fetch_news_details',
                      dest="fetch_news_details",
                      help='fetch news details',
                      )

    (options, args) = parser.parse_args()

    if options.fetch_news_details:
        get_news_details(options.fetch_news_details)
