from xbmcswift2 import Plugin
from resources.lib import mensrea

plugin = Plugin()

url1 = "https://feeds.acast.com/public/shows/1d1223a2-9d05-473b-9e79-c2b65b71d676"

@plugin.route('/all_mensrea/')
def all_mensrea():
    soup = mensrea.get_soup1(url1)
    playable_mensrea = mensrea.get_playable_mensrea(soup)
    items = mensrea.compile_playable_mensrea(playable_mensrea)
    
    for item in items:
        item['info'] = {
            'plot': item.get('description', '')  # Set description in 'info' plot field
        }
    
    kodi_items = []
    for podcast in items:
        kodi_items.append({
            'label': podcast['title'],
            'thumbnail': podcast['thumbnail'],
            'path': podcast['url'],
            'is_playable': True,
            'info': {
                'plot': podcast['info'].get('plot', '')
            }
        })
    
    return kodi_items

if __name__ == '__main__':
    plugin.run()
