import facebook

my_token = "AAACEdEose0cBAAHrG1I6ae0tINfsp1CdN7pAlaecafXYvEoFPFVJZBGAX8YCxp41GwZCorvzYs1esZCoZCh1KYHQvoNq77RwdIBmzZBZCJ4AZDZD"

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

