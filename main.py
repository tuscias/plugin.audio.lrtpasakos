import sys
import json
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
from urlparse import parse_qs, parse_qsl

from talesclient import TalesClient

_url = sys.argv[0]
_handle = int(sys.argv[1])

client = TalesClient()


def listTales():
    for tale in client.getTaleList():
        length = ':'.join(tale.size.split('.'))
        itemCaption = '{0} [{1}]'.format(tale.name, length)
        listItem = xbmcgui.ListItem(label=itemCaption)
        listItem.setArt({'thumb': tale.thumbUrl, 'poster': tale.imageUrl, 'fanArt': tale.imageUrl})
        listItem.setProperty('IsPlayable', 'true')

        url = '{0}?action=playTale&url={1}'.format(_url, tale.fileUrl)
        xbmcplugin.addDirectoryItem(_handle, url, listItem, False)

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_handle)


def playTale(fileUrl):
    playItem = xbmcgui.ListItem(path=fileUrl)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=playItem)


def router(paramstring):
    params = dict(parse_qsl(paramstring))

    if params:
        if params['action'] == 'playTale':
            playTale(params['url'])
    else:
        listTales()


if __name__ == '__main__':
    router(sys.argv[2][1:])
