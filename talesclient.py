import json
import urllib2

class Tale(object):

    def __init__(self, name, size, points, fileUrl, imageUrl, thumbUrl):
        self.name = name
        self.size = size
        self.points = points
        self.fileUrl = fileUrl
        self.imageUrl = imageUrl
        self.thumbUrl = thumbUrl

    def __str__(self):
        return self.name


class TalesClient(object):
    SITE_URL = 'http://tales.sneakybox.lt/'

    def __init__(self):
        self.client = urllib2.build_opener(urllib2.HTTPRedirectHandler())
        defaultHeaders = [('User-Agent', 'Mozilla/5.0'),
                          ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')]
        self.client.addheaders = defaultHeaders

    def doRequest(self, url, data=None):
        return self.client.open(url, data)

    def getTaleList(self):
        tales = []
        response = self.doRequest(TalesClient.SITE_URL + 'json_tale_list.php')
        content = response.read()
        baseUrl = TalesClient.SITE_URL + 'tales/'
        for el in json.loads(content):
            url = baseUrl + el['audiofile']
            imageUrl = baseUrl + el['image']
            thumbUrl = baseUrl + el['thumb']
            tales.append(Tale(el['name'].encode('utf-8'), el['size'], el['pionts'], url, imageUrl, thumbUrl))
        return tales
