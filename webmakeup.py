from urllib2 import urlopen

def get_image_from_url(url):
    return urlopen(url).read()
