import eventlet
from eventlet.green import urllib2

import facebook


def get_photo_array(api, maxPhotos = 150):
    photos = []
    friends = api.fql("SELECT uid2 FROM friend WHERE uid1 = me() ORDER BY rand()")
    def dl_image_from_friend(friend):
        if len(photos) > maxPhotos:
            return None
        data = api.get_connections(
            friend['uid2'],
            "picture",
            width = 25,
            height = 25)['data']
        return data
    pool = eventlet.GreenPool()
    for data in pool.imap(dl_image_from_friend, friends):
        if data is not None:
            photos.append(data)
    return photos

def dump_photo_array(photos, path):
    counter = 0
    for photo in photos:
        with open(path+"/"+str(counter)+".jpeg", 'wb') as f:
            f.write(photo)
            counter += 1

if __name__ == "__main__":
    my_token = "AAACEdEose0cBAAHrG1I6ae0tINfsp1CdN7pAlaecafXYvEoFPFVJZBGAX8YCxp41GwZCorvzYs1esZCoZCh1KYHQvoNq77RwdIBmzZBZCJ4AZDZD"
    api = facebook.GraphAPI(my_token)

