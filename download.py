import facebook

my_token = "AAACEdEose0cBAAHrG1I6ae0tINfsp1CdN7pAlaecafXYvEoFPFVJZBGAX8YCxp41GwZCorvzYs1esZCoZCh1KYHQvoNq77RwdIBmzZBZCJ4AZDZD"
api = facebook.GraphAPI(my_token)

def get_photo_array(maxPhotos = 150):
    photos = []
    friends = api.fql("SELECT uid2 FROM friend WHERE uid1 = me() ORDER BY rand()")
    for friend in friends:
        data = api.get_connections(
            friend['uid2'],
            "picture",
            width="25",
            height="25")['data']
        photos.append(data)
        if len(photos) > maxPhotos: # for debugging, only download 20
            break
    return photos

def dump_photo_array(photos, path):
    counter = 0
    for photo in photos:
        with open(path+"/"+str(counter)+".jpeg", 'w') as f:
            f.write(photo)
            counter += 1

