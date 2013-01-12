import facebook

my_token = "AAACEdEose0cBAEKG4ZAXuUc5GXvqI9bAZAgEXQh6SzaNlLCYyBlznSk26za80ACll5YakxwOZBuz4qiWRTqqNKLba2wuzw3KDf4PDxVSbEGGGZCvBFIf"

api = facebook.GraphAPI(my_token)

def create_test_user(name):
    path = facebook_app_id + "/accounts/test-users"
    post_args = {
        "installed" : True,
        "name" : name,
        "locale" : "en_US",
        "permissions" : "read_stream",
    }
    return api.request(
        path,
        post_args=post_args
    )

