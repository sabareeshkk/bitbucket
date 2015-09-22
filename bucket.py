import cookielib
import urllib2
import base64
import json
import pprint
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    api = API('sabareeshk', 'valiyakkunnu')
    print "heloo"
    result = api.get_commits('rawdatatech', 'proman', '41fa551e4d2315fe3d107595fbba026b9b181ac3')
    pprint.pprint(result)
    return json.dumps(result)

class API():
    api_url = 'http://bitbucket.org/api/2.0/'

    def __init__(self, username, password, proxy=None):
        encodedstring = base64.encodestring("%s:%s" % (username, password))[:-1]
        self._auth = "Basic %s" % encodedstring
        self._opener = self._create_opener(proxy)

    def _create_opener(self, proxy=None):
        cj = cookielib.LWPCookieJar()
        cookie_handler = urllib2.HTTPCookieProcessor(cj)
        if proxy:
            proxy_handler = urllib2.ProxyHandler(proxy)
            opener = urllib2.build_opener(cookie_handler, proxy_handler)
        else:
            opener = urllib2.build_opener(cookie_handler)
        return opener

    def get_issues(self, username, repository):
        query_url = 'https://bitbucket.org/api/2.0/repositories/'
        return self._get_result(query_url)
        
    def get_commits(self, username, repository, revision):
        query_url = 'https://bitbucket.org/api/2.0/repositories/%s/%s/commits/%s' % (username, repository, revision)
        print query_url
        result = self._get_result(query_url)
        return result
    
    def _get_result(self, query_url):
        try:
            req = urllib2.Request(query_url, None, {"Authorization": self._auth })
            handler = self._opener.open(req)
        except urllib2.HTTPError, e:
            print e.headers
            raise e
        return json.load(handler)


if __name__ == '__main__':
    app.run()