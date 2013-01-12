import facebook

my_token = "AAACEdEose0cBAEKG4ZAXuUc5GXvqI9bAZAgEXQh6SzaNlLCYyBlznSk26za80ACll5YakxwOZBuz4qiWRTqqNKLba2wuzw3KDf4PDxVSbEGGGZCvBFIf"
api = facebook.GraphAPI(my_token)

def get_photo_array():
    photos = []
    friends = api.fql("SELECT uid2 FROM friend WHERE uid1 = me()")
    for friend in friends:
        data = api.get_connections(
            friend['uid2'],
            "picture",
            width="25",
            height="25")['data']
        photos.append(data)
        if len(photos) > 150: # for debugging, only download 20
            break
    return photos

def dump_photo_array(photos, path):
    counter = 0
    for photo in photos:
        with open(path+"/"+str(counter)+".jpeg", 'w') as f:
            f.write(photo)
            counter += 1

